from mahjong import *

# 全ての牌をセット
# 筒子・索子
mjhai_list = []
for i in range(2):
    for j in range(1, 10):
        mjhai_list.extend([MjHai(i, j) for k in range(4)])

# 萬子
mjhai_list.extend([MjHai(2, 1) for i in range(4)])
mjhai_list.extend([MjHai(2, 9) for i in range(4)])

# 字牌
for i in range(3, 10):
    mjhai_list.extend([MjHai(i) for j in range(4)])

# ゲームスタート
game = Game(3, mjhai_list)
game.haipai()

# 摸打
while len(game.yama) > 0:
    for i in range(game.player_num):
        print("Player" + str(i) + " [残り" + str(len(game.yama)) + "]")
        game.tumo(i)
        game.show(i)

        for j in range(14):
            print(format(j, "<3d"), end="")
        print()

        # 入力
        while True:
            select_input = input("> ")

            if select_input == "q":
                exit()

            # ツモ切り
            elif select_input == "":
                select = -1
                break

            select = int(select_input)
            if select >= 0 and select < 14:
                break

        # 打牌
        game.dahai(i, select)
        print()

print("終了")
