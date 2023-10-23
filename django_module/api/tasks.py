from celery import shared_task
from .funding_module import funding_rate
import requests
import telebot
import prettytable as pt

from .models import FundingFinal, TelegramUsers


@shared_task()
def get_funding_rate():

    url = "https://open-api.coinglass.com/public/v2/funding"
    headers = {
        "accept": "application/json",
        "coinglassSecret": "ce9ddceeb2754f72ae8e7054fe65a68a"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        funding_rate(response)
    else:
        print(f"Не удалось получить данные. Код статуса: {response.status_code}")


@shared_task()
def send_funding_to_tg():
    bot = telebot.TeleBot("6726984732:AAFU2iMO880Zdp9T4wBGWiZew0F36xtC7AM", parse_mode="MarkdownV2")

    table_data = FundingFinal.objects.all().values(
        "symbol",
        "binance_positive",
        "binance_balance",
        "binance_negative",
        "other_ex_positive",
        "other_ex_balance",
        "other_ex_negative",
        "top_pos",
        "top_neg"
    ).order_by("symbol")
    listdata = list(table_data)

    user_data = TelegramUsers.objects.values_list("chat_id", flat=True)
    list_user_data = list(user_data)

    table = pt.PrettyTable(['Label', 'Bin+', 'Bin0', 'Bin-', 'Oth+', 'Oth0', 'Oth-'])
    table.align['Label'] = 'l'
    table.align['Bin+'] = 'l'
    table.align['Bin0'] = 'l'
    table.align['Bin-'] = 'l'
    table.align['Oth+'] = 'r'
    table.align['Oth0'] = 'r'
    table.align['Oth-'] = 'r'

    data = [
        (item['symbol'], item['binance_positive'], item['binance_balance'], item['binance_negative'],
         item['other_ex_positive'], item['other_ex_balance'], item['other_ex_negative']) for item in listdata
    ]

    top100_entry = FundingFinal.objects.get(symbol="Top100")
    top_pos_value = top100_entry.top_pos
    top_neg_value = top100_entry.top_neg

    for label, bin1, bin2, bin3, o1, o2, o3 in data:
        table.add_row([label, f'{bin1}', f'{bin2}', f'{bin3}', f'{o1}', f'{o2}', f'{o3}'])

    print(list_user_data)
    for chat_id in list_user_data:
        print(f'Chat ID: {chat_id}')
        bot.send_message(chat_id, f'```{table}```')
        bot.send_message(chat_id, f'Top positive funding rate: {top_pos_value}')
        bot.send_message(chat_id, f'Top negative funding rate: {top_neg_value}')
