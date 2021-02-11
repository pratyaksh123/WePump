from binance.client import Client
from binance.enums import *
from utils.get_mac_id import get_mac
from datetime import datetime
import api.index as api
from binance.exceptions import BinanceAPIException, BinanceOrderUnknownSymbolException
import json
import time
import scripts.telegram as tel
from utils.extract_coin import extract
import re
from telethon import TelegramClient, events

with open("./config.json") as f:
    data = json.load(f)


api_key = data["apiKey"]
api_secret = data["secret"]
telegram_App_id = data["telegram_App_id"]
telegram_api_hash = data["telegram_api_hash"]
channel_id = data["channel_id"]
Test_channel_id = data["Test_channel_id"]
quoteOrderQty = data["BtcToSpend"]
take_profit = str(data["takeProfit"]).lower()
takeProfitAt = data["takeProfitAt"]
takeProfitLimit = data["takeProfitLimit"]
stopLoss = str(data["stopLoss"]).lower()
stopLossAt = data["stopLossAt"]
stopLossLimit = data["stopLossLimit"]
sell_time = data["Timeout"]
telegram_App_id = data["telegram_App_id"]
telegram_api_hash = data["telegram_api_hash"]
channel_id = data["channel_id"]

client = Client(api_key, api_secret)
telegram_client = TelegramClient("anon", telegram_App_id, telegram_api_hash)
coin_symbol = ''
coin_extract_status = False


def update_precision(quantity):
    precision = 5
    amt_str = "{:0.0{}f}".format(float(quantity), precision)
    return amt_str


def set_status_to_expire(mac_add):
    res = api.update_user_status(mac_add, "Expired")
    if res != "Success":
        print("Fatal Error, Please contact support")


def create_market_order(symbol):
    quantity = quoteOrderQty
    try:
        order = client.order_market_buy(
            symbol=symbol,
            quoteOrderQty=update_precision(quantity),
        )
        return order
    except BinanceAPIException as e:
        print(f"Market Buy Error - {e}")


def create_market_order_sell(symbol, quantity):
    try:
        order = client.order_market_sell(
            symbol=symbol,
            quantity=quantity,
        )
        return order
    except BinanceAPIException as e:
        print(f"Market Sell Error - {e}")


def Average(lst):
    return sum(lst) / len(lst)


def calculate_target_price(price, percent_change, loss):
    if loss:
        final_price = price - ((percent_change / 100) * price)
    else:
        final_price = price + ((percent_change / 100) * price)
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
            timeInForce=TIME_IN_FORCE_GTC,
        )
        return order_take_ptf
    except BinanceAPIException as e:
        print(f"Take Profit Error - {e}")


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
            timeInForce=TIME_IN_FORCE_GTC,
        )
        return order_take_loss
    except BinanceAPIException as e:
        print(f"Stop Loss Error - {e}")


def start_main(symbol, Trial):
    market_order = create_market_order(symbol)
    price_brought_list = []
    tp_order_id, sp_order_id = None, None
    Tp_triggered = False
    sp_triggered = False
    if market_order:
        for i in market_order["fills"]:
            price_brought_list.append(float(i["price"]))
        quantity_brought = market_order["executedQty"]
        price_brought = Average(price_brought_list)
        print(
            f"Market Buy successful at price {price_brought} and quantity brought - {quantity_brought}"
        )
        if take_profit == "true":
            take_profit_order = setup_take_profit(
                price_brought, quantity_brought, symbol
            )
            if take_profit_order:
                print(f"Take Profit successfully set!")
                tp_order_id = take_profit_order["orderId"]
        if stopLoss == "true":
            stop_loss_order = setup_stop_loss(
                price_brought, quantity_brought, symbol)
            if stop_loss_order:
                print(f"Stop Loss successfully set !")
                sp_order_id = stop_loss_order["orderId"]
        if sell_time > 0:
            t = sell_time
            while t:
                mins, secs = divmod(t, 60)
                timer = "{:02d}:{:02d}".format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                t -= 1
            if tp_order_id:
                order_status_tp = client.get_order(
                    symbol=symbol, orderId=tp_order_id)
                if order_status_tp["status"] == "TRADE":
                    Tp_triggered = True
            elif sp_order_id:
                order_status_sp = client.get_order(
                    symbol=symbol, orderId=sp_order_id)
                if order_status_sp["status"] == "TRADE":
                    sp_triggered = True

            if not Tp_triggered and not sp_triggered:
                # Cancel open orders first or some coins will be locked
                if tp_order_id:
                    client.cancel_order(symbol=symbol, orderId=tp_order_id)
                if sp_order_id:
                    client.cancel_order(symbol=symbol, orderId=sp_order_id)
                print(
                    "None of Take profit or stop loss were triggered ! Selling ASAP !"
                )
                order = create_market_order_sell(
                    symbol, update_precision(quantity_brought)
                )
                if order:
                    print("Market sell successful !")
    if Trial:
        mac_address = get_mac()
        if market_order and market_order["status"] == "FILLED":
            set_status_to_expire(mac_address)


def pump_take_profit(data, Trial):
    print("Do you want to use telegram capture mode(Y/N) ?")
    telegram_mode = input()
    global coin_symbol, coin_extract_status
    if telegram_mode == "N" or telegram_mode == "n":
        print("Enter Coin name")
        x = input()
        symbol = x.upper() + "BTC"
        start_main(symbol, Trial)
    elif telegram_mode == "Y" or telegram_mode == "y":

        @telegram_client.on(events.NewMessage)
        async def my_event_handler(event):
            chat_id = event.chat_id
            if chat_id == channel_id:
                global coin_symbol
                global coin_extract_status
                coin_symbol = (extract(event.raw_text) + "BTC").upper()
                if re.match("^[A-Z0-9-_.]{1,20}$", coin_symbol):
                    print(f"Coin to pump detected - {coin_symbol}")
                    coin_extract_status = True

                await telegram_client.disconnect()

        telegram_client.start()
        print("Listening For messages (press Ctrl+c to exit) !")
        telegram_client.run_until_disconnected()
        if(not coin_extract_status):
            print("Failed to detect coin, enter manually")
            coin_symbol = (input() + "BTC").upper()
        if(coin_symbol != ''):
            start_main(coin_symbol, Trial)
