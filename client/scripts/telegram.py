from telethon import TelegramClient, events
from utils.extract_coin import extract
import re
from termcolor import colored


def Telegram(data):
    telegram_App_id = data["telegram_App_id"]
    telegram_api_hash = data["telegram_api_hash"]
    channel_id = data["Test_channel_id"]

    telegram_client = TelegramClient("anon-3", telegram_App_id, telegram_api_hash)

    @telegram_client.on(events.NewMessage)
    async def my_event_handler(event):
        if event.chat_id == channel_id:
            coin_symbol = (extract(event.raw_text) + "BTC").upper()
            if not re.match("^[A-Z0-9-_.]{1,20}$", coin_symbol):
                print(colored("Failed to detect coin, enter manually !", "yellow"))

                coin_symbol = (input() + "BTC").upper()
        print(f"Coin to pump detected - {colored(coin_symbol,'green')}")

    telegram_client.start()
    print("Listening For messages (press Ctrl+c to exit) !")
    telegram_client.run_until_disconnected()
