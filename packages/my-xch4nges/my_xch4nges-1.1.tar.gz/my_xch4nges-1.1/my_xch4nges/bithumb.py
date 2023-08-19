from dotenv import load_dotenv
from pybithumb.core import *
from pybithumb import Bithumb as Super_Bithumb
import time
import os
import time
import sqlite3

# Environment Variables
load_dotenv()

class Bithumb(Super_Bithumb):
    def __init__(self):
        super().__init__(os.environ['BITHUMB_API_KEY'], os.environ['BITHUMB_SECRET_KEY'])

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, bithumb FROM coins WHERE bithumb IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        print(db_tickers - tickers)

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, None, quote, None, None, None, None, None, None))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET bithumb=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("bithumb db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for (base, quote) in (list((base, "KRW") for base in self.get_tickers("KRW")) + list((base, "BTC") for base in self.get_tickers("BTC"))):
            if 'USDT' == quote[-4:] or 'USDC' == quote[-4:] or 'BUSD' == quote[-4:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            elif 'KRW' == quote[-3:] and 'BKRW' != quote[-4:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            else:
                print(f"Passing {base}{quote}")
        return set((key, ", ".join(value)) for key, value in ticker_dict.items())

    # Trading methods
    def get_avg_buying_price(self, coin, amount, currency):
        if currency == "BTC":
            amount = amount / self.get_orderbook("BTC")["asks"][0]["price"]

        total_buying = []
        remainder = amount

        for order_book in ((book['price'], book['price'] * book['quantity']) for book in self.get_orderbook(coin, payment_currency=currency)["asks"]):
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
            # Buying amount = KRW
            buying_amount = buying_amount
            result = {
                "exchange": self.__class__.__name__,
                "side": "buy",
                "pair": (coin, currency)
            }

            # Calcualte average price to determine buying amount
            avg_price = self.get_avg_buying_price(coin, buying_amount, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)
            '''
            # Reduce Order Volume if Price Volatility is too high (current parameter: 5%)
            if abs(((avg_price - price)/price)*100) >= 5:
                buying_amount = 1500
                #raise Exception("Price volatility too high. Aborting Order...")            
            '''

            # Buy Coin
            if currency == "BTC":
                btc_price = self.get_orderbook("BTC")["bids"][0]["price"]
                btc_amount = round((buying_amount*1.01) / btc_price, 8)

                buying_result = self.buy_market_order("BTC", btc_amount, "KRW")
                if type(buying_result) is dict:
                    raise Exception(buying_result["message"])

                # Minimum order amount: 0.0005
                buying_amount = round(buying_amount / btc_price, 8)
                buying_result = self.buy_market_order(coin, buying_amount, currency)
                if type(buying_result) is dict:
                    raise Exception(buying_result["message"])
            else:
                # Bithumb calculated market buy amount not by quote, but by base
                buying_amount = round(buying_amount / avg_price, 8)
                # Minimum order amount: 1,000 KRW
                buying_result = self.buy_market_order(coin, buying_amount, currency)
                if type(buying_result) is dict:
                    raise Exception(buying_result["message"])

            result["result"] = "Passed"
            result["msg"] = (buying_amount, avg_price)
        except Exception as e:
            print(f"{self.__class__.__name__} maesoo: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result
    def maedo(self, coin, currency):
        try:
            result = {
                "exchange": self.__class__.__name__,
                "side": "sell",
                "pair": (coin, currency)
            }

            # Get Balance and Selling Amount
            amount = self.get_balance(coin)[0]
            if currency == "BTC":
                price = self.get_orderbook(coin, payment_currency="BTC")["bids"][0]["price"]
                krw_balance = amount * price * self.get_orderbook("BTC")["bids"][0]["price"]
            else:
                price = self.get_orderbook(coin, payment_currency="KRW")["bids"][0]["price"]
                krw_balance = amount * price

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if krw_balance < 3000:
                raise Exception('Not enough {} to sell.'.format(coin))

            if currency == "BTC":
                selling_result = self.sell_market_order(coin, amount, "BTC")
                if type(selling_result) is dict:
                    raise Exception(selling_result["message"])

                btc_received = self.get_balance("BTC")[0]

                selling_result = self.sell_market_order("BTC", btc_received, "KRW")
                if type(selling_result) is dict:
                    raise Exception(selling_result["message"])

                mark_price = self.get_ohlc(coin, payment_currency=currency)[coin][-1]
            else:
                selling_result = self.sell_market_order(coin, amount, "KRW")
                if type(selling_result) is dict:
                    raise Exception(selling_result["message"])

                mark_price = self.get_ohlc(coin, payment_currency=currency)[coin][-1]

            result["result"] = "Passed"
            result["msg"] = (amount, price, mark_price)
        except Exception as e:
            print(f"{self.__class__.__name__} maedo: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result

if __name__ == "__main__":
    bithumb = Bithumb()
    start = time.time()
    bithumb.maesoo("ETH", 2, "KRW")
    end = time.time()
    print(end - start)