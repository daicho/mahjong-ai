import random
import tkinter as tk
import mahjong as mj
import graphic as gp

root = tk.Tk()
root.title("Iso-kun")
size = 13 * gp.MJHAI_HEIGHT + 5 * gp.MJHAI_WIDTH + 4
root.geometry(str(size) + "x" + str(size))
background = tk.Canvas(bg="green")
background.pack(fill=tk.BOTH, expand=1)

# 全ての牌をセット
# 筒子・索子
mjhai_set = []
for i in range(2):
    for j in range(1, 10):
        mjhai_set.extend([mj.MjHai(i, j) for k in range(4)])

# 萬子
mjhai_set.extend([mj.MjHai(2, 1) for i in range(4)])
mjhai_set.extend([mj.MjHai(2, 9) for i in range(4)])

# 字牌
for i in range(3, 10):
    mjhai_set.extend([mj.MjHai(i) for j in range(4)])

gp.load_image(mjhai_set)
players = [mj.Player("Player1"), mj.Player("Player2"), mj.Player("Player3")]

# ゲームスタート
yama = mjhai_set[:]
random.shuffle(yama)

for player in players:
    player.haipai(yama)

# 摸打
while len(yama) > 0:
    for player in players:
        player.tumo(yama)
        print(player.name + " [残り" + str(len(yama)) + "]")
        player.show()
        gp.show_tehai(background, player)

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
        player.dahai(select)
        print()

print("終了")
