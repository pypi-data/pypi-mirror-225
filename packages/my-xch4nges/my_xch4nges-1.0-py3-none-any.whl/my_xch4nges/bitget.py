from dotenv import load_dotenv
from pathlib import Path
from pybitget import Client
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

class bitget(Client):
    def __init__(self):
        super().__init__(os.environ['BITGET_API_KEY'], os.environ['BITGET_SECRET_KEY'], os.environ['BITGET_API_PASSPHRASE'], use_server_time=False, verbose=False)

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, bitget FROM coins WHERE bitget IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, quote, None, None, None, None, None, None, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET bitget=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("bitget db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for ticker in tuple(x['symbol'] for x in self.spot_get_tickers()['data']):
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
        order_books = self.spot_get_depth(symbol="{}{}_SPBL".format(coin, currency), limit=50, type='step0')['data']['asks']

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
            price = float(self.spot_get_ticker(symbol="BTCUSDT_SPBL")['data']['buyOne'])
            avg_price = self.get_avg_buying_price(coin, buying_amount / price, currency)
            if type(avg_price) == "str":
                raise Exception(avg_price)

            # Buy Coin
            # Minimum order amount: 10 USD
            self.spot_place_order(
                symbol="{}{}_SPBL".format(coin, currency),
                side="buy",
                orderType="market",
                force="ioc",
                quantity=buying_amount
            )

            bought_amount = round(buying_amount / avg_price, 8)

            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Passed"
            result["msg"] = (buying_amount, avg_price)
        except Exception as e:
            # raise Exception(e)
            print_n_log(e)
            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def maedo(self, coin, currency):
        try:
            result = {}

            # Get Balance and Selling Amount
            selling_amount = float(self.spot_get_account_assets(coin=coin)['data'][0]['available'])
            price = float(self.spot_get_ticker(symbol="BTCUSDT_SPBL")['data']['sellOne'])
            usd_balance = "{:.8f}".format(selling_amount * price)

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if float(usd_balance) < 3:
                raise Exception('Not enough {} to sell.'.format(coin))

            self.spot_place_order(
                symbol="{}{}_SPBL".format(coin, currency),
                side="sell",
                orderType="market",
                force="ioc",
                quantity=selling_amount
            )
            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Passed"
            result["msg"] = (selling_amount, price)
        except Exception as e:
            print_n_log(e)
            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result

if __name__ == "__main__":
    bitget = bitget()
    coin="BTC"
    start = time.time()
    bitget.maedo(("BTC", ))
    end = time.time()
    print(end - start)