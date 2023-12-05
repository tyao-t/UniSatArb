import requests
# from multiprocessing import Process, Manager, Lock
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait
import json
import time
from datetime import datetime, timedelta
import threading
import time
import redis
import sqlite3
import atexit
import signal
import sys

# connect to redis server with port = 6379
r = redis.Redis(host='localhost', port=6379)

# list of BRC-20 tokens that we are monitoring
# list of 11 tokens currently
# symbol_Ls = ['ordi']
symbol_Ls = ['arks','biop','ordi','vmpx','majo','biso','trac','noot','drac','nals','meme']
poll_interval = 2 # Every _ seconds

def perr(msg):
    print(f"Error: {msg}", file=sys.stderr)

class SlackNotice:
    def __init__(self):
        # self.webhook = "https://hooks.slack.com/services/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"
        self.webhook = "https://hooks.slack.com/services/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"

    # send alert to slack channel
    def sendSlack(self, msg):
        payload = {"text": msg}
        return requests.post(self.webhook, json.dumps(payload))
    
    # send alert when process is started
    def startProcessMsg(self, processName):
        msg = "Process for: " + processName + " started by user"
        return self.sendSlack(msg)
    
    # notification to slack in event of termination
    def killFunction(self, processName, error=""):
        msg = 'Process for: ' + processName + " is terminated" + "\n" + "Error: " + error
        perr(msg)
        self.sendSlack(msg)

class GateIO:
    def __init__(self):
        self.processName = "gateIO"
        self.slackChannel = SlackNotice()
    
    # call gateIO api to retrieve orderbook
    # update redis with latest listings
    def gateIO_redis(self, symbol):

        ss = symbol.upper()
        host = "https://api.gateio.ws"
        prefix = "/api/v4"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        url = "/spot/order_book"
        query_param = "currency_pair={}_USDT&limit=150".format(ss)
        try:
            response = requests.request(
                "GET", host + prefix + url + "?" + query_param, headers=headers
            )
        except Exception as error:
            self.slackChannel.sendSlack(error)
            perr(error)
            return
        key = symbol + "_GateIO"
        if 'bids' in response.json():
            bids = response.json()['bids']
            r.json().set(key, '$', bids)
            # print(key)
            # print(r.json().get(key))
            # print("\n")
        return 

    # return most recent listings of Gateio on redis
    def get_GateIORedis(self, symbol):
        key = symbol + "_GateIO"
        res = r.json().get(key)
        return res

class Unisat:
    def __init__(self):
        self.slackChannel = SlackNotice()
        self.processName = "Unisat"
        # res = r.json().get("ordi_Unisat")
        # print(res)

    def InitUnisatListings(self, symbol):

        # get most update set of listings on Unisat marketplace
        # update in redis
        listings = self.retrieveUnitsatBRC(symbol)
        key = symbol + "_Unisat"
        r.json().set(key, '$', listings)
        # print(key)
        # print(r.json().get(key))
        # print("\n")
        return

    # get most recent unisat listing on redis
    def getUnisat(self, symbol):
        key = symbol + "_Unisat"
        res = r.json().get(key)
        return res

    # api call to get BRC20 listing of token on unisat marketplace
    def retrieveUnitsatBRC(self,symbol):
        url = "https://open-api.unisat.io/v2/market/brc20/auction/list"

        # data to pass into post request
        myobj = {
            "filter": {
                "nftType": "brc20",
                "tick": symbol,
                "isEnd": "false",
                "nftConfirm": "true"
            },
            "sort": {
                'unitPrice':1
            },
            "start": 0,
            "limit": 99,
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer 84aadbbd4b03e64879dae6a285b17a58cc31ccaa0a0eceb2e3bce2abfb3a6c06"
        }

        res = requests.post(url, json=myobj, headers=headers)
        try:
            rj = res.json()
        except Exception as error:
            perr(error)
            perr(res)
            return

        #print(res.status_code)

        # return error if array is empty
        if len(rj['data']['list']) == 0:
            msg = "error with retrieving from unisat, list array is 0."
            self.slackChannel.sendSlack(msg)
            return 
        
        # return listings as a dictionary
        # key is unique inscription ID for each listing
        masterD = {}
        for i in rj['data']['list']:
            if i['inscriptionId'] not in masterD:
                masterD[i['inscriptionId']] = i

        return masterD


    
class ArbOpp:
    def __init__(self):
        self.slackChannel = SlackNotice()
        self.processName = "ArbOppScanning"

    # using OKX exchange rate for BTC-USDT spot
    # get btc -> usdt conversion
    def get_usdtFromBTC(self):
        instID = "BTC-USDT"

        url = "http://www.okx.com/api/v5/market/ticker?instId=" + instID

        headers = {
            "accept": "application/json",
        }
        try:
            response = requests.get(url, headers=headers)
        except Exception as error:
            perr(error)
            return None
        res = response.json()
        if len(res['data']) == 0:
            perr("error with btcUSDT retrieveal")
            return None
        return float(res['data'][0]['last'])

    # calculate potential profits from price difference between gateio orderbook & unisat listings
    # account for 0.8% service fee on unisat buy
    # account for 0.2% taker/maker fee on gateio (lowest tier)
    def calc_potentialProfits(self, gateio, unisat, btcUSDT):

        unisatKeys = list(unisat.keys())
        buyPtr = 0
        sellPtr = 0
        soldSize = 0
        rev = 0
        exp = 0
        done = False
        unitsTransact = 0
        profit = 0

        unisatFee = 0.8/100
        gateioFee = 0.2/100

        while True:
            curBuy = unisat[unisatKeys[buyPtr]]
            curBuyUnits = curBuy['amount']
            curBuyPrice = curBuy['unitPrice'] * btcUSDT / 1e8 * (1 + unisatFee)
            volBuy = float(curBuy['price']) * btcUSDT / 1e8

            tempGatePtr = sellPtr
            curRev = 0
            while curBuyUnits > 0:
                if tempGatePtr > len(gateio) - 1:
                    done = True
                    break
                curSell = gateio[tempGatePtr]
                
                curSellPrice, curSellSize = float(curSell[0]), float(curSell[1]) - soldSize
                curSellPrice = curSellPrice * (1 - gateioFee)
                if curSellPrice <= curBuyPrice:
                    done = True
                    break
                toSell = min(curSellSize, curBuyUnits)
                unitsTransact += toSell
                curRev += curSellPrice * toSell
                curBuyUnits -= toSell
                if curSellSize == toSell:
                    tempGatePtr += 1
                else:
                    soldSize = toSell
            if done:
                break
            
            if curBuyUnits == 0:
                sellPtr = tempGatePtr
                exp += volBuy
                rev += curRev
                
            buyPtr += 1
            profit = rev - exp

        if profit <= 0:
            return profit, 0, 0

        return profit, unitsTransact, profit/exp*100

    def arbOpp(self, symbol, ts, btcUSDT):
        unisatInstance = Unisat()
        gateioInstance = GateIO()
        unisat = unisatInstance.getUnisat(symbol)
        gateio = gateioInstance.get_GateIORedis(symbol)
        if unisat is None or gateio is None:
            return 
        cheapestUnisat = unisat[list(unisat.keys())[0]]['unitPrice'] * btcUSDT / 1e8
        # print(unisat[list(unisat.keys())[0]]['unitPrice'])

        unisatFee = 0.8/100
        gateioFee = 0.2/100

        # taking into account fixed fees for gateio & unisat
        if (1-gateioFee) * float(gateio[0][0]) - (1+unisatFee) * cheapestUnisat > 0:
            potentialProfit, units, percProfit = self.calc_potentialProfits(gateio, unisat, btcUSDT)
            if (potentialProfit <= 0): 
                print("No profit, inner")
                return
            msg = "Timestamp: "+ts +", Token: "+symbol+ ", Highest GateIO bid: "+gateio[0][0] + ", Lowest Unisat ask: "+ str(cheapestUnisat) + "\n" + "Potential profit: " + str(potentialProfit) + ", Units transacted: "+ str(units) + ", % profit: " + str(percProfit)
            with open("logs/profit.log", "a") as lf:
                lf.write(msg + "\n")
            self.slackChannel.sendSlack(msg)
        else:
            log_path = f"logs/{symbol}.log"
            with open(log_path, "a") as f:
                f.write("No profit, outer\n")
                f.write(f"Time = {ts}\n")
                f.write(symbol + "\n")
                f.write("Gateio = " + str(gateio[0][0]) + "\n")
                f.write("Unisat = " + str(cheapestUnisat) + "\n")
                # print(1-gateioFee)
                # print(1+unisatFee)
                # print((1-gateioFee) * float(gateio[0][0]))
                # print((1+unisatFee) * cheapestUnisat)
                f.write("\n")
            return
        
        key = symbol + "_arbLog"

        # create connection to SqLite Database
        connection = sqlite3.connect('./SqLiteDB/{}.db'.format(key))
        cursor = connection.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS ArbLog (
                timestamp TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # save to corresponding table in ArbLog db
        rawValue = json.dumps({"unisat":unisat, "gateio": gateio, "profit": potentialProfit, "units": units, "percentage": percProfit})
        try:
            cursor.execute(f"INSERT OR REPLACE INTO ArbLog (timestamp, value) VALUES (?, ?)", (ts, rawValue))
        except Exception as error:
            self.slackChannel.sendSlack(error)
        connection.commit()
        connection.close()

        return 