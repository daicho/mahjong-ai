import sys
import time
import random
import tkinter as tk
from PIL import ImageTk
import mahjong as mj

"""
import mahjong.core as mj
import mahjong.graphic as gp

from mahjong.core import Human
from mahjong.learning import Isokun, Fast
from mahjong.point import TadaAi
"""

# ウィンドウを作成
root = tk.Tk()
root.title("Mahjong")
size = 13 * mj.MJHAI_HEIGHT + 5 * mj.MJHAI_WIDTH + 4
root.geometry(str(size) + "x" + str(size) + "+0+0")
root.resizable(0, 0)

# 画像表示部
screen = tk.Label(root)
screen.grid()

# 全ての牌をセット
# 筒子・索子
mjhai_list = []
for i in range(2):
    for j in range(1, 10):
        mjhai_list.extend([mj.MjHai(i, j) for k in range(4)])

# 萬子
mjhai_list.extend([mj.MjHai(2, 1) for i in range(4)])
mjhai_list.extend([mj.MjHai(2, 9) for i in range(4)])

# 字牌
for i in range(3, 10):
    mjhai_list.extend([mj.MjHai(i) for j in range(4)])

mj.load_image(mjhai_list)
players = [mj.Human("Human"), mj.Isokun("Iso-kun"), mj.TadaAi("Tada Ai")]
view = 0 # 視点

# ゲームスタート
yama = mj.Yama(mjhai_list)

# 配牌
for player in players:
    player.haipai(yama)

cur_player = 0

while len(yama) > 14:
    player = players[cur_player]
    player.tumo(yama)

    # 画面描画
    screen_img = ImageTk.PhotoImage(mj.draw_screen(players, view, True))
    screen.configure(image=screen_img)
    root.update()
    #time.sleep(0.5)

    if player.tehai.shanten() == -1:
        print("アガリ！")
        break

    # 打牌
    player.tehai.show()
    select_index = player.select(players, yama)
    player.dahai(select_index)
    print()

    # 画面描画
    screen_img = ImageTk.PhotoImage(mj.draw_screen(players, view, True))
    screen.configure(image=screen_img)
    root.update()
    #time.sleep(0.5)

    # 次のプレイヤーへ
    cur_player = (cur_player + 1) % len(players)

print("終了")

root.mainloop()
#while input("> ") != "q":
#    root.update()
