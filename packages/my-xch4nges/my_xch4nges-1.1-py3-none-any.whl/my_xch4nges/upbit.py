from dotenv import load_dotenv
import pyupbit
import time
import os
import time
import sqlite3

# Environment Variables
load_dotenv()

class Upbit(pyupbit.Upbit):
    def __init__(self):
        super().__init__(os.environ['UPBIT_API_KEY'], os.environ['UPBIT_SECRET_KEY'])

    # Ticker methods
    def update_ticker(self):
        con = sqlite3.connect('noti.db')
        cur = con.cursor()
        db_tickers = set(cur.execute("SELECT symbol, upbit FROM coins WHERE upbit IS NOT NULL").fetchall())
        tickers = self.format_ticker()

        print(tickers - db_tickers)

        if db_tickers != tickers:
            insert_params = []
            update_params = []
            db_base = tuple(element[0] for element in cur.execute("SELECT symbol FROM coins").fetchall())
            db_quote = tuple(quote for (base, quote) in db_tickers)

            for (base, quote) in tickers:
                if base not in db_base:
                    insert_params.append((base, None, None, None, None, None, None, None, None, quote))
                elif quote != db_quote:
                    update_params.append((quote, base))

            cur.executemany("INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_params)
            cur.executemany("UPDATE coins SET upbit=? WHERE symbol=?", update_params)
            con.commit()
            con.close()
        else:
            print("upbit db not changed")
    def format_ticker(self):
        ticker_dict = {}
        for (quote, base) in tuple(tuple(x.split("-")) for x in self.get_tickers()):
            if 'USDT' == quote[-4:] or 'USDC' == quote[-4:] or 'BUSD' == quote[-4:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            elif 'BTC' == quote[-3:] or 'KRW' == quote[-3:]:
                if base not in ticker_dict.keys():
                    ticker_dict[base] = []
                ticker_dict[base].append(quote)
            else:
                print(f"Passing {base}{quote}")
        
        tickers = set((key, ", ".join(value)) for key, value in ticker_dict.items())
        tickers = {(t[0], 'KRW') if 'KRW' in t[1] and ('BTC' in t[1] or 'USDT' in t[1]) else t for t in tickers}
        tickers = {(t[0], 'KRW') if 'BTC' in t[1] and 'USDT' in t[1] else t for t in tickers}
        return tickers

    # Trading methods
    def get_avg_buying_price(self, coin, amount, currency):
        if currency == "BTC":
            amount = amount / self.get_orderbook(ticker="KRW-BTC")['orderbook_units'][0]['ask_price']
        total_buying = []
        remainder = amount

        for order_book in ((x['ask_price'], x['ask_size'])for x in self.get_orderbook(ticker="{}-{}".format(currency, coin))['orderbook_units']):
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
            # Account for exchange rate
            result = {
                "exchange": self.__class__.__name__,
                "side": "buy",
                "pair": (coin, currency)
            }
            # buying_amount = buying_amount * EXCHANGE_RATE
            # Calcualte average price to determine buying amount
            price = self.get_current_price("{}-{}".format(currency, coin))
            avg_price = self.get_avg_buying_price(coin, buying_amount / price, currency)
            if type(avg_price) is str:
                raise Exception(avg_price)
            # Reduce Order Volume if Price Volatility is too high (current parameter: 5%)
            '''
            if abs(((avg_price - price)/price)*100) >= 5:
                buying_amount = 1500
                #raise Exception("Price volatility too high. Aborting Order...")            
            '''

            # Buy Coin
            if currency == "BTC":
                buying_result = self.buy_market_order(
                    ticker="KRW-BTC",
                    price=buying_amount*1.01
                )
                # Check if order was successful
                if 'created_at' not in buying_result:
                    raise Exception(buying_result)

                # Calculate BTC Price
                btc_price = self.get_orderbook(ticker="KRW-BTC")['orderbook_units'][0]['bid_price']
                btc_amount = round(buying_amount / btc_price, 8)

                # Minimum order amount: 0.0005
                buying_result = self.buy_market_order(
                    ticker=f"{currency}-{coin}",
                    price=btc_amount
                )
                # Check if order was successful
                if 'created_at' not in buying_result:
                    raise Exception(buying_result)

                # Calculate bought amount
                bought_amount = round((buying_amount / btc_price), 8)
            else:
                # Minimum order amount: 1,000 KRW
                buying_result = self.buy_market_order(
                    f"{currency}-{coin}",
                    volume=buying_amount,
                    price=320
                )
                if 'created_at' not in buying_result: # Also includes UpbitError
                    raise Exception(buying_result)

            # Calculate bought amount
            bought_amount = round(buying_amount / avg_price, 8)

            result["result"] = "Passed"
            result["msg"] = (bought_amount, avg_price)
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
            amount = self.get_balance(ticker="{}".format(coin))
            price = self.get_orderbook(ticker="{}-{}".format(currency, coin))['orderbook_units'][1]['bid_price']

            if currency == "BTC":
                krw_balance = amount * price * self.get_orderbook(ticker="KRW-BTC")['orderbook_units'][0]['bid_price']
            else:
                krw_balance = amount * price

            # Denominate coin balance in KRW to count in garbage amount like 50 KRW
            if krw_balance < 3000:
                raise Exception('Not enough {} to sell.'.format(coin))

            if currency == "BTC":
                # Volume: Coin Amount
                selling_result = self.sell_market_order(
                    ticker=f"{currency}-{coin}",
                    volume=amount
                )
                if 'created_at' not in selling_result:
                    raise Exception(selling_result)

                btc_received = self.get_balance("BTC")
                while btc_received <= 0.0002:
                    btc_received = self.get_balance("BTC")

                selling_result = self.sell_market_order(
                    ticker="KRW-BTC",
                    volume=btc_received
                )
                if 'created_at' not in selling_result:
                    raise Exception(selling_result)
            else:
                selling_result = self.sell_market_order(
                    ticker=f"{currency}-{coin}",
                    volume=amount
                )
                if 'created_at' not in selling_result:
                    raise Exception(selling_result)

            last_mark_price = self.get_ohlcv(ticker="{}-{}".format(currency, coin), count=1, interval="minute1")['close'][0]

            result["result"] = "Passed"
            result["msg"] = (amount, price, last_mark_price)
        except Exception as e:
            print(f"{self.__class__.__name__} maedo: {e}")
            result["result"] = "Failed"
            result["msg"] = str(e)
        return result

if __name__ == "__main__":
    import random
    upbit = Upbit()
    start = time.time()
    # Token counts, not krw based when limit order
    upbit.maesoo("GLM", 1000, "KRW")
    end = time.time()
    print(end - start)
    time.sleep(random.randint(1, 5) / 10)