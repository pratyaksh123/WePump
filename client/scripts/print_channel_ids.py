import json
from telethon import TelegramClient, events


async def main(telegram_client):
    async for dialog in telegram_client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)


def channel_id(data):
    telegram_App_id = data["telegram_App_id"]
    telegram_api_hash = data["telegram_api_hash"]
    telegram_client = TelegramClient(
        "anon-2", telegram_App_id, telegram_api_hash)

    with telegram_client:
        telegram_client.loop.run_until_complete(main(telegram_client))
