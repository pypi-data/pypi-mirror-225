from dotenv import load_dotenv
from gate_api import ApiClient, Configuration, SpotApi, WalletApi, Order
import time
import os
import time
import sqlite3

# Environment Variables
load_dotenv()

class gateio(ApiClient):
    def __init__(self, configuration=None, header_name=None, header_value=None, cookie=None, pool_threads=1):
        configuration = Configuration(
            host = "https://api.gateio.ws/api/v4",
            key = os.environ['GATE_API_KEY'],
            secret = os.environ['GATE_SECRET_KEY']
        )
        super().__init__(configuration, header_name, header_value, cookie, pool_threads)

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, gateio FROM coins WHERE gateio IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        print(tickers - db_tickers)

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, None, None, None, quote, None, None, None, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET gateio=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("gate db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for (base, quote) in (tuple(tuple(x.currency_pair.split("_")) for x in SpotApi(self).list_tickers())):
            if 'USDT' == quote[-4:] or 'USDC' == quote[-4:] or 'BUSD' == quote[-4:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            elif ('KRW' == quote[-3:] and 'BKRW' != quote[-4:]):
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
        order_books = SpotApi(self).list_order_book("{}_{}".format(coin, currency), interval = 1, limit = 20).asks

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
            price = float(SpotApi(self).list_order_book("{}_{}".format(coin, currency), interval = 1, limit = 1).asks[0][0])
            avg_price = self.get_avg_buying_price(coin, buying_amount / price, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)

            # Buy Coin
            # Minimum order amount: 10 USD
            SpotApi(self).create_order(Order(
                currency_pair="{}_{}".format(coin, currency),
                type="market",
                account="spot",
                side="buy",
                amount=buying_amount,
                time_in_force="ioc"
            ))

            bought_amount = round(buying_amount / avg_price, 8)
            result["exchange"] = self.__class__.__name__
            result["pair"] = (coin, currency)
            result["result"] = "Passed"
            result["msg"] = (bought_amount, avg_price)
        except Exception as e:
            if hasattr(e, "message"):
                e = e.message
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
            selling_amount = float(tuple(filter(lambda x: x.currency == coin, SpotApi(self).list_spot_accounts()))[0].available)
            price = float(SpotApi(self).list_order_book("{}_{}".format(coin, currency), interval = 1, limit = 20).bids[0][0])
            usd_balance = "{:.8f}".format(selling_amount * price)

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if float(usd_balance) < 3:
                raise Exception('Not enough {} to sell.'.format(coin))

            SpotApi(self).create_order(Order(
                currency_pair="{}_{}".format(coin, currency),
                type="market",
                account="spot",
                side="sell",
                amount=selling_amount,
                time_in_force="ioc"
            ))

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
    gateio = gateio()
    start = time.time()
    gateio.maedo("WEMIX", "USDT")
    end = time.time()
    print(end - start)