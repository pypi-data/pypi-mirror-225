from datetime import datetime
from dotenv import load_dotenv
import base64
import hmac
import hashlib
import math
import os
import requests
import sqlite3
import time
import urllib

# Environment Variables
load_dotenv()

class huobi():
    def __init__(self):
        self.apikey = os.environ["HUOBI_API_KEY"]
        self.secret = os.environ["HUOBI_SECRET_KEY"]
        self.account_id = os.environ["HUOBI_USER_ID"]
        self.endpoint_url = "https://api.huobi.pro"

    # Api methods
    def HTTP_public_request(self, method, endpoint, payload = {}):
        try:
            if method == "GET":
                response = requests.get(self.endpoint_url + endpoint + "?" + urllib.parse.urlencode(payload))
            else:
                response = requests.post(self.endpoint_url + endpoint + "?" + urllib.parse.urlencode(payload))
            return response.json()
        except Exception as e:
            print(e)
            raise Exception(e)
    def HTTP_private_request(self, method, endpoint, payload = {}):
        params = {
            "AccessKeyId": self.apikey,
            "SignatureMethod" : "HmacSHA256",
            "SignatureVersion": 2,
            "Timestamp": (datetime.utcnow()).isoformat(timespec="seconds")
        }
        prehash_params = urllib.parse.urlencode(sorted(params.items(),  key=lambda d: d[0]))
        prehash = f"{method}\n{self.endpoint_url[8:]}\n{endpoint}\n{prehash_params}"
        signature = self.genSignature(prehash)
        params['Signature'] = signature
        posthash_params = urllib.parse.urlencode(params)
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        try:
            if method == "GET":
                response = requests.get(f"{self.endpoint_url}{endpoint}?{posthash_params}", data=payload)
            else:
                response = requests.post(url=f"{self.endpoint_url}{endpoint}?{posthash_params}", json=payload)
            return response.json()
        except AssertionError as e:
            print(e)
            raise Exception(e)
    def genSignature(self, prehash):
        return base64.standard_b64encode(hmac.new(self.secret.encode('latin-1'), prehash.encode('latin-1'), hashlib.sha256).digest()).decode('latin-1')

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, huobi FROM coins WHERE huobi IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        print(tickers - db_tickers)

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, None, None, None, None, quote, None, None, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET huobi=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("huobi db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for ticker in (tuple(x['symbol'].upper() for x in self.HTTP_public_request("GET", "/market/tickers")['data'])):
            if 'USDT' == ticker[-4:] or 'USDC' == ticker[-4:] or 'BUSD' == ticker[-4:]:
                if ticker[:-4] not in ticker_dict.keys():
                    ticker_dict[ticker[:-4]] = []
                ticker_dict[ticker[:-4]].append(ticker[-4:])
            elif 'KRW' == ticker[-3:]:
                if ticker[:-4] not in ticker_dict.keys():
                    ticker_dict[ticker[:-3]] = []
                ticker_dict[ticker[:-3]].append(ticker[-3:])
            else:
                print(f"Passing {ticker}")
        return set((key, ", ".join(value)) for key, value in ticker_dict.items())
    
    # Trading methods
    def get_avg_buying_price(self, coin, amount, currency):
        total_buying = []
        remainder = amount
        order_books = self.HTTP_public_request("GET", "/market/depth", {
            "symbol": "{}{}".format(coin.lower(), currency.lower()),
            "type": "step0"
        })['tick']['asks']

        for order_book in order_books:
            order_book[0] = float(order_book[0])
            order_book[1] = float(order_book[1])
            remainder -= order_book[1]
            if remainder <= 0:
                total_buying.append(order_book[0] * (remainder + order_book[1]))
                return sum(buying for buying in total_buying) / amount
            else:
                total_buying.append(order_book[0] * order_book[1])
        if remainder > 0:
            return "Not enough liquidity"
    def maesoo(self, coin, buying_amount, currency):
        try:
            result = {}

            # Get average price to calculate buying amount
            price = float(self.HTTP_public_request("GET", "/market/depth", {
                "symbol": "{}{}".format(coin.lower(), currency.lower()),
                "type": "step1"
            })['tick']['asks'][0][0])
            avg_price = self.get_avg_buying_price(coin, buying_amount / price, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)

            # Buy Coin
            # Minimum order amount: 10 USD
            buying_result = self.HTTP_private_request("POST", "/v1/order/orders/place", {
                "account-id": self.account_id,
                "symbol": "{}{}".format(coin.lower(), currency.lower()),
                "type": "buy-market",
                "amount": buying_amount
            })
            if "err-msg" in buying_result:
                raise Exception(buying_result['err-msg'])

            bought_amount = round(buying_amount / avg_price, 8)
            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Passed"
            result["msg"] = (bought_amount, avg_price)
        except Exception as e:
            print(e)
            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def maedo(self, coin, currency):
        try:
            result = {}

            # Get Balance and Selling Amount
            res = None
            while res is None or res['status'] == "error":
                res = self.HTTP_private_request("GET", "/v1/account/accounts/{}/balance".format(self.account_id))

            # Match precision sepcified in api
            precision = tuple(filter(lambda x: x['symbol'] == "{}{}".format(coin.lower(), currency.lower()), self.HTTP_public_request("GET", "/v1/settings/common/symbols")['data']))[0]['tap']

            selling_amount = float(tuple(filter(lambda x: x['currency'] == coin.lower(), res['data']['list']))[0]['available'])
            selling_amount = math.floor(selling_amount * 10 ** precision) / 10 ** precision

            price = float(self.HTTP_public_request("GET", "/market/depth", {
                "symbol": "{}{}".format(coin.lower(), currency.lower()),
                "type": "step1"
            })['tick']['bids'][0][0])

            usd_balance = selling_amount * price

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if usd_balance < 3:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_result = self.HTTP_private_request("POST", "/v1/order/orders/place", {
                "account-id": self.account_id,
                "symbol": "{}{}".format(coin.lower(), currency.lower()),
                "type": "sell-market",
                "amount": selling_amount
            })
            if "err-msg" in selling_result:
                raise Exception(selling_result['err-msg'])

            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Passed"
            result["msg"] = (selling_amount, price)
        except Exception as e:
            print(e)
            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result

if __name__ == "__main__":
    huobi = huobi()
    start = time.time()
    # huobi.maesoo('HIVE', 10, 'USDT')
    huobi.maedo('HIVE', 'USDT')
    end = time.time()
    print(end - start)