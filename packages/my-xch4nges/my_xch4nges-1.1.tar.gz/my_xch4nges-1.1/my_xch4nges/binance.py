from dotenv import load_dotenv
import asyncio
import aiohttp
import hmac
import hashlib
import os
import sqlite3
import time
import urllib

# Environment Variables
load_dotenv()

class Binance():
    def __init__(self):
        self.apikey = os.environ["BINANCE_API_KEY"]
        self.secret = os.environ["BINANCE_SECRET_KEY"]
        self.endpoint_url = "https://api.binance.com"

    # API methods
    async def HTTP_public_request(self, method, endpoint, payload = {}):
        start = time.time()
        httpClient=aiohttp.ClientSession()

        headers = {
            'X-MBX-APIKEY': self.apikey,
            'Content-Type': 'application/json'
        }

        async with httpClient as client:
            try:
                response = await client.request(method, self.endpoint_url + endpoint + "?" + urllib.parse.urlencode(payload), headers=headers)
                assert response.status == 200, f'status code error {response.status}'
                response = await response.json()
                print(response)
                print(time.time() - start)

                return response

            except AssertionError as e:
                response = await response.json()
                raise Exception(response)

    async def HTTP_private_request(self, method, endpoint, payload = {}):
        start = time.time()
        httpClient=aiohttp.ClientSession()
        payload = urllib.parse.urlencode(payload) + "&timestamp={}".format(int(time.time() * 10 ** 3))
        payload = payload + "&signature={}".format(self.genSignature(payload))

        headers = {
            'X-MBX-APIKEY': self.apikey,
            'Content-Type': 'application/json'
        }

        async with httpClient as client:
            try:
                response = await client.request(method, self.endpoint_url + endpoint + "?" + payload, headers=headers)

                assert response.status == 200, f'status code error {response.status}'
                response = await response.json()
                print(time.time() - start)
                print(response)
                return response

            except AssertionError as e:
                response = await response.json()
                raise Exception(response)

    def genSignature(self, payload):
        return hmac.new(self.secret.encode("utf-8"), payload.encode("utf-8"),hashlib.sha256).hexdigest()

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = tuple(cur.execute("SELECT symbol, binance FROM coins WHERE binance IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, quote, None, None, None, None, None, None, None, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET binance=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("binance db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for (base, quote) in ((x["baseAsset"], x['quoteAsset']) for x in self.HTTP_public_request("GET", "/api/v3/exchangeInfo")['symbols']):
            if 'USDT' == quote[-4:] or 'BUSD' == quote[-4:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            elif ('KRW' == quote[-3:] and 'BKRW' != quote[-4:]):
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            else:
                print(f"Passing {base}{quote}")
        return tuple((key, ", ".join(value)) for key, value in ticker_dict.items())

    # Trading methods
    def get_avg_buying_price(self, coin, amount, currency):
        total_buying = []
        remainder = amount
        order_books = self.HTTP_public_request("GET", "/api/v3/depth", {
            "symbol": "{}{}".format(coin, currency),
            "limit": 99
        })['asks']

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
    def maesoo(self, coin, buying_amount, currency): # Deprecated
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "buy",
                "pair": (coin, currency)
            }

            # Get average price to calculate buying amount
            price = float(self.HTTP_public_request("GET", "/api/v3/ticker/price", {
                "symbol": "{}{}".format(coin, currency)
            })['price'])
            avg_price = self.get_avg_buying_price(coin, buying_amount/price, currency)
            if type(avg_price) == "str":
                raise Exception(avg_price)

            # Buy Coin
            # Minimum order amount: 10 USD
            buying_result = self.HTTP_private_request("POST", "/api/v3/order", {
                "symbol": "{}{}".format(coin, currency),
                "side": "BUY",
                "type": "MARKET",
                "quoteOrderQty": buying_amount
            })
            if "msg" in buying_result:
                raise Exception(buying_result['msg'])

            bought_amount = round(buying_amount / avg_price, 8)

            result["result"] = "Passed"
            result["msg"] = (bought_amount, avg_price)
        except Exception as e:
            print(e)
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def maedo(self, coin, currency): # Deprecated
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "sell",
                "pair": (coin, currency)
            }

            # Get Balance and Selling Amount
            balance_free = self.HTTP_private_request("POST", "/sapi/v3/asset/getUserAsset", {"asset": "{}".format(coin)})
            if balance_free == []:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_amount = float(balance_free[0]['free'])
            price = float(self.HTTP_public_request("GET", "/api/v3/ticker/price", {
                "symbol": "{}{}".format(coin, currency)
            })['price'])
            usd_balance = selling_amount * price

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if usd_balance < 3:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_result = self.HTTP_private_request("POST", "/api/v3/order", {
                "symbol": "{}{}".format(coin, currency),
                "side": "SELL",
                "type": "MARKET",
                "quantity": selling_amount
            })
            if "msg" in selling_result:
                raise Exception(selling_result['msg'])

            result["result"] = "Passed"
            result["msg"] = (selling_amount, price)
        except Exception as e:
            # raise Exception(e)
            print(e)
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def borrow_margin(self, coin):
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "margin",
                "pair": coin
            }

            # Cross margin borrow
            response = asyncio.run(self.HTTP_private_request("GET", "/sapi/v1/margin/maxBorrowable", {
                "asset": coin
            }))

            margin_borrow_amount = min(float(response['borrowLimit']), round(float(response['amount']) * 0.99, 4))
            print("margin_borrow_amount:", margin_borrow_amount)

            margin_result = asyncio.run(self.HTTP_private_request("POST", "/sapi/v1/margin/loan", {
                "asset": coin,
                "amount": margin_borrow_amount
            }))
            print(margin_result)
            result["result"] = "Passed"
            result["msg"] = f"{margin_borrow_amount} {coin}"
        except Exception as e:
            print(f"{self.__class__.__name__} margin: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def borrow_loan(self, coin, collateral="USDT"):
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "loan",
                "pair": coin
            }

            # Binance loan borrow
            response = asyncio.run(self.HTTP_private_request("GET", "/sapi/v1/loan/loanable/data", {
                "loanCoin": coin,
            }))

            # Denomiated in USD
            loan_borrow_amount = float(response['rows'][0]['maxLimit'])

            response = asyncio.run(self.HTTP_private_request("POST", "/sapi/v3/asset/getUserAsset", {
                "asset": collateral
            }))

            loan_borrow_amount = min(loan_borrow_amount, round(float(response[0]['free']) * 0.99,4))
            print("loan_borrow_amount:", loan_borrow_amount)

            loan_result = asyncio.run(self.HTTP_private_request("POST", "/sapi/v1/loan/borrow", {
                "loanCoin": coin,
                "collateralCoin": collateral,
                "collateralAmount": loan_borrow_amount,
                "loanTerm": 7
            }))

            result["result"] = "Passed"
            result["msg"] = f"{loan_result['loanAmount']} {coin}"
        except Exception as e:
            print(f"{self.__class__.__name__} loan: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result

if __name__ == "__main__":
    binance = Binance()
    # binance.borrow_margin("LAZIO")

    # asyncio.run(binance.HTTP_private_request("POST", "/sapi/v1/capital/withdraw/apply", {
    #         "coin": "AVAX",
    #         "netowrk": "AVAXC",
    #         "amount": 0.3,
    #         "address":  "0xbd262Ff3437eaFa02197199F8003abACED95d741"
    #     }))