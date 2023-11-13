from binance import ThreadedDepthCacheManager
import psycopg2 as pg


def main():

    symbol_list = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "NEOUSDT", "LTCUSDT", "QTUMUSDT", "ADAUSDT", "XRPUSDT", "EOSUSDT", "IOTAUSDT", "XLMUSDT", "ONTUSDT", "TRXUSDT", "ETCUSDT", "ICXUSDT", "VETUSDT", "USDCUSDT", "LINKUSDT", "WAVESUSDT", "HOTUSDT", "ZILUSDT", "ZRXUSDT", "FETUSDT", "BATUSDT", "XMRUSDT", "ZECUSDT", "IOSTUSDT", "CELRUSDT", "DASHUSDT", "OMGUSDT", "THETAUSDT", "ENJUSDT", "MATICUSDT", "ATOMUSDT", "ONEUSDT", "FTMUSDT", "ALGOUSDT", "DOGEUSDT", "DUSKUSDT", "ANKRUSDT", "MTLUSDT", "TOMOUSDT", "DENTUSDT", "KEYUSDT", "CHZUSDT", "BANDUSDT", "BUSDUSDT", "XTZUSDT", "RENUSDT", "RVNUSDT", "HBARUSDT", "NKNUSDT", "STXUSDT", "KAVAUSDT", "ARPAUSDT", "IOTXUSDT", "RLCUSDT", "BCHUSDT", "FTTUSDT", "OGNUSDT", "BNTUSDT", "COTIUSDT", "STPTUSDT", "SOLUSDT", "CTSIUSDT", "CHRUSDT", "MDTUSDT", "STMXUSDT", "KNCUSDT", "LRCUSDT", "COMPUSDT", "ZENUSDT", "SNXUSDT", "SXPUSDT", "MKRUSDT", "STORJUSDT", "MANAUSDT", "YFIUSDT", "BALUSDT", "BLZUSDT", "SRMUSDT", "ANTUSDT", "CRVUSDT", "SANDUSDT", "OCEANUSDT", "NMRUSDT", "DOTUSDT", "RSRUSDT", "PAXGUSDT", "TRBUSDT", "SUSHIUSDT", "YFIIUSDT", "KSMUSDT", "EGLDUSDT", "RUNEUSDT", "UMAUSDT", "BELUSDT", "UNIUSDT", "OXTUSDT", "SUNUSDT", "AVAXUSDT", "HNTUSDT", "FLMUSDT", "XVSUSDT", "ALPHAUSDT", "AAVEUSDT", "NEARUSDT", "INJUSDT", "AUDIOUSDT", "CTKUSDT", "AKROUSDT", "AXSUSDT", "UNFIUSDT", "ROSEUSDT", "XEMUSDT", "SKLUSDT", "GRTUSDT", "PSGUSDT", "1INCHUSDT", "REEFUSDT", "OGUSDT", "CELOUSDT", "RIFUSDT", "TRUUSDT", "CKBUSDT", "TWTUSDT", "LITUSDT", "SFPUSDT", "DODOUSDT", "CAKEUSDT", "BADGERUSDT", "DEGOUSDT", "ALICEUSDT", "LINAUSDT", "PERPUSDT", "CFXUSDT", "TLMUSDT", "FORTHUSDT", "BAKEUSDT", "SLPUSDT", "SHIBUSDT", "ICPUSDT", "ARUSDT", "MASKUSDT", "LPTUSDT", "XVGUSDT", "ATAUSDT", "GTCUSDT", "KLAYUSDT", "C98USDT", "CLVUSDT", "QNTUSDT", "FLOWUSDT", "MINAUSDT", "RAYUSDT", "ALPACAUSDT", "XECUSDT", "DYDXUSDT", "IDEXUSDT", "GALAUSDT", "ILVUSDT", "YGGUSDT", "FIDAUSDT", "FRONTUSDT", "AGLDUSDT", "RADUSDT", "LAZIOUSDT", "CHESSUSDT", "AUCTIONUSDT", "DARUSDT", "ENSUSDT", "VGXUSDT", "JASMYUSDT", "RNDRUSDT", "MCUSDT", "BICOUSDT", "FXSUSDT", "HIGHUSDT", "CVXUSDT", "PEOPLEUSDT", "SPELLUSDT", "JOEUSDT", "ACHUSDT", "IMXUSDT", "GLMRUSDT", "SCRTUSDT", "API3USDT", "WOOUSDT", "ALPINEUSDT", "TUSDT", "ASTRUSDT", "GMTUSDT", "KDAUSDT", "APEUSDT", "BSWUSDT", "MULTIUSDT", "GALUSDT", "LDOUSDT", "OPUSDT", "LEVERUSDT", "STGUSDT", "LUNCUSDT", "GMXUSDT", "APTUSDT", "HFTUSDT", "PHBUSDT", "HOOKUSDT", "MAGICUSDT", "HIFIUSDT", "RPLUSDT", "AGIXUSDT", "GNSUSDT", "SYNUSDT", "SSVUSDT", "LQTYUSDT", "AMBUSDT", "USTCUSDT", "IDUSDT", "ARBUSDT", "LOOMUSDT", "RDNTUSDT", "EDUUSDT", "SUIUSDT", "PEPEUSDT", "FLOKIUSDT", "COMBOUSDT", "MAVUSDT", "PENDLEUSDT", "ARKMUSDT", "WLDUSDT", "SEIUSDT", "CYBERUSDT", "ARKUSDT", "CREAMUSDT", "GFTUSDT"]

    conn = pg.connect(
        host='postgres',
        database='django_db',
        port=5432,
        user='user',
        password='password'
    )

    cur = conn.cursor()
    print("Подключение к postgres установленно.")

    dcm = ThreadedDepthCacheManager()
    dcm.start()

    def on_input_message(depth_cache):

        # time = depth_cache.update_time

        symbol = depth_cache.symbol
        bids = depth_cache.get_bids()
        asks = depth_cache.get_asks()

        limit3positive = asks[0][0] * 1.03
        limit3negative = bids[0][0] * 0.97
        limit5positive = asks[0][0] * 1.05
        limit5negative = bids[0][0] * 0.95
        limit8positive = asks[0][0] * 1.08
        limit8negative = bids[0][0] * 0.92
        limit30positive = asks[0][0] * 1.30
        limit30negative = bids[0][0] * 0.70

        total_asks_volume = sum(price * amount for price, amount in asks)
        total_bids_volume = sum(price * amount for price, amount in bids)

        total3_asks_volume = sum(price * amount for price, amount in asks if price <= limit3positive)
        total3_bids_volume = sum(price * amount for price, amount in bids if price >= limit3negative)
        total5_asks_volume = sum(price * amount for price, amount in asks if price <= limit5positive)
        total5_bids_volume = sum(price * amount for price, amount in bids if price >= limit5negative)
        total8_asks_volume = sum(price * amount for price, amount in asks if price <= limit8positive)
        total8_bids_volume = sum(price * amount for price, amount in bids if price >= limit8negative)
        total30_asks_volume = sum(price * amount for price, amount in asks if price <= limit30positive)
        total30_bids_volume = sum(price * amount for price, amount in bids if price >= limit30negative)

        limit3 = total3_bids_volume / total3_asks_volume
        limit5 = total5_bids_volume / total5_asks_volume
        limit8 = total8_bids_volume / total8_asks_volume
        limit30 = total30_bids_volume / total30_asks_volume

        data = {
            'Symbol': symbol,
            'Asks': int(total_asks_volume),
            'Bids': int(total_bids_volume),
            'Limit3': round(limit3, 2),
            'Limit5': round(limit5, 2),
            'Limit8': round(limit8, 2),
            'Limit30': round(limit30, 2),
        }

        # print(data)

        cur.execute(
            "INSERT INTO api_depth (symbol, total_asks_volume, total_bids_volume, limit3, limit5, limit8, limit30) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (symbol) DO UPDATE SET (total_asks_volume, total_bids_volume, limit3, limit5, limit8, limit30) = ROW(EXCLUDED.total_asks_volume, EXCLUDED.total_bids_volume, EXCLUDED.limit3, EXCLUDED.limit5, EXCLUDED.limit8, EXCLUDED.limit30)",
            (data['Symbol'], data['Asks'], data['Bids'], data['Limit3'], data['Limit5'], data['Limit8'], data['Limit30'])
        )

        conn.commit()

    for coin_symbol in symbol_list:
        dcm.start_depth_cache(on_input_message, symbol=coin_symbol)

    dcm.join()


if __name__ == "__main__":
    main()
