from datetime import datetime

import requests
import json

from db import *
import time
from web3 import Web3
from bs4 import BeautifulSoup

mainnet_provider = "https://mainnet.infura.io/v3/5605598770db449ea039caffced8c302"

web3 = Web3(Web3.HTTPProvider(mainnet_provider))

true = True

factory_abi = [{"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
               {"anonymous": False,
                "inputs": [{"indexed": true, "internalType": "address", "name": "owner", "type": "address"},
                           {"indexed": true, "internalType": "address", "name": "spender", "type": "address"},
                           {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}],
                "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": true, "internalType": "address", "name": "sender", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "amount0", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount1", "type": "uint256"},
        {"indexed": true, "internalType": "address", "name": "to", "type": "address"}], "name": "Burn",
                                                       "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": true, "internalType": "address", "name": "sender", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "amount0", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount1", "type": "uint256"}], "name": "Mint",
                                                                          "type": "event"}, {"anonymous": False,
                                                                                             "inputs": [
                                                                                                 {"indexed": true,
                                                                                                  "internalType": "address",
                                                                                                  "name": "sender",
                                                                                                  "type": "address"},
                                                                                                 {"indexed": False,
                                                                                                  "internalType": "uint256",
                                                                                                  "name": "amount0In",
                                                                                                  "type": "uint256"},
                                                                                                 {"indexed": False,
                                                                                                  "internalType": "uint256",
                                                                                                  "name": "amount1In",
                                                                                                  "type": "uint256"},
                                                                                                 {"indexed": False,
                                                                                                  "internalType": "uint256",
                                                                                                  "name": "amount0Out",
                                                                                                  "type": "uint256"},
                                                                                                 {"indexed": False,
                                                                                                  "internalType": "uint256",
                                                                                                  "name": "amount1Out",
                                                                                                  "type": "uint256"},
                                                                                                 {"indexed": true,
                                                                                                  "internalType": "address",
                                                                                                  "name": "to",
                                                                                                  "type": "address"}],
                                                                                             "name": "Swap",
                                                                                             "type": "event"},
               {"anonymous": False,
                "inputs": [{"indexed": False, "internalType": "uint112", "name": "reserve0", "type": "uint112"},
                           {"indexed": False, "internalType": "uint112", "name": "reserve1", "type": "uint112"}],
                "name": "Sync", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": true, "internalType": "address", "name": "from", "type": "address"},
        {"indexed": true, "internalType": "address", "name": "to", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Transfer",
                                                   "type": "event"},
               {"constant": true, "inputs": [], "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}], "payable": False,
                "stateMutability": "view", "type": "function"},
               {"constant": true, "inputs": [], "name": "MINIMUM_LIQUIDITY",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False,
                "stateMutability": "view", "type": "function"},
               {"constant": true, "inputs": [], "name": "PERMIT_TYPEHASH",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}], "payable": False,
                "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [
        {"internalType": "address", "name": "", "type": "address"},
        {"internalType": "address", "name": "", "type": "address"}], "name": "allowance", "outputs": [
        {"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                                                                 "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "spender", "type": "address"},
        {"internalType": "uint256", "name": "value", "type": "uint256"}], "name": "approve", "outputs": [
        {"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable",
                                                                                       "type": "function"},
               {"constant": true, "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "payable": False, "stateMutability": "view", "type": "function"},
               {"constant": False, "inputs": [{"internalType": "address", "name": "to", "type": "address"}],
                "name": "burn", "outputs": [{"internalType": "uint256", "name": "amount0", "type": "uint256"},
                                            {"internalType": "uint256", "name": "amount1", "type": "uint256"}],
                "payable": False, "stateMutability": "nonpayable", "type": "function"},
               {"constant": true, "inputs": [], "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False,
                "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "factory",
                                                                 "outputs": [{"internalType": "address", "name": "",
                                                                              "type": "address"}], "payable": False,
                                                                 "stateMutability": "view", "type": "function"},
               {"constant": true, "inputs": [], "name": "getReserves",
                "outputs": [{"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
                            {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
                            {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"}],
                "payable": False, "stateMutability": "view", "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "_token0", "type": "address"},
        {"internalType": "address", "name": "_token1", "type": "address"}], "name": "initialize", "outputs": [],
                                                                                   "payable": False,
                                                                                   "stateMutability": "nonpayable",
                                                                                   "type": "function"},
               {"constant": true, "inputs": [], "name": "kLast",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False,
                "stateMutability": "view", "type": "function"},
               {"constant": False, "inputs": [{"internalType": "address", "name": "to", "type": "address"}],
                "name": "mint", "outputs": [{"internalType": "uint256", "name": "liquidity", "type": "uint256"}],
                "payable": False, "stateMutability": "nonpayable", "type": "function"},
               {"constant": true, "inputs": [], "name": "name",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False,
                "stateMutability": "view", "type": "function"},
               {"constant": true, "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "nonces", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "payable": False, "stateMutability": "view", "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "owner", "type": "address"},
        {"internalType": "address", "name": "spender", "type": "address"},
        {"internalType": "uint256", "name": "value", "type": "uint256"},
        {"internalType": "uint256", "name": "deadline", "type": "uint256"},
        {"internalType": "uint8", "name": "v", "type": "uint8"},
        {"internalType": "bytes32", "name": "r", "type": "bytes32"},
        {"internalType": "bytes32", "name": "s", "type": "bytes32"}], "name": "permit", "outputs": [], "payable": False,
                                                                                   "stateMutability": "nonpayable",
                                                                                   "type": "function"},
               {"constant": true, "inputs": [], "name": "price0CumulativeLast",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False,
                "stateMutability": "view", "type": "function"},
               {"constant": true, "inputs": [], "name": "price1CumulativeLast",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False,
                "stateMutability": "view", "type": "function"},
               {"constant": False, "inputs": [{"internalType": "address", "name": "to", "type": "address"}],
                "name": "skim", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
               {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount0Out", "type": "uint256"},
                                              {"internalType": "uint256", "name": "amount1Out", "type": "uint256"},
                                              {"internalType": "address", "name": "to", "type": "address"},
                                              {"internalType": "bytes", "name": "data", "type": "bytes"}],
                "name": "swap", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
               {"constant": true, "inputs": [], "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False,
                "stateMutability": "view", "type": "function"},
               {"constant": False, "inputs": [], "name": "sync", "outputs": [], "payable": False,
                "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "token0",
                                                                       "outputs": [
                                                                           {"internalType": "address", "name": "",
                                                                            "type": "address"}], "payable": False,
                                                                       "stateMutability": "view", "type": "function"},
               {"constant": true, "inputs": [], "name": "token1",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False,
                "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "totalSupply",
                                                                 "outputs": [{"internalType": "uint256", "name": "",
                                                                              "type": "uint256"}], "payable": False,
                                                                 "stateMutability": "view", "type": "function"},
               {"constant": False, "inputs": [{"internalType": "address", "name": "to", "type": "address"},
                                              {"internalType": "uint256", "name": "value", "type": "uint256"}],
                "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False,
                "stateMutability": "nonpayable", "type": "function"}, {"constant": False, "inputs": [
        {"internalType": "address", "name": "from", "type": "address"},
        {"internalType": "address", "name": "to", "type": "address"},
        {"internalType": "uint256", "name": "value", "type": "uint256"}], "name": "transferFrom", "outputs": [
        {"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable",
                                                                       "type": "function"}]

base = "https://io.dexscreener.com/u/chart/bars/ethereum/"
contract = "0x688C56C2a19b88E46b008AaaA268a29F1772B79B"
# contract = "0xc4c336c9da49dd5c9fd00e5de91a0bf8608c363d" # giza


time0 = "1653944340000"
one_minute = 60 * 1000
five_minutes = one_minute * 5

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


def get_liq_pool(contract):
    try:
        contract = web3.toChecksumAddress(contract)
        factory_contract = web3.eth.contract(address=contract, abi=factory_abi)
        return factory_contract.functions.getReserves().call()[1] * 10 ** -18
    except:
        return 0


def get_diff(ath, closeUsd):
    return int(((float(ath) / float(closeUsd)) - 1) * 100)


def get_ath(time0, contract):
    tim1 = str(int(time0) + 360000000)
    url = base + contract + "?from=" + time0 + "&to=" + tim1 + "&res=360000&cb=301"
    bars = requests.get(url, headers=headers).json()['bars']
    # print(url, bars)
    ath = bars[0]['highUsd']
    start = bars[0]['openUsd']
    timestamp_start = bars[0]['timestamp']

    return {"start": start, "ath": ath, 'timestamp': timestamp_start}


def get_info_hour(time0, contract):
    time1 = str(3600000 + int(time0))
    url = base + contract + "?from=" + time0 + "&to=" + time1 + "&res=1&cb=301"
    # print(url)

    r = requests.get(url, headers=headers).json()
    return r['bars']


def parse_start_volume(time0, contract, ath):
    # print(datetime.fromtimestamp(int(time0)/1000).strftime('%Y-%m-%d %H:%M:%S'))
    try:
        bars = get_info_hour(time0, contract)

        start_price = bars[0]['openUsd']
        length = (bars[-1]['timestamp'] - bars[0]['timestamp']) // one_minute
        start_time = bars[0]['timestamp']
        volumes = []
        peaks = []

        volumes.append(int(float(bars[0]['volumeUsd'])))
        peaks.append(get_diff(ath, float(bars[0]['closeUsd'])))
        for i in range(1, len(bars)):
            # if i == 4:
            #     peaks.append(get_diff(ath, float(bars[i]['closeUsd'])))
            # if i == 9:
            #     peaks.append(get_diff(ath, float(bars[i]['closeUsd'])))
            # if i == 14:
            #     peaks.append(get_diff(ath, float(bars[i]['closeUsd'])))

            # volume math
            if bars[i]['timestamp'] - bars[i - 1]['timestamp'] == one_minute:
                volumes.append(int(float(bars[i]['volumeUsd'])))
                peaks.append(get_diff(ath, float(bars[i]['closeUsd'])))
            else:
                for j in range((bars[i]['timestamp'] - bars[i - 1]['timestamp']) // one_minute - 1):
                    volumes.append(0)
                    peaks.append(peaks[i - 1])
                volumes.append(int(float(bars[i]['volumeUsd'])))
                peaks.append(get_diff(ath, float(bars[i]['closeUsd'])))
            # print(peaks)
        return {"volumes": volumes, "peaks": peaks}
    except TypeError:
        volumes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        peaks = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        return {"volumes": volumes, "peaks": peaks}



def check_rug(contract):
    r = requests.get(
        f"https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=eth&token={contract}",
        headers=headers)
    html = r.text

    lp_pool = get_liq_pool(contract)
    try:
        # parse the HTML
        soup = BeautifulSoup(html, "html.parser")

        # print the HTML as text
        parseError = json.loads(str(soup))["Error"]
        assert (parseError == None)
        # bool is Rug?
        isRug = json.loads(str(soup))["IsHoneypot"]
        buyTax = json.loads(str(soup))["BuyTax"]
        sellTax = json.loads(str(soup))["SellTax"]

        # print(buyTax, sellTax, isRug)


        if not isRug and sellTax <= 10 and buyTax <= 10 and lp_pool > 0.7:
            return {"scam": False, "isRug": isRug, "sellTax": sellTax, "buyTax": buyTax, "lp_pool": lp_pool}
        else:
            return {"scam": True, "isRug": isRug, "sellTax": sellTax, "buyTax": buyTax, "lp_pool": lp_pool}
    except Exception:
        return {"scam": True, "isRug": True, "sellTax": 0, "buyTax": 0, "lp_pool": 0}

# print(parse_start_volume(time0, contract), '\n', len(parse_start_volume(time0, contract)))
#
# insert_row(contract, parse_start_volume(time0, contract))
#
# for ts in range(int(time0), int(float(time.time())) * 1000, one_minute * 60):
#     print(get_info_hour(str(ts), contract))


# print(get_ath(time0, contract))
