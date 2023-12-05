#!/usr/bin/python3

import requests
import json
from time import sleep
url = "https://open-api.unisat.io/v2/market/brc20/auction/create_bid"

data = {
    "auctionId": "fwd14oi6badkn68a3pfajmvtmpdfx383",
    "bidPrice": 1415501,
    "address": "bc1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqtpxddu",
    "pubkey": "03f7c249c258cf0257917cae0d6befa16dcba8a3806707fbfd1322d83361be901c",
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 84aadbbd4b03e64879dae6a285b17a58cc31ccaa0a0eceb2e3bce2abfb3a6c06"
}

res = requests.post(url, json=data, headers=headers)
print(res.status_code)
print(res.json())
