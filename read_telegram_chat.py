import json
import datetime


def get_timestamp(date):
    date = date[:18]
    date, time = date.split('T')
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')
    hour = (int(hour) + 3) % 24
    # print(year, month, day, hour, minute, second)

    second = datetime.datetime(int(year), int(month), int(day), hour, int(minute), int(second))
    return int(second.timestamp())


def find_num_by_index(index, text):
    s = ""
    while text[index] != " " and text[index] != '\n':
        s += text[index]
        index += 1
    return s


def get_tokens():
    list_of_tokens = []
    messages = []


    with open("hff_messages_20220613T001044.json", 'r') as f:

        try:

            for i in json.load(f):
                messages.append(i)

        except Exception as e:
            print('ya ebal')

    for msg in messages:
        try:
            if 'WETH' in msg['message']:
                date = msg['date']
                timestamp = get_timestamp(date)

                url_dex = msg['reply_markup']['rows'][0]['buttons'][0]['url']
                url_tokensniff = msg['reply_markup']['rows'][2]['buttons'][0]['url']
                addr_pair = url_dex[33:75]
                addr_token = url_tokensniff[31:]

                msg_text = msg['message']
                weth_index = msg_text.find("Pooled WETH: ") + 13
                fdv_index = msg_text.find("FDV: ") + 5
                pooled_weth = find_num_by_index(weth_index, msg_text)
                fdv = find_num_by_index(fdv_index, msg_text)[1:]
                fdv = int(fdv.replace(',', ''))
                pooled_weth = float(pooled_weth.replace(',', ''))

                list_of_tokens.append(
                    {"timestamp": timestamp, "pair": addr_pair, "token": addr_token, "pooled_weth": pooled_weth,
                     "fdv": fdv})


        except KeyError:
            print('ya ebal')

    return list_of_tokens
