from binance.client import Client
from binance.enums import *
from datetime import datetime
from binance.exceptions import BinanceAPIException, BinanceOrderUnknownSymbolException
import json
import time

with open('./config.json') as f:
    data = json.load(f)


api_key = data['apiKey']
api_secret = data['secret']
quoteOrderQty = data['BtcToSpend']
take_profit = data['takeProfit']
takeProfitAt = data['takeProfitAt']
takeProfitLimit = data['takeProfitLimit']
stopLoss = data['stopLoss']
stopLossAt = data['stopLossAt']
stopLossLimit = data['stopLossLimit']
sell_time = data['Timeout']


client = Client(api_key, api_secret)


def create_market_order(symbol):
    quantity = quoteOrderQty
    try:
        order = client.order_market_buy(
            symbol=symbol,
            quoteOrderQty=quantity,
        )
        return order
    except BinanceAPIException as e:
        print(e.message)


def create_market_order_sell(symbol, quantity):
    try:
        order = client.order_market_sell(
            symbol=symbol,
            quantity=quantity,
        )
        return order
    except BinanceAPIException as e:
        print(e.message)


def Average(lst):
    return sum(lst) / len(lst)


def update_precision(quantity):
    precision = 5
    amt_str = "{:0.0{}f}".format(float(quantity), precision)
    return amt_str


def calculate_target_price(price, percent_change, loss):
    if(loss):
        final_price = price-((percent_change/100)*price)
    else:
        final_price = price+((percent_change/100)*price)
    return final_price


def setup_take_profit(price_brought, quantity_brought, symbol):
    price = calculate_target_price(price_brought, takeProfitLimit, False)
    stopPrice = calculate_target_price(price_brought, takeProfitAt, False)
    try:
        order_take_ptf = client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
            quantity=update_precision(quantity_brought),
            price=update_precision(price),
            stopPrice=update_precision(stopPrice),
            timeInForce=TIME_IN_FORCE_GTC
        )
        return order_take_ptf
    except BinanceAPIException as e:
        print(e.message)


def setup_stop_loss(price_brought, quantity_brought, symbol):
    price = calculate_target_price(price_brought, stopLossLimit, True)
    stopPrice = calculate_target_price(price_brought, stopLossAt, True)
    try:
        order_take_loss = client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            quantity=update_precision(quantity_brought),
            price=update_precision(price),
            stopPrice=update_precision(stopPrice),
            timeInForce=TIME_IN_FORCE_GTC
        )
        return order_take_loss
    except BinanceAPIException as e:
        print(e.message)


def pump_take_profit(data):
    # display settings then
    print('Enter Coin name')
    x = input()
    symbol = x.upper()+'BTC'
    market_order = create_market_order(symbol)
    price_brought_list = []
    tp_order_id, sp_order_id = None, None
    Tp_triggered = False
    sp_triggered = False
    if(market_order):
        for i in market_order['fills']:
            price_brought_list.append(float(i['price']))
        quantity_brought = market_order['executedQty']
        price_brought = Average(price_brought_list)
        print(
            f'Market Buy successful at price {price_brought} and quantity brought - {quantity_brought}')
        if(take_profit):
            take_profit_order = setup_take_profit(
                price_brought, quantity_brought, symbol)
            if(take_profit_order):
                print(
                    f'Take Profit successfully set!')
                tp_order_id = take_profit_order['orderId']
        if(stopLoss):
            stop_loss_order = setup_stop_loss(
                price_brought, quantity_brought, symbol)
            if(stop_loss_order):
                print(
                    f'Stop Loss successfully set !')
                sp_order_id = stop_loss_order['orderId']
        if(sell_time > 0):
            t = sell_time
            while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                t -= 1
            if(tp_order_id):
                order_status_tp = client.get_order(
                    symbol=symbol,
                    orderId=tp_order_id)
                if(order_status_tp['status'] == 'TRADE'):
                    Tp_triggered = True
            elif(sp_order_id):
                order_status_sp = client.get_order(
                    symbol=symbol,
                    orderId=sp_order_id)
                if(order_status_sp['status'] == 'TRADE'):
                    sp_triggered = True

            if(not Tp_triggered and not sp_triggered):
                print('None of Take profit or stop loss were triggered ! Selling ASAP !')
                order = create_market_order_sell(symbol, quantity_brought)
                if(order):
                    print('market sell sucessful')
