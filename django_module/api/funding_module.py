from .models import Funding, FundingFinal


def funding_rate(response):

    # Установка начальных значений
    data = response.json()

    top100list = ["USDT", "BNB", "XRP", "USDC", "SOL", "ADA", "DOGE", "TRX", "TON", "DAI", "MATIC", "LTC",
                  "DOT", "WBTC", "BCH", "SHIB", "LINK", "LEO", "TUSD", "AVAX", "XLM", "XMR", "OKB", "ATOM", "UNI",
                  "ETC", "BUSD", "HBAR", "FIL", "LDO", "ICP", "MKR", "CRO", "APT", "VET", "OP", "QNT", "ARB", "MNT",
                  "NEAR", "AAVE", "GRT", "STX", "ALGO", "BSV", "USDD", "RNDR", "INJ", "XDC", "IMX", "EGLD", "XTZ",
                  "EOS", "ASX", "SAND", "THETA", "BGB", "MANA", "RUNE", "SNX", "FTM", "KAVA", "NEO", "XEC", "USDP",
                  "PAXG", "XAUT", "FLOW", "KCS", "TWT", "FXS", "CHZ", "IOTA", "OCEAN", "KLAY", "ZEC", "CRV", "APE",
                  "CFX", "RPL", "LOOM", "HT", "MINA", "BTT", "GT", "SUI", "CSPR", "DYDX", "GALA", "LUNC", "GMX", "COMP",
                  "NFT", "WOO", "NEXO", "DASH", "ZIL", "ROSE"]

    btc = []
    eth = []
    top100 = []
    other_coins = []

    for currency_data in data.get("data", []):

        symbol = currency_data.get("symbol", "")
        exchange_logo = currency_data.get("symbolLogo", "")
        u_margin_list = currency_data.get("uMarginList", [])  # Массив с данными бирж

        def get_rate(exchange_list, exchange_name):
            for ex in exchange_list:
                if ex.get("exchangeName") == exchange_name and "rate" in ex:
                    return ex["rate"]
            return 0

        binance_rate = round(get_rate(u_margin_list, "Binance"), 4)
        okx_rate = round(get_rate(u_margin_list, "OKX"), 4)
        dydx_rate = round(get_rate(u_margin_list, "dYdX"), 4)
        bybit_rate = round(get_rate(u_margin_list, "Bybit"), 4)
        gate_rate = round(get_rate(u_margin_list, "Gate"), 4)
        bitget_rate = round(get_rate(u_margin_list, "Bitget"), 4)
        coinex_rate = round(get_rate(u_margin_list, "CoinEx"), 4)
        bingx_rate = round(get_rate(u_margin_list, "BingX"), 4)

        rates = [okx_rate, dydx_rate, bybit_rate, gate_rate, bitget_rate, coinex_rate, bingx_rate]
        non_zero_rates = [rate for rate in rates if rate != 0]
        other_ex_sum = sum(non_zero_rates)
        other_ex_numbers = len(non_zero_rates)

        if other_ex_numbers != 0:
            average = other_ex_sum / other_ex_numbers
        else:
            average = 0

        other_exchange_sum = round(average, 4)

        if symbol in top100list:
            top100.append([symbol, round(binance_rate, 4), other_exchange_sum])
        elif symbol == 'BTC':
            btc.append([symbol, round(binance_rate, 4), other_exchange_sum])
        elif symbol == 'ETH':
            eth.append([symbol, round(binance_rate, 4), other_exchange_sum])
        else:
            other_coins.append([symbol, round(binance_rate, 4), other_exchange_sum])

        funding_obj, created = Funding.objects.get_or_create(
            symbol=symbol,
            defaults={
                "exchangeLogo": exchange_logo,
                "binance_funding": binance_rate,
                "okx_funding": okx_rate,
                "dydx_funding": dydx_rate,
                "bybit_funding": bybit_rate,
                "gate_funding": gate_rate,
                "bitget_funding": bitget_rate,
                "coinex_funding": coinex_rate,
                "bingx_funding": bingx_rate,
                "other_exchange_sum": other_exchange_sum,
            }
        )

        # Если запись уже существует, обновляем значения
        if not created:
            funding_obj.exchangeLogo = exchange_logo
            funding_obj.binance_funding = binance_rate
            funding_obj.okx_funding = okx_rate
            funding_obj.dydx_funding = dydx_rate
            funding_obj.bybit_funding = bybit_rate
            funding_obj.gate_funding = gate_rate
            funding_obj.bitget_funding = bitget_rate
            funding_obj.coinex_funding = coinex_rate
            funding_obj.bingx_funding = bingx_rate
            funding_obj.other_exchange_sum = other_exchange_sum

        # Сохраняем изменения
        funding_obj.save()

        def get_final_tables(input_data):

            other_ex_positive_count = 0
            other_ex_balanced_count = 0
            other_ex_negative_count = 0

            for _, _, other_ex in input_data['data']:
                if other_ex >= 0.01:
                    other_ex_positive_count += 1
                elif -0.01 <= other_ex <= 0.01:
                    other_ex_balanced_count += 1
                else:
                    other_ex_negative_count += 1

            binance_positive_count = 0
            binance_balanced_count = 0
            binance_negative_count = 0

            for _, binance, _ in input_data['data']:
                if binance >= 0.01:
                    binance_positive_count += 1
                elif -0.01 <= binance <= 0.01:
                    binance_balanced_count += 1
                else:
                    binance_negative_count += 1


            funding_final_obj, created = FundingFinal.objects.get_or_create(
                symbol=input_data['label'],
                defaults={
                    "binance_positive": binance_positive_count,
                    "binance_balance": binance_balanced_count,
                    "binance_negative": binance_negative_count,
                    "other_ex_positive": other_ex_positive_count,
                    "other_ex_balance": other_ex_balanced_count,
                    "other_ex_negative": other_ex_negative_count,
                }
            )

            # Если запись уже существует, обновляем значения
            if not created:
                funding_final_obj.binance_positive = binance_positive_count
                funding_final_obj.binance_balance = binance_balanced_count
                funding_final_obj.binance_negative = binance_negative_count
                funding_final_obj.other_ex_positive = other_ex_positive_count
                funding_final_obj.other_ex_balance = other_ex_balanced_count
                funding_final_obj.other_ex_negative = other_ex_negative_count

            # Сохраняем изменения
            funding_final_obj.save()


        def get_final_tables2(input_data):

            other_ex_positive_count = 0
            other_ex_balanced_count = 0
            other_ex_negative_count = 0

            for _, _, other_ex in input_data['data']:
                if other_ex >= 0.01:
                    other_ex_positive_count += 1
                elif -0.01 <= other_ex <= 0.01:
                    other_ex_balanced_count += 1
                else:
                    other_ex_negative_count += 1

            binance_positive_count = 0
            binance_balanced_count = 0
            binance_negative_count = 0

            for _, binance, _ in input_data['data']:
                if binance >= 0.01:
                    binance_positive_count += 1
                elif -0.01 <= binance <= 0.01:
                    binance_balanced_count += 1
                else:
                    binance_negative_count += 1

            top_pos = []
            top_neg = []

            sort_column_index = 1
            sorted_data = sorted(input_data['data'], key=lambda x: x[sort_column_index], reverse=True)

            top_pos = [item[0] for item in sorted_data[:10]]
            top_neg = [item[0] for item in sorted_data[-10:]]


            funding_final_obj, created = FundingFinal.objects.get_or_create(
                symbol=input_data['label'],
                defaults={
                    "binance_positive": binance_positive_count,
                    "binance_balance": binance_balanced_count,
                    "binance_negative": binance_negative_count,
                    "other_ex_positive": other_ex_positive_count,
                    "other_ex_balance": other_ex_balanced_count,
                    "other_ex_negative": other_ex_negative_count,
                    "top_pos": top_pos,
                    "top_neg": top_neg,
                }
            )

            # Если запись уже существует, обновляем значения
            if not created:
                funding_final_obj.binance_positive = binance_positive_count
                funding_final_obj.binance_balance = binance_balanced_count
                funding_final_obj.binance_negative = binance_negative_count
                funding_final_obj.other_ex_positive = other_ex_positive_count
                funding_final_obj.other_ex_balance = other_ex_balanced_count
                funding_final_obj.other_ex_negative = other_ex_negative_count
                funding_final_obj.top_pos = top_pos
                funding_final_obj.top_neg = top_neg

            # Сохраняем изменения
            funding_final_obj.save()


        get_final_tables({'label': 'BTC', 'data': btc})
        get_final_tables({'label': 'ETH', 'data': eth})
        get_final_tables2({'label': 'Top100', 'data': top100})
        get_final_tables({'label': 'OtherCoins', 'data': other_coins})
