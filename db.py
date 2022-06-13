import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)


def itit():
    conn = create_connection("data.db")
    c = conn.cursor()

    c.execute('''
            CREATE TABLE IF NOT EXISTS mem
            ([id] INTEGER PRIMARY KEY, [token] TEXT, [pair] TEXT, [ath] INTEGER, [timestamp] INTEGER, [isRug] BOOLEAN, [isHoneyPot] BOOLEAN, [sell_tax] INTEGER, [buy_tax] INTEGER, [lp_pool] INTEGER, [fdv] INTEGER, [pooled_weth] INTEGER, [gas] INTEGER, [volume_1] INTEGER, [volume_2] INTEGER, [volume_3] INTEGER, [volume_4] INTEGER, [volume_5] INTEGER, [volume_6] INTEGER, [volume_7] INTEGER, [volume_8] INTEGER, [volume_9] INTEGER, [volume_10] INTEGER, [volume_11] INTEGER, [volume_12] INTEGER, [volume_13] INTEGER, [volume_14] INTEGER, [volume_15] INTEGER, [volume_1_5] INTEGER, [volume_1_10] INTEGER, [volume_1_15] INTEGER, [volume_1_30] INTEGER, [volume_1_60] INTEGER, [to_peak_5] INTEGER, [to_peak_10] INTEGER, [to_peak_15] INTEGER)
            ''')

    conn.commit()


def insert_row(token, pair, volumes, ath, isRug, isHoneyPot, sell_tax, buy_tax, lp_pool, fdv, pooled_weth, timestamp,
               peaks):
    conn = create_connection("data.db")
    c = conn.cursor()


    try:
        volume_1_5 = volumes[0] + volumes[1] + volumes[2] + volumes[3] + volumes[4]
    except:
        volume_1_5 = 0
    try:
        volume_1_10 = volume_1_5 + volumes[5] + volumes[6] + volumes[7] + volumes[8] + volumes[9]
        volume_1_15 = volume_1_10 + + volumes[10] + volumes[11] + volumes[12] + volumes[13] + volumes[14]
    except:
        volume_1_10 = 0
        volume_1_15 = 0

    volume_1_30 = 0
    try:
        for i in range(30):
            volume_1_30 += volumes[i]
    except IndexError:
        volume_1_30 = 0

    try:
        volume_1_60 = 0
        for i in range(60):
            volume_1_60 += volumes[i]
    except IndexError:
        volume_1_60 = 0
    if len(volumes) < 15:
        for i in range(len(peaks), 18):
            volumes.append(0)
    if len(peaks) < 15:
        for i in range(len(peaks), 18):
            peaks.append(0)


    # token, pair, volumes, ath, isRug, isHoneyPot, sell_tax, buy_tax, lp_pool, fdv, pooled_weth, timestamp,
    # peaks)
    c.execute(''' INSERT INTO mem (token, pair, ath, timestamp, lp_pool, isRug, isHoneyPot, sell_tax, buy_tax, fdv, pooled_weth, volume_1, volume_2, volume_3, volume_4, volume_5, volume_6, volume_7, volume_8, volume_9, volume_10, volume_11, volume_12, volume_13, volume_14, volume_15, volume_1_5, volume_1_10, volume_1_15, volume_1_30, volume_1_60, to_peak_5, to_peak_10, to_peak_15)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', (
    token, pair, ath, timestamp, lp_pool, isRug, isHoneyPot, sell_tax, buy_tax, fdv, pooled_weth, volumes[0],
    volumes[1], volumes[2], volumes[3], volumes[4], volumes[5], volumes[6], volumes[7], volumes[8], volumes[9],
    volumes[10], volumes[11], volumes[12], volumes[13], volumes[14], volume_1_5, volume_1_10, volume_1_15, volume_1_30, volume_1_60, peaks[4], peaks[9], peaks[14]))

    conn.commit()
