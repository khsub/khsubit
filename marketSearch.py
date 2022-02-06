import time
import pyupbit
import datetime
import numpy as np

access = "xwSHBhkiNNAWYBxFQ52QdKQy5lx8aCFgJwGKhJSc"
secret = "imj8DPP97x0gBE6Fo65xs7OvIea7CRlcGNxG9N7Z"

# 변동성 돌파 전략으로 매수 목표가 조회
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=21)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

# 시작 시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# 잔고조
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

# 현재가 조회
def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 상승 & 하락 체크
def get_check_point():
    df = pyupbit.get_ohlcv("KRW-BTC")
    ma5 = df['close'].rolling(window=21).mean()
    last_ma5 = ma5[-2]
    price = pyupbit.get_current_price("KRW-BTC")
    if price > last_ma5:
        return 0.3
    else:
        return 0.7

#해당 코인 매수평균단가 반환
def get_avg_buy_price(coin):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
        time.sleep(0.2)
    return 0

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
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


        print("=======" + str(now) + "======= : " + str(chk_point))
        #print(get_check_point())
        print("Target  : " + str(get_target_price("KRW-BTC", chk_point)))
        print("Current : " + str(get_current_price("KRW-BTC")))
        #print(old_total)
        #print("========================================")
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(1)