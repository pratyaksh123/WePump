from telethon import TelegramClient, events
from utils.extract_coin import extract
import re


def Telegram(data, testMode):
    telegram_App_id = data["telegram_App_id"]
    telegram_api_hash = data["telegram_api_hash"]
    if testMode:
        channel_id = data["Test_channel_id"]
    else:
        channel_id = data["channel_id"]

    telegram_client = TelegramClient(
        "anon-3", telegram_App_id, telegram_api_hash)

    @telegram_client.on(events.NewMessage)
    async def my_event_handler(event):
        chat_id = event.chat_id
        if chat_id == channel_id:
            coin_symbol = (extract(event.raw_text) + "BTC").upper()
            if not re.match("^[A-Z0-9-_.]{1,20}$", coin_symbol):
                print("Failed to detect coin, enter manually")
                coin_symbol = (input() + "BTC").upper()
        print(f"Coin to pump detected - {coin_symbol}")

    telegram_client.start()
    print("Listening For messages (press Ctrl+c to exit) !")
    telegram_client.run_until_disconnected()
