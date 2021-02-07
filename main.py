import json
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from telethon import TelegramClient, events
from extract_coin import extract
import time
import re

with open("./config.json") as f:
    data = json.load(f)

api_key = data["apiKey"]
api_secret = data["secret"]
telegram_App_id = data["telegram_App_id"]
telegram_api_hash = data["telegram_api_hash"]
channel_id = data["channel_id"]
quoteOrderQty = data["BtcToSpend"]
percent_change = data["percentChange"]
client = Client(api_key, api_secret)
telegram_client = TelegramClient("anon", telegram_App_id, telegram_api_hash)
sell_time = 20


def Average(lst):
    return sum(lst) / len(lst)


def countdown(t, symbol):
    while t:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

    print("Triggering Limit Sell order !")


def calculate_target_price(price):
    final_price = price + ((percent_change / 100) * price)
    return final_price


def limit_sell(symbol, quantity, price):
    order_sell = client.order_limit_sell(
        symbol=symbol, quantity=quantity, price=f"{price}"
    )
    return order_sell


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


@telegram_client.on(events.NewMessage)
async def my_event_handler(event):
    chat_id = event.chat_id
    if chat_id == channel_id:
        coin_symbol = (extract(event.raw_text) + "BTC").upper()
        if not re.match("^[A-Z0-9-_.]{1,20}$", coin_symbol):
            print("Failed to detect coin, enter manually")
            coin_symbol = (input() + "BTC").upper()
        print(f"Coin to pump detected - {coin_symbol}")
        order_status = create_market_order(coin_symbol)
        price_brought_list = []
        quantity_brought = 0
        if order_status:
            for j in order_status["fills"]:
                price_brought_list.append(float(j["price"]))
            quantity_brought = float(order_status["executedQty"])
            price_brought = Average(price_brought_list)
        price_to_sell = calculate_target_price(price_brought)
        print(quantity_brought)
        print(f"Buying process complete ! price brought - {price_brought}")
        countdown(sell_time, coin_symbol)
        sell_order = limit_sell(coin_symbol, quantity_brought, price_to_sell)
        print(sell_order)
        await telegram_client.disconnect()


telegram_client.start()
telegram_client.run_until_disconnected()
