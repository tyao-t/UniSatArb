#!/usr/bin/python3

import requests
import json
from time import sleep
url = "https://open-api.unisat.io/v2/market/brc20/auction/create_bid"

data = {
    "auctionId": "opjaolhu9smfoc7umvu8enyquqy5d1t3",
    "bidPrice": 5027191,
    "address": "bc1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqtpxddu",
    "pubkey": "03f7c249c258cf0257917cae0d6befa16dcba8a3806707fbfd1322d83361be901c",
}
# from threading import Thread

# data to pass into post request
# myobj = {
#     "filter": {
#         "nftType": "brc20",
#         "tick": "biso",
#         "isEnd": "false",
#         "nftConfirm": "true",
#     },
#     "sort": {
#         'unitPrice':1
#     },
#     "start": 0,
#     "limit": 99,
# }

# data = {"filter":{"nftType":"brc20","tick":"ordi"},"sort":{},"start":0,"limit":2}
    
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 84aadbbd4b03e64879dae6a285b17a58cc31ccaa0a0eceb2e3bce2abfb3a6c06"
}

res = requests.post(url, json=data, headers=headers)
print(res.status_code)
print(res.json())
# print(res.status_code)

# nft_list = res.json()["data"]["list"]
# print(nft_list[0])
# print(nft_list[1])

# symbol = "ordi"
# ss = symbol.upper()
# host = "https://api.gateio.ws"
# prefix = "/api/v4"
# headers = {"Accept": "application/json", "Content-Type": "application/json"}
# url = "/spot/order_book"
# query_param = "currency_pair={}_USDT&limit=150".format(ss)
# response = requests.request(
#     "GET", host + prefix + url + "?" + query_param, headers=headers
# )

# print(type(response.text))

