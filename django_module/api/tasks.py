from celery import shared_task
from django.db.models import Avg

from .funding_module import funding_rate
import requests
import telebot
import prettytable as pt

from .models import FundingFinal, TelegramUsers, FundingTop10Pos, FundingTop10Neg, Depth

bot = telebot.TeleBot("6726984732:AAFU2iMO880Zdp9T4wBGWiZew0F36xtC7AM", parse_mode="MarkdownV2")


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

    # ------------------------------- GET DATA FROM DB
    table_data = FundingFinal.objects.all().values(
        "symbol",
        "binance_positive",
        "binance_balance",
        "binance_negative",
        "other_ex_positive",
        "other_ex_balance",
        "other_ex_negative",
    ).order_by("symbol")
    listdata = list(table_data)

    # ------------------------------- SUM DATA


    positive_sum = (sum(item["binance_positive"] for item in listdata))
    balance_sum = (sum(item["binance_balance"] for item in listdata))
    negative_sum = (sum(item["binance_negative"] for item in listdata))
    all_sum = positive_sum + balance_sum + negative_sum

    def percentage(part):
        return round((part / all_sum) * 100)

    # ------------------------------- TABLES MAIN
    table = pt.PrettyTable()

    data = [
        (item['symbol'], item['binance_positive'], item['binance_balance'], item['binance_negative'],
         item['other_ex_positive'], item['other_ex_balance'], item['other_ex_negative']) for item in listdata
    ]

    table.add_column(fieldname=f'Exc', column=[f'Bin +', f'Bin =', f'Bin -', f'Oth +', f'Oth =', f'Oth -'], align='l')
    for (label, bin1, bin2, bin3, o1, o2, o3) in data:
        table.add_column(fieldname=label, column=[bin1, bin2, bin3, o1, o2, o3], align='r')

    # ------------------------------- TABLES SECOND
    table10 = pt.PrettyTable()

    table10pos_data = FundingTop10Pos.objects.all().values(
        "pos_symbol",
        "pos_value",
    )
    listpos10data = list(table10pos_data)
    pos_symbols = [item.get('pos_symbol', 'N/A') for item in listpos10data]
    pos_values = [item.get('pos_value', 0) for item in listpos10data]

    table10neg_data = FundingTop10Neg.objects.all().values(
        "neg_symbol",
        "neg_value",
    ).order_by("neg_value")
    listneg10data = list(table10neg_data)
    neg_symbols = [item.get('neg_symbol', 'N/A') for item in listneg10data]
    neg_values = [item.get('neg_value', 0) for item in listneg10data]


    table10.add_column(fieldname=f'Top +', column=pos_symbols, align='l')
    table10.add_column(fieldname=f'#', column=pos_values, align='l')
    table10.add_column(fieldname=f'Top -', column=neg_symbols, align='l')
    table10.add_column(fieldname=f'#', column=neg_values, align='l')

    # ------------------------------- MESSAGE BODY
    user_data = TelegramUsers.objects.values_list("chat_id", flat=True)
    list_user_data = list(user_data)
    # for chat_id in list_user_data:
    #     print(f'Chat ID: {chat_id}')
    #
    #     combined_message = f'```\nPos(+): {positive_sum} ({percentage(positive_sum)}%)\nBal(=): {balance_sum} ({percentage(balance_sum)}%)\nNeg(-): {negative_sum} ({percentage(negative_sum)}%)\n\n{table}\n\n{table10}\n\nEyeOfChubaka Funding v.1.0\n```'
    #     bot.send_message(chat_id, combined_message)
    combined_message = f'```\nPos(+): {positive_sum} ({percentage(positive_sum)}%)\nBal(=): {balance_sum} ({percentage(balance_sum)}%)\nNeg(-): {negative_sum} ({percentage(negative_sum)}%)\n\n{table}\n\n{table10}\n\nEyeOfChubaka Funding v.1.0\n```'
    bot.send_message(-1002135412128, combined_message,  message_thread_id=4)

@shared_task()
def send_depth_to_tg():

    # ------------------------------- GET DATA FROM DB
    table_data = Depth.objects.all().values(
        "symbol",
        "limit8",
        "limit30",
    )
    average_limit30 = table_data.aggregate(avg_limit30=Avg('limit30'))['avg_limit30']
    average_limit8 = table_data.aggregate(avg_limit8=Avg('limit8'))['avg_limit8']
    btcusdt_limit8 = table_data.get(symbol="BTCUSDT")["limit8"]

    # ------------------------------- TABLES MAIN

    table = pt.PrettyTable()

    pos_data = table_data.order_by("-limit8")[:10]
    list_pos_data = list(pos_data)
    pos_symbols = [item.get('symbol', 'N/A') for item in list_pos_data]
    pos_values = [item.get('limit8', 0) for item in list_pos_data]

    neg_data = table_data.order_by("limit8")[:10]  # изменено здесь
    list_neg_data = list(neg_data)
    neg_symbols = [item.get('symbol', 'N/A') for item in list_neg_data]
    neg_values = [item.get('limit8', 0) for item in list_neg_data]

    table.add_column(fieldname=f'Top +', column=pos_symbols, align='l')
    table.add_column(fieldname=f'#', column=pos_values, align='l')
    table.add_column(fieldname=f'Top -', column=neg_symbols, align='l')
    table.add_column(fieldname=f'#', column=neg_values, align='l')


    # ------------------------------- MESSAGE BODY
    user_data = TelegramUsers.objects.values_list("chat_id", flat=True)
    list_user_data = list(user_data)

    # for chat_id in list_user_data:
    #     print(f'Chat ID: {chat_id}')
    #     combined_message = f'```\nBA8 BTC: {round(btcusdt_limit8, 2)}\nBA8 ALL: {round(average_limit8, 2)}\nAVG ALL: {round(average_limit30, 2)}\n{table}\n\nEyeOfChubaka BidAsk v.1.0\n```'
    #     bot.send_message(chat_id, combined_message)

    combined_message = f'```\nBA8 BTC: {round(btcusdt_limit8, 2)}\nBA8 ALL: {round(average_limit8, 2)}\nAVG ALL: {round(average_limit30, 2)}\n{table}\n\nEyeOfChubaka BidAsk v.1.0\n```'
    bot.send_message(-1002135412128, combined_message,  message_thread_id=2)
