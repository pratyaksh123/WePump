from binance.client import Client
import json


def Check_balance(data):
    api_key = data["apiKey"]
    api_secret = data["secret"]
    client = Client(api_key, api_secret)
    print("Type Coin/Asset Name")
    asset = input()
    balance = client.get_asset_balance(asset)
    json_output = json.dumps(balance, indent=4)
    return json_output