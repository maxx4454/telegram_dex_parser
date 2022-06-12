from parser import *
from db import *
from read_telegram_chat import *

# {"timestamp": timestamp, "pair": addr_pair, "token": addr_token, "pooled_weth": pooled_weth, "fdv": fdv})
# {"start": start, "ath": ath}
# {"volumes": volumes, "peaks": peaks}
# {"scam": False, "isRug": isRug, "sellTax": sellTax, "buyTax": buyTax, "lp_pool": lp_pool}

def process_token(token_inf):
    token = token_inf['token']
    pooled_weth = token_inf['pooled_weth']
    fdv = token_inf['fdv']
    timestamp = token_inf['timestamp']

    contract = token_inf['pair']
    time0 = str(int(timestamp) - 900000)

    res1 = get_ath(time0, contract)
    start_price = res1['start']
    ath = res1['ath']
    ath_percent = get_diff(ath, start_price)

    scam_report = check_rug(contract)
    scam = scam_report['scam']
    is_rug = scam_report['isRug']
    s_tax = scam_report['sellTax']
    b_tax = scam_report['buyTax']
    lp_pool = scam_report['lp_pool']


    volparinf = parse_start_volume(time0, contract, ath)
    volumes = volparinf['volumes']
    peaks = volparinf['peaks']

    # token, pair, volumes, ath, isRug, isHoneyPot, sell_tax, buy_tax, lp_pool, fdv, pooled_weth, timestamp, peaks
    insert_row(token, contract, volumes, ath_percent, scam, is_rug, s_tax, b_tax, lp_pool, fdv, pooled_weth, timestamp, peaks)

def real_main():

    process_token(get_tokens()[0])

print(get_tokens())

real_main()