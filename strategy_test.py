from db import *


def get_rows():
    conn = create_connection("data.db")
    c = conn.cursor()
    c.execute('SELECT * FROM mem')
    all_rows = []
    for row in c:
        is_honeypot = row[6]
        lp_pool = row[9]
        pair = row[2]
        ath = row[3]
        volumes = []
        peaks = []
        peaks.append(ath)

        for i in range(13, 33):
            volumes.append(row[i])
        for i in range(33, 36):
            peaks.append(row[i])

        all_rows.append({"is_honeypot": is_honeypot, "lp_pool": lp_pool, "pair": pair, "ath": ath, "volumes": volumes, "peaks": peaks})
    return all_rows


def criteria_met(row):
    # return True
    try:
        if row['volumes'][0] + row['volumes'][1] + row['volumes'][2] + row['volumes'][3] + row['volumes'][4] > 5000:
            print(row['volumes'][0] + row['volumes'][1] + row['volumes'][2] + row['volumes'][3] + row['volumes'][4])
            return True
        else:
            return False
    except TypeError:
        return False

#full 0 delete
# [id], [token], [pair], [ath], [timestamp], [isRug], [isHoneyPot], [sell_tax], [buy_tax], [lp_pool], [fdv], [pooled_weth], [gas], [volume_1], [volume_2] INTEGER, [volume_3] INTEGER, [volume_4] INTEGER, [volume_5] INTEGER, [volume_6] INTEGER, [volume_7] INTEGER, [volume_8] INTEGER, [volume_9] INTEGER, [volume_10] INTEGER, [volume_11] INTEGER, [volume_12] INTEGER, [volume_13] INTEGER, [volume_14] INTEGER, [volum
# (1386, '0x9ceeb12ae832622203d48a165f10564213bd9996', '0xeb9e3c7ed9104c2dd989cfaacd393353e1ca9745', 18, 1653423065, 1, 1, 0, 0, 3.3700000000000003e-15, 18605, 7.1, None, 293, 0, 0, 0, 0, 0, 0, 293, 234, 0, 391, 0, 0, 0, 0, 293, 820, 1211, 0, 0, 15, 15, 15)
def test_strat_row(row, aim, bet, when_enter):
    if not row['is_honeypot']:
        if row['volumes'][0] == 0 or row['peaks'][0] == 0:
            return bet, False
        if criteria_met(row):

            if row['lp_pool'] < 0.7:
                # print('rugged', end=' ')
                return 0, True
            else:
                #when_enter - минута входа (1 5 10 15)
                if row['peaks'][when_enter]/100 >= aim:
                    # print('peaked', end=' ')
                    return bet * aim, True

                else:
                    # print('sucked', end=' ')
                    return bet * 0.9, True

        return bet, False
    return bet, False


def main():
    cash = 1
    rows = get_rows()
    for row_ in rows:

        bet_sum, zahod = test_strat_row(row_, 30, 0.1, 0)
        if zahod:
            cash -= 0.1
            cash += bet_sum
            print(cash)
    print(cash)


main()








# do_stuff_with_row