from dotenv import load_dotenv
import hmac
import hashlib
import json
import math
import os
import random
import requests
import sqlite3
import time
import urllib
import uuid

# Environment Variables
load_dotenv()

class bybit():
    def __init__(self):
        self.apikey = os.environ["BYBIT_API_KEY"]
        self.secret = os.environ["BYBIT_SECRET_KEY"]
        self.endpoint_url = "https://api.bybit.com"

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
        recv_window=str(5000)
        time_stamp=str(int(time.time() * 10 ** 3))
        payload_encoded = urllib.parse.urlencode(payload)

        if method == "GET":
            signature=self.genSignature(payload_encoded, time_stamp, recv_window)
        else:
            signature=self.genSignature(json.dumps(payload), time_stamp, recv_window)

        headers = {
            'X-BAPI-API-KEY': self.apikey,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': recv_window,
            'Content-Type': 'application/json'
        }
        try:
            if(method=="GET"):
                response = requests.get(f"{self.endpoint_url}{endpoint}?{payload_encoded}", headers=headers)
            else:
                response = requests.post(f"{self.endpoint_url}{endpoint}", json=payload, headers=headers)
            return response.json()
        except AssertionError as e:
            print(e)
            raise Exception(e)
    def genSignature(self, payload, time_stamp, recv_window):
        param_str= str(time_stamp) + self.apikey + recv_window + payload
        return hmac.new(bytes(self.secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
    def uuid(self, a = None):
        if a:
            return format((a ^ random.random() * 16 >> a / 4), 'x')
        else:
            return str(uuid.uuid4())

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, bybit FROM coins WHERE bybit IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, None, None, quote, None, None, None, None, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET bybit=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("bybit db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for (base, quote) in ((x['baseCoin'], x['quoteCoin']) for x in self.HTTP_public_request("GET", "/spot/v3/public/symbols")['result']['list']):
            if 'USDT' == quote[-4:] or 'USDC' == quote[-4:] or 'BUSD' == quote[-4:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            elif 'KRW' == quote[-3:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            else:
                print(f"Passing {base}{quote}")
        return set((key, ", ".join(value)) for key, value in ticker_dict.items())

    # Trading methods
    def get_avg_buying_price(self, coin, amount, currency):
        total_buying = []
        remainder = amount
        order_books = self.HTTP_public_request("GET", "/spot/v3/public/quote/depth", {
            "symbol": "{}{}".format(coin, currency),
            "limit": 30
        })['result']['asks']

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
            price = float(self.HTTP_public_request("GET", "/spot/v3/public/quote/ticker/bookTicker", {
                "symbol": "{}{}".format(coin, currency)
            })['result']['askPrice'])
            avg_price = self.get_avg_buying_price(coin, buying_amount / price, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)

            # Buy Coin
            # Minimum order amount: 10 USD
            buying_result = self.HTTP_private_request("POST", "/spot/v3/private/order", {
                "symbol": "{}{}".format(coin, currency),
                "orderType": "Market",
                "side": "Buy",
                "orderQty":str(buying_amount),
                "timeInForce": "IOC"
            })
            if "retMsg" in buying_result:
                raise Exception(buying_result['retMsg'])

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

            # Set order precision
            precision = self.HTTP_public_request("GET", "/spot/v3/public/symbols")
            precision = tuple(filter(lambda x: x['name'] == "{}{}".format(coin, currency), precision['result']['list']))[0]['basePrecision']
            precision_count = len(str(precision).split('.')[1])

            # Get Balance and Selling Amount
            selling_amount = float(self.HTTP_private_request("GET", "/asset/v3/private/transfer/account-coin/balance/query", {
                    "accountType": "SPOT",
                    "coin": coin
                })['result']['balance']['walletBalance'])
            selling_amount = math.floor(selling_amount * 10 ** precision_count) / 10 ** precision_count

            price = float(self.HTTP_public_request("GET", "/spot/v3/public/quote/ticker/bookTicker", {
                "symbol": "{}{}".format(coin, currency)
            })['result']['bidPrice'])
            usd_balance = float("{:.8f}".format(selling_amount * price))

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if usd_balance < 3:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_result = self.HTTP_private_request("POST", "/spot/v3/private/order", {
                "symbol": "{}{}".format(coin, currency),
                "orderType": "Market",
                "side": "Sell",
                "orderQty":str(selling_amount),
                "timeInForce": "IOC"
            })
            if "retMsg" in selling_result:
                raise Exception(selling_result['retMsg'])

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
    bybit = bybit()
    start = time.time()
    # bybit.maesoo('HVH', 15, "USDT")
    bybit.maedo('HVH', "USDT")
    end = time.time()
    print(end - start)