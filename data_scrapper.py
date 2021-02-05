from binance.client import Client
from binance.websockets import BinanceSocketManager
import json

api_key = 'fFeGQosVGZyw76wCqXArlmZX5Vw9Ymp55T3VkzqB0zy911EZVysJq3DJAzvPSinG'
secret = 'EZpqVKJLZbWX0nXGP92EjVhHtcQL6GjyUzZlqwnCNmxwg7k43mUAyIBErPjvHmDC'

client = Client(api_key, secret)
bm = BinanceSocketManager(client)


def process_message(msg):
    with open('./data.json', 'a') as file:
        for i in msg:
            json.dump(i, file, indent=4)


conn_key = bm.start_ticker_socket(process_message)
bm.start()
