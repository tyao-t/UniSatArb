# # from bitcoinlib.wallets import Wallet, wallet_delete_if_exists
# # if wallet_delete_if_exists('unisat'): pass

# # wif = "L2AYnT4WgW61Ldrcm8oJxHKWxa9YVo6nijQjCxDycARXFejJTkWw"
# # w = Wallet.create('unisat', wif)
# # print(w)
# # print(w.as_json())

# # Copyright (C) 2018-2022 The python-bitcoin-utils developers
# #
# # This file is part of python-bitcoin-utils
# #
# # It is subject to the license terms in the LICENSE file found in the top-level
# # directory of this distribution.
# #
# # No part of python-bitcoin-utils, including this file, may be copied,
# # modified, propagated, or distributed except according to the terms contained
# # in the LICENSE file.

# from bitcoinutils.setup import setup
# from bitcoinutils.script import Script
# from bitcoinutils.keys import P2trAddress, PrivateKey, PublicKey

# def main():
#     # always remember to setup the network
#     setup('mainnet')

#     # could also instantiate from existing WIF key
#     priv = PrivateKey.from_wif('L2AYnT4WgW61Ldrcm8oJxHKWxa9YVo6nijQjCxDycARXFejJTkWw')

#     # compressed is the default
#     print("\nPrivate key WIF:", priv.to_wif())

#     # get the public key
#     pub = priv.get_public_key()
#     print("Public key as usual:", pub.to_hex())

#     # get address from public key
#     address = pub.get_taproot_address()

#     # print the address and hash - default is compressed address
#     print("Address:", address.to_string())

# if __name__ == "__main__":
#     main()
import requests
import json

url = "https://blockchain.info/unspent?active=bc1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqtpxddu"

payload = json.dumps({
  "method": "bb_getaddress",
  "params": [
    "bc1p72h09wplu60qdxyr8q3ftgdhga7jxnjhdz08qs4u9we9q3lzmqmqa4yzj6",
    {
      "page": 1,
      "size": 1000,
      "fromHeight": 0,
      "details": "txids"
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}

res = requests.request("GET", url)

print(res.json()["unspent_outputs"][0])


