from dotenv import load_dotenv
from pathlib import Path
from pyokx import OKXClient, Account, Marketdata, Trade
import time
import os
import sys
import time
import sqlite3

os.chdir(str(Path(os.path.dirname(__file__)).parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.absolute()))

from config import print_n_log, stopwatch, send_error_message

# Environment Variables
load_dotenv()

class Okx(OKXClient):
    def __init__(self):
        super().__init__(os.environ["OKX_API_KEY"], os.environ["OKX_SECRET_KEY"], os.environ["OKX_API_PASSPHRASE"], None, False)

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, okx FROM coins WHERE okx IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        print(tickers - db_tickers)

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, None, None, None, None, None, None, quote, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET okx=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("okx db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for (base, quote) in tuple(tuple(x['instId'].split("-")) for x in Marketdata(self).get_tickers(instType="SPOT").response.json()['data']):
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
    def get_avg_buying_price(self, coin, token_amount, currency="USDT"):
        total_buying = []
        remainder = token_amount
        order_books = Marketdata(self).get_order_lite_book(f"{coin}-{currency}").response.json()['data'][0]['asks']

        for order_book in order_books:
            order_book[0] = float(order_book[0])
            order_book[1] = float(order_book[1])
            remainder -= order_book[1]
            if remainder <= 0:
                total_buying.append(order_book[0] * (remainder + order_book[1]))
                return sum(buying for buying in total_buying) / token_amount
            else:
                total_buying.append(order_book[0] * order_book[1])
        if remainder > 0:
            return "Not enough liquidity"
    def maesoo(self, coin, usd_amount, currency="USDT"):
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "buy",
                "pair": (coin, currency)
            }

            # Get average price to calculate buying amount
            price = float(Marketdata(self).get_order_lite_book("{}-{}".format(coin, currency)).response.json()['data'][0]['asks'][0][0])
            avg_price = self.get_avg_buying_price(coin, usd_amount / price, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)

            # Buy Coin
            # Minimum order amount: 10 USD
            buying_result = Trade(self).place_order("{}-{}".format(coin, currency), "buy", "market", str(usd_amount), "cash")
            print(buying_result.response.json()['data'])

            bought_amount = round(usd_amount / avg_price, 8)

            result["result"] = "Passed"
            result["msg"] = (bought_amount, avg_price)
        except Exception as e:
            if len(e.args) != 1:
                e = e.args[3]['data'][0]['sMsg']
            print_n_log(f"{self.__class__.__name__} maesoo: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def maedo(self, coin, currency="USDT"):
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "sell",
                "pair": (coin, currency)
            }

            # Get Balance and Selling Amount
            coin_balance = Account(self).get_balance("{}".format(coin)).response.json()['data'][0]['details']
            if len(coin_balance) == 0:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_amount = float(coin_balance[0]['availBal'])
            price = float(Marketdata(self).get_order_lite_book("{}-{}".format(coin, currency)).response.json()['data'][0]['bids'][0][0])
            usd_balance = selling_amount * price

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if usd_balance < 3:
                raise Exception('Not enough {} to sell.'.format(coin))

            selling_result = Trade(self).place_order("{}-{}".format(coin, currency), "sell", "market", str(selling_amount), "cash")
            print(selling_result.response.json()['data'])

            result["result"] = "Passed"
            result["msg"] = (selling_amount, price)
        except Exception as e:
            if len(e.args) != 1:
                e = e.args[3]['data'][0]['sMsg']
            print_n_log(f"{self.__class__.__name__} maedo: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def borrow_margin(self, coin, currency="USDT"):
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "margin",
                "pair": coin
            }

            # Get USDT Amount
            usdt_balance = Account(self).get_balance("USDT").response.json()['data'][0]['details']
            if len(usdt_balance) == 0:
                raise Exception('Not enough USDT balance in the wakket.')
            usdt_balance = float(usdt_balance[0]['availBal'])

            # Get average price to calculate buying amount
            price = Marketdata(self).get_order_lite_book(f"{coin}-{currency}").response.json()['data'][0]['asks']
            print(price)
            avg_price = self.get_avg_buying_price(coin, token_amount, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)

            # Market buy tokens
            buying_result = Trade(self).place_order(
                f"{coin}-{currency}",
                "buy",
                "market",
                str(token_amount * avg_price),
                "cash"
            )
            print(buying_result.response.json()['data'])

            # Isolated margin borrow
            margin_result = Trade(self).place_order(
                instId=f"{coin}-{currency}",
                tdMode="cross",
                ccy=currency,
                side="sell",
                ordType="market",
                sz=str(token_amount)
            )
            print(margin_result.response.json()['data'])

            result["result"] = "Passed"
            # result["msg"] = (amount, price, last_mark_price)
        except Exception as e:
            if len(e.args) != 1:
                e = e.args[3]['data'][0]['sMsg']
            print_n_log(f"{self.__class__.__name__} margin: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def borrow_loan(self, coin, amount, currency="USDT"):
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "margin",
                "pair": coin
            }

            # Isolated margin borrow
            margin_result = Trade(self).place_order(
                instId=f"{coin}-{currency}",
                tdMode="cross",
                ccy=currency,
                side="sell",
                ordType="market",
                sz=str(amount)
            )
            print(margin_result.response.json()['data'])

            result["result"] = "Passed"
            # result["msg"] = (amount, price, last_mark_price)
        except Exception as e:
            if len(e.args) != 1:
                e = e.args[3]['data'][0]['sMsg']
            print_n_log(f"{self.__class__.__name__} margin: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result

if __name__ == "__main__":
    start = time.time()
    Okx = Okx()
    Okx.borrow_margin("USTC", 100)
    end = time.time()
    print(end - start)