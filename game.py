import sys
import random
import tkinter as tk
import mahjong as mj
from learning import Isokun
from point import TadaAi
import graphic as gp

# ウィンドウを作成
root = tk.Tk()
root.title("Iso-kun")
size = 13 * gp.MJHAI_HEIGHT + 5 * gp.MJHAI_WIDTH + 4
root.geometry(str(size) + "x" + str(size))
root.resizable(0, 0)

# 画像表示部
screen = tk.Label(root)
screen.grid()

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
players = [mj.Human("Player1"), Isokun("Player2"), TadaAi("Player3")]

# ゲームスタート
yama = mjhai_set[:]
random.shuffle(yama)

# 配牌
for player in players:
    player.haipai(yama)

cur_player = 0

while len(yama) > 14:
    player = players[cur_player]
    player.tumo(yama)

    # 画面描画
    screen_img = gp.draw_screen(players, cur_player)
    screen.configure(image=screen_img)

    # 打牌
    player.tehai.show()
    select_index = player.select(players)
    player.dahai(select_index)
    print()

    cur_player = (cur_player + 1) % len(players)

print("終了")
