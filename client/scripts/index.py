from binance.client import Client
from binance.enums import *
from utils.get_mac_id import get_mac
from datetime import datetime
import api.index as api
from binance.exceptions import BinanceAPIException, BinanceOrderUnknownSymbolException
import scripts.telegram as tel
from utils.extract_coin import extract
from termcolor import colored
from telethon import TelegramClient, events
import json
import time
import re
import math


class Bot:
    def __init__(self, data, isTrial):
        self.api_key = data["apiKey"]
        self.api_secret = data["secret"]
        self.useTelegramCapture = str(data['useTelegramCapture']).lower()
        self.quoteOrderQty = data["BtcToSpend"]
        self.take_profit = str(data["takeProfit"]).lower()
        self.takeProfitAt = data["takeProfitAt"]
        self.takeProfitLimit = data["takeProfitLimit"]
        self.stopLoss = str(data["stopLoss"]).lower()
        self.stopLossAt = data["stopLossAt"]
        self.stopLossLimit = data["stopLossLimit"]
        self.timeout = data["Timeout"]
        self.client = Client(self.api_key, self.api_secret)
        self.isTrial = isTrial
        self.tp_order_id, self.sl_order_id, self.oco_order = False, False, False
        self.tp_triggered, self.sl_triggered = False, False
        if(self.useTelegramCapture == 'true'):
            self.initialise_telegram_client(data)

    def initialise_telegram_client(self, data):
        self.telegram_App_id = data["telegram_App_id"]
        self.telegram_api_hash = data["telegram_api_hash"]
        self.channel_id = data["channel_id"]
        self.Test_channel_id = data["Test_channel_id"]
        self.coin_extract_status = False
        self.coin_symbol = ''
        self.telegram_client = TelegramClient(
            "anon", self.telegram_App_id, self.telegram_api_hash)

    def create_market_order(self):
        try:
            order = self.client.order_market_buy(
                symbol=self.coin_symbol,
                quoteOrderQty=self.quoteOrderQty,
            )
            return order
        except BinanceAPIException as e:
            print(colored(f"Market Buy Error - {e}", 'red'))

    def create_market_order_sell(self):
        try:
            order = self.client.order_market_sell(
                symbol=self.coin_symbol,
                quantity=self.quantity_brought,
            )
            return order
        except BinanceAPIException as e:
            print(colored(f"Market Sell Error - {e}", 'red'))

    def float_precision(self, f, n):
        n = int(math.log10(1 / float(n)))
        f = math.floor(float(f) * 10 ** n) / 10 ** n
        f = "{:0.0{}f}".format(float(f), n)
        return str(int(f)) if int(n) == 0 else f

    def get_price(self):
        price = None
        tickers = self.client.get_all_tickers()
        for ticker in tickers:
            if ticker['symbol'] == self.coin_symbol:
                price = float(ticker['price'])
        return price

    def get_tick_and_step_size(self):
        try:
            tick_size = None
            step_size = None
            symbol_info = self.client.get_symbol_info(self.coin_symbol)
            for filt in symbol_info['filters']:
                if filt['filterType'] == 'PRICE_FILTER':
                    tick_size = float(filt['tickSize'])
                elif filt['filterType'] == 'LOT_SIZE':
                    step_size = float(filt['stepSize'])
            return tick_size, step_size
        except TypeError as e:
            print(colored(f'Wrong Coin Name Entered - {e}', 'red'))

    def get_asset_info(self):
        try:
            self.tick_size, self.step_size = self.get_tick_and_step_size()
        except TypeError as e:
            print(colored(f'Wrong Coin Name Entered - {e}', 'red'))

    def Average(self, lst):
        return sum(lst) / len(lst)

    def calculate_target_price(self, price, percent_change, loss):
        if loss:
            final_price = price - ((percent_change / 100) * price)
        else:
            final_price = price + ((percent_change / 100) * price)
        return final_price

    def set_take_profit(self):
        take_profit_price = self.calculate_target_price(
            self.price_brought, self.takeProfitLimit, False)
        stop_price = self.calculate_target_price(
            self.price_brought, self.takeProfitAt, False)
        price_formatted = self.float_precision(
            take_profit_price, self.tick_size)
        stop_price_formatted = self.float_precision(stop_price, self.tick_size)
        try:
            order_take_ptf = self.client.create_order(
                symbol=self.coin_symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
                quantity=self.quantity_brought,
                price=price_formatted,
                stopPrice=stop_price_formatted,
                timeInForce=TIME_IN_FORCE_GTC,
            )
            return order_take_ptf
        except BinanceAPIException as e:
            print(colored(f"Take Profit Error - {e}", 'red'))

    def set_stop_loss(self):
        stop_loss_price = self.calculate_target_price(
            self.price_brought, self.stopLossLimit, True)
        stop_price = self.calculate_target_price(
            self.price_brought, self.stopLossAt, True)
        price_formatted = self.float_precision(
            stop_loss_price, self.tick_size)
        stop_price_formatted = self.float_precision(stop_price, self.tick_size)
        try:
            order_stop_loss = self.client.create_order(
                symbol=self.coin_symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_STOP_LOSS_LIMIT,
                quantity=self.quantity_brought,
                price=price_formatted,
                stopPrice=stop_price_formatted,
                timeInForce=TIME_IN_FORCE_GTC,
            )
            return order_stop_loss
        except BinanceAPIException as e:
            print(colored(f"Stop Loss Error - {e}", 'red'))

    def set_oco_order(self):
        take_profit_price = self.float_precision(self.calculate_target_price(
            self.price_brought, self.takeProfitLimit, False), self.tick_size)
        stop_loss_price = self.float_precision(self.calculate_target_price(
            self.price_brought, self.stopLossLimit, True), self.tick_size)
        stop_price = self.float_precision(self.calculate_target_price(
            self.price_brought, self.stopLossAt, True), self.tick_size)
        try:
            oco_order = self.client.create_oco_order(
                symbol=self.coin_symbol,
                side=SIDE_SELL,
                stopLimitTimeInForce=TIME_IN_FORCE_GTC,
                quantity=self.quantity_brought,
                stopPrice=stop_price,
                stopLimitPrice=stop_loss_price,
                price=take_profit_price
            )
            return oco_order
        except BinanceAPIException as e:
            print(colored(f"OCO order Error - {e}", 'red'))

    def start(self):
        self.coin_currency = self.coin_symbol[0:len(self.coin_symbol)-3]
        self.get_asset_info()
        market_order = self.create_market_order()
        price_brought_list, commission = [], 0
        if market_order:
            for i in market_order["fills"]:
                price_brought_list.append(float(i["price"]))
                if(i['commissionAsset'] == self.coin_currency):
                    commission += float(i['commission'])
            self.quantity_brought = float(self.float_precision(
                float(market_order["executedQty"])-commission, self.step_size))
            self.price_brought = self.Average(price_brought_list)

            print(
                f"Market Buy Successful at price {colored(self.price_brought,'green')} and quantity brought - {colored(self.quantity_brought,'green')}"
            )
            if(self.take_profit == 'true' and self.stopLoss != 'true'):
                take_profit_order = self.set_take_profit()
                if(take_profit_order):
                    print(colored(f"Take Profit Successfully set!", 'green'))
                    self.tp_order_id = take_profit_order["orderId"]
            if(self.stopLoss == 'true' and self.take_profit != 'true'):
                stop_loss_order = self.set_stop_loss()
                if(stop_loss_order):
                    print(colored(f"Stop Loss Successfully set!", 'green'))
                    self.sl_order_id = stop_loss_order['orderId']
            if(self.take_profit == 'true' and self.stopLoss == 'true'):
                self.oco_order = self.set_oco_order()
                if(self.oco_order):
                    print(
                        colored(f"Take Profit and Stop Loss Successfully Set!", 'green'))
            if(self.timeout > 0):
                t = self.timeout
                while t:
                    mins, secs = divmod(t, 60)
                    timer = "{:02d}:{:02d}".format(mins, secs)
                    print(colored(timer, 'yellow'), end="\r")
                    time.sleep(1)
                    t -= 1
                if(self.tp_order_id):
                    try:
                        order_status_tp = self.client.get_order(
                            symbol=self.coin_symbol, orderId=self.tp_order_id)
                        if order_status_tp["status"] == "FILLED":
                            self.tp_triggered = True
                    except BinanceAPIException as e:
                        print(colored(f"Failed to get TP Order - {e}", 'red'))
                elif(self.sl_order_id):
                    try:
                        order_status_sl = self.client.get_order(
                            symbol=self.coin_symbol, orderId=self.sl_order_id)
                        if order_status_sl['status'] == 'FILLED':
                            self.sl_triggered = True
                    except BinanceAPIException as e:
                        print(colored(f"Failed to get SL Order - {e}", 'red'))
                elif(self.oco_order):
                    try:
                        order_status_oco = self.client.get_order(
                            symbol=self.coin_symbol, orderId=self.oco_order['orders'][1]['orderId'])
                        if(order_status_oco['status'] == 'FILLED'):
                            self.tp_triggered = True
                        elif(order_status_oco['status'] == 'EXPIRED'):
                            self.sl_triggered = True
                    except BinanceAPIException as e:
                        print(colored(f"Failed to get OCO Order - {e}", 'red'))
                if(not self.tp_triggered and not self.sl_triggered):
                    if self.tp_order_id:
                        try:
                            self.client.cancel_order(
                                symbol=self.coin_symbol, orderId=self.tp_order_id)
                        except BinanceAPIException as e:
                            print(
                                colored(f"Failed to Cancel TP order - {e}", 'red'))
                    if self.sl_order_id:
                        try:
                            self.client.cancel_order(
                                symbol=self.coin_symbol, orderId=self.sl_order_id)
                        except BinanceAPIException as e:
                            print(
                                colored(f"Failed to Cancel SL order - {e}", 'red'))
                    print(colored(
                        "None of Take Profit or Stop Loss were triggered, Selling ASAP !", 'yellow'))

                    market_sell_order = self.create_market_order_sell()
                    if(market_sell_order and market_sell_order['status'] == 'FILLED'):
                        print(colored("Market Sell Successful !", 'green'))
                    if(market_sell_order and market_sell_order['status'] != 'FILLED'):
                        print(colored(
                            "Market Sell Partially Successfull or Failed , Please check on Binance.com", 'yellow'))
                else:
                    if(self.tp_triggered):
                        print(
                            colored("Congrats, Your Take Profit Order was triggered !", 'green'))
                    if(self.sl_triggered):
                        print(
                            colored("Your Stop Loss Order was triggered !", 'green'))
            if self.isTrial:
                mac_address = get_mac()
                if market_order and market_order['status'] == 'FILLED':
                    self.set_status_to_expire(mac_address)

    def set_status_to_expire(self, mac_add):
        res = api.update_user_status(mac_add, "Expired")
        if res != "Success":
            print(colored("Fatal Error, Please contact support", 'red'))

    def initialise(self):
        if(self.useTelegramCapture == 'true'):
            @ self.telegram_client.on(events.NewMessage)
            async def my_event_handler(event):
                if event.chat_id == self.channel_id:
                    self.coin_symbol = (
                        extract(event.raw_text) + "BTC").upper()
                    if re.match("^[A-Z0-9-_.]{1,20}$", self.coin_symbol):
                        print(
                            f"Coin to pump detected - {colored(self.coin_symbol,'green')}")
                        self.coin_extract_status = True

                    await self.telegram_client.disconnect()

            self.telegram_client.start()
            print("Listening For messages (press Ctrl+c to exit) !")
            self.telegram_client.run_until_disconnected()
            if(not self.coin_extract_status):
                print(colored("Failed to detect coin, enter manually !", 'yellow'))
                self.coin_symbol = (input() + "BTC").upper()
            if(self.coin_symbol != ''):
                self.start()
        else:
            print('Enter Coin name')
            self.coin_symbol = input().upper()+'BTC'
            print(f"Coin Entered - {colored(self.coin_symbol,'green')}")
            self.start()


def main(data, isTrial):
    client = Bot(data, isTrial)
    client.initialise()
