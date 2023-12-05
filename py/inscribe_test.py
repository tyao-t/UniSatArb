#!/usr/bin/python3

import requests
import json
from time import sleep
url = "https://open-api.unisat.io/v1/inscribe/order/brc20/transfer"

# from threading import Thread

# data to pass into post request
myobj = {
  "receiveAddress": "bc1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqtpxddu",
  "feeRate": 10,
  "outputValue": 546,
  "brc20Ticker": "drac",
  "brc20Amount": "100"
}

# data = {"filter":{"nftType":"brc20","tick":"ordi"},"sort":{},"start":0,"limit":2}
    
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 84aadbbd4b03e64879dae6a285b17a58cc31ccaa0a0eceb2e3bce2abfb3a6c06"
}

res = requests.post(url, json=myobj, headers=headers)

print(res.status_code)
print(res.text)