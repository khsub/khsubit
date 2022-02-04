import time
import pyupbit
import datetime
import numpy as np

access = "xwSHBhkiNNAWYBxFQ52QdKQy5lx8aCFgJwGKhJSc"
secret = "imj8DPP97x0gBE6Fo65xs7OvIea7CRlcGNxG9N7Z"

# Inquire the purchase target price with a strategy to break through volatility
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=16) # search days
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

# Start time
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# Balance inquiry
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

# Current price inquiry
def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# Check Up & Down
def get_check_point():
    df = pyupbit.get_ohlcv("KRW-BTC")
    ma5 = df['close'].rolling(window=16).mean() # check days
    last_ma5 = ma5[-2]
    price = pyupbit.get_current_price("KRW-BTC")
    if price > last_ma5:
        return 0.3
    else:
        return 0.7

# Coin average price
def get_avg_buy_price(coin):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
        time.sleep(0.2)
    return 0

# LOGIN
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# start auto trade
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") # 09:00
        end_time = start_time + datetime.timedelta(days=1) # 09:00 + 1

        amount = get_balance("BTC") #upbit.get_balance(coin)    0.00959525 보유수량 (비코개수)
        cur_price = pyupbit.get_current_price("KRW-BTC")        #45776000.0 현재가
        total = amount * cur_price                              #439232.164 환산매수금 (살때 쓴돈)
        old_price = get_avg_buy_price("BTC")                    #45750802.9525 매수평균가
        old_total = amount * old_price                          #438990.3920 매수금

        chk_point = get_check_point()                           #하락 & 상승 체크 (하락 0.3 상승 0.7)
        target_price = get_target_price("KRW-BTC", chk_point)
        current_price = get_current_price("KRW-BTC")

        #print(get_check_point())
        #print(get_target_price("KRW-BTC", chk_point))
        #print(get_current_price("KRW-BTC"))
        #print(old_total)
        #print("=======")

        if chk_point == 0.3: # bull market 
            if (total >= old_total * 1.045 or total <= old_total * 0.955) and old_total > 1000: # +5.5% or -4.5% 
                upbit.sell_market_order("KRW-BTC", amount*0.7) # 70%
                print("1111111111111")
                time.sleep(300) # Stop 5 minute 
        else: # bear market 
            if (total >= old_total * 1.035 or total <= old_total * 0.965) and old_total > 1000: # ±3.5%
                upbit.sell_market_order("KRW-BTC", amount) # All Sell
                print("2222222222222")
                time.sleep(300)
        
        if start_time < now < end_time - datetime.timedelta(seconds=10): # non Time 08:50 ~ 09:00
            if target_price < current_price:
                print("3333333333333")
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.6)
                    print("44444444444444")
                    time.sleep(300)
        else:
            # All sales over 1000
            if old_total > 1000:
                if chk_point == 0.3:
                    print("555555555555")
                    if total >= old_total * 1.02 or total <= old_total * 0.98:
                        print("6666666666666")
                        upbit.sell_market_order("KRW-BTC", amount)
                else:
                    upbit.sell_market_order("KRW-BTC", amount)
                    print("77777777777777")
            time.sleep(10)

        time.sleep(1.5)
    except Exception as e:
        print(e)
        time.sleep(1)