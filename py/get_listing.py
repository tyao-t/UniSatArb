#!/usr/bin/python3

import requests
import json
from time import sleep
url = "https://open-api.unisat.io/v2/market/brc20/auction/list"

# data to pass into post request
myobj = {
    "filter": {
        "nftType": "brc20",
        "tick": "ordi",
        "isEnd": "false",
        "nftConfirm": "true",
    },
    "sort": {
        'unitPrice':1
    },
    "start": 0,
    "limit": 99,
}

# data = {"filter":{"nftType":"brc20","tick":"ordi"},"sort":{},"start":0,"limit":2}
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 84aadbbd4b03e64879dae6a285b17a58cc31ccaa0a0eceb2e3bce2abfb3a6c06"
}

res = requests.post(url, json=myobj, headers=headers)
print(res.status_code)

nft_list = res.json()["data"]["list"]
print(nft_list[0])
print(nft_list[1])

