import random

# 人数
PLAYER_NUM = 3

# 牌の数
MJHAI_NUM = 108

# 牌
mjhai_name = [
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
    "1m", "9m", "東", "南", "西", "北", "白", "發", "中"
]

# 全ての牌
mjhai = []
for i in range(MJHAI_NUM):
    mjhai.append(mjhai_name[int(i / 4)])

# 山の作成 & シャッフル
yama = list(range(MJHAI_NUM))
random.shuffle(yama)

#ゲームスタート
cur_pos = 0
tehai = []

oya = 0
cur_player = oya

# 配牌
for i in range(PLAYER_NUM):
    tehai.append([])

    for j in range(13):
        tehai[i].append(yama[cur_pos])
        cur_pos += 1

# 摸打
while cur_pos < MJHAI_NUM:
    for i in range(PLAYER_NUM):
        # ツモ
        tehai[i].sort()
        tehai[i].append(yama[cur_pos])
        cur_pos += 1

        # 表示
        print("Player" + str(i + 1) + " [残り" + str(MJHAI_NUM - cur_pos) + "]")

        for j in range(13):
            print(mjhai[tehai[i][j]] + " ", end="")
        print(" " + mjhai[tehai[i][j]])

        for j in range(13):
            print(format(j, "<3d"), end="")
        print(" " + str(j))

        # 入力
        while True:
            select_input = input("> ")

            if select_input == "q":
                exit()

            elif select_input == "":
                select = 13
                break

            select = int(select_input)
            if select >= 0 and select <= 14:
                break

        # 打牌
        tehai[i].pop(select)
        print()

print("終了")