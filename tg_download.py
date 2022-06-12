
import csv
import json
import sys
from math import *


maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 2)

from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest



# Присваиваем значения внутренним переменным
api_id = 12403598
api_hash = "069c3c3f4ae45f35630d194f9ce03363"
username = "arrogant_preson"

# создание объекта клиента Telegram
client = TelegramClient(username, api_id, api_hash)

client.start()


async def dump_all_messages(channel, short_url_, datetime_):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        print(f'{str(datetime.now())} | Получено записей: {len(all_messages)}', end='\r')
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    #
    with open(f'{short_url_}_messages_{datetime_}.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    channel = await client._get_peer(-1001699399340)
    # await dump_all_participants(channel)
    await dump_all_messages(channel, channel_string, datetime_string)


# парсинг чата или канала в Telegram и сохранение в JSON-файл
url = 't.me/' + input("Введите ссылку на канал или чат: @")
# url = 't.me/testflight_app'
channel_string = url.split('/')[-1]
print(f'{str(datetime.now())} | Парсинг начат')
datetime_string = str(datetime.now()).replace("-", "").replace(" ", "T").replace(":", "").split(".")[0]
with client:
    client.loop.run_until_complete(main())
print(f'{str(datetime.now())} | Парсинг закончен!')

