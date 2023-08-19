from dotenv import load_dotenv
import hmac
import hashlib
import os
import random
import requests
import sqlite3
import time
import urllib
import uuid

# Environment Variables
load_dotenv()

class mexc():
    def __init__(self):
        self.apikey = os.environ["MEXC_API_KEY"]
        self.secret = os.environ["MEXC_SECRET_KEY"]
        self.endpoint_url = "https://api.mexc.com"

    # API methods
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
        payload.update({
            "recvWindow": str(5000),
            "timestamp": str(int(time.time() * 10 ** 3))
        })
        payload_encoded = urllib.parse.urlencode(payload)
        signature=self.genSignature(payload_encoded)
        headers = {
            'X-MEXC-APIKEY': self.apikey,
            'Content-Type': 'application/json'
        }
        try:
            if(method=="GET"):
                response = requests.get(f"{self.endpoint_url}{endpoint}?{payload_encoded}&signature={signature}", headers=headers)
            else:
                response = requests.post(f"{self.endpoint_url}{endpoint}?signature={signature}", data=payload, headers=headers)
            return response.json()
        except AssertionError as e:
            print(e)
            raise Exception(e)
    def genSignature(self, payload):
        return hmac.new(bytes(self.secret, "utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    def uuid(self, a = None):
        if a:
            return format((a ^ random.random() * 16 >> a / 4), 'x')
        else:
            return str(uuid.uuid4())

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, mexc FROM coins WHERE mexc IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        print(tickers - db_tickers)

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, None, None, None, None, None, quote, None, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET mexc=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("mexc db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for ticker in tuple(x['symbol'] for x in self.HTTP_public_request("GET", "/api/v3/ticker/price")):
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

        order_books = self.HTTP_public_request("GET", "/api/v3/depth", {
            "symbol": "{}{}".format(coin, currency),
            "limit": 30
        })['asks']

        for order_book in order_books:
            order_book[0] = float(order_book[0])
            order_book[1] = float(order_book[1])
            remainder -= order_book[1]
            if remainder <= 0:
                total_buying.append(order_book[0] * (remainder + order_book[1]))
                return order_book[0]
            else:
                total_buying.append(order_book[0] * order_book[1])
        if remainder > 0:
            return "Not enough liquidity"
    def get_avg_selling_price(self, coin, amount, currency):
        total_buying = []
        remainder = amount

        order_books = self.HTTP_public_request("GET", "/api/v3/depth", {
            "symbol": "{}{}".format(coin, currency),
            "limit": 30
        })['bids']

        for order_book in order_books:
            order_book[0] = float(order_book[0])
            order_book[1] = float(order_book[1])
            remainder -= order_book[1]
            if remainder <= 0:
                total_buying.append(order_book[0] * (remainder + order_book[1]))
                return order_book[0]
            else:
                total_buying.append(order_book[0] * order_book[1])
        if remainder > 0:
            return "Not enough liquidity"
    def maesoo(self, coin, buying_amount, currency):
        try:
            result = {}

            # Get average price to calculate buying amount
            price = float(self.HTTP_public_request("GET", "/api/v3/ticker/price", {"symbol": "{}{}".format(coin, currency)})['price'])
            avg_price = self.get_avg_buying_price(coin, buying_amount / price, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)

            # Buy Coin
            # Minimum order amount: 5 USD
            buying_result = self.HTTP_private_request("POST", "/api/v3/order", {
                "symbol": "{}{}".format(coin, currency),
                "side": "BUY",
                "type": "LIMIT",
                "quantity": buying_amount / price,
                "price": avg_price,
                "timeInForce": "IOC"
            })
            if "msg" in buying_result:
                raise Exception(buying_result['msg'])

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
            account_balance = tuple(filter(lambda x: x['asset'] == coin, self.HTTP_private_request("GET", "/api/v3/account")['balances']))
            if len(account_balance) == 0:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_amount = float(account_balance[0]['free'])
            price = self.get_avg_selling_price(coin, selling_amount, currency)
            usd_balance = float("{:.8f}".format(selling_amount * price))

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if usd_balance < 3:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_result = self.HTTP_private_request("POST", "/api/v3/order", {
                "symbol": "{}{}".format(coin, currency),
                "side": "SELL",
                "type": "LIMIT",
                "price": price,
                "quantity":selling_amount,
                "timeInForce": "IOC"
            })
            if "msg" in selling_result:
                raise Exception(selling_result['msg'])

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
    mexc = mexc()
    start = time.time()
    mexc.maedo("BFC", "USDT")
    end = time.time()
    print(end - start)