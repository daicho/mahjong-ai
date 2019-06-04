import time
import tkinter as tk
from PIL import ImageTk

import mahjong.core as mj
import mahjong.player as mp
import mahjong.graphic as gp

# ウィンドウを作成
root = tk.Tk()
root.title("Mahjong")
root.geometry("{0}x{0}+0+0".format(gp.SCREEN_SIZE + 4))
root.resizable(0, 0)

# 画像表示部
screen = tk.Label(root)
screen.grid()

# プレイヤー
players = [mp.Tenari("Tenari1", 0), mp.Tenari("Tenari2", 1), mp.Tenari("Tenari3", 2)]
#players = [mp.Human("Human", 0), mp.Tenari("Tenari1", 1), mp.Tenari("Tenari2", 2)]

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

# 山積み
yama = mj.Yama(mjhai_set)

# 配牌
for player in players:
    player.haipai(yama)

view = 0 # 視点
open_tehai = True
cur_player = 0

while len(yama) > 14:
    #view = cur_player

    # 自摸
    player = players[cur_player]
    player.tumo(yama)

    # コンソール表示
    print("{} [残り{}]".format(player.name, len(yama) - 14))
    player.tehai.show()

    # 画面描画
    screen_img = ImageTk.PhotoImage(gp.draw_screen(players, view, yama, open_tehai))
    screen.configure(image=screen_img)
    root.update()

    # ツモ判定
    if player.agari_tumo():
        print()
        print("{}：ツモ".format(player.name))
        player.tehai.yaku()
        break

    # 打牌
    select_index = player.select(players, mjhai_set)
    player.dahai(select_index)
    print()

    # 画面描画
    screen_img = ImageTk.PhotoImage(gp.draw_screen(players, view, yama, open_tehai))
    screen.configure(image=screen_img)
    root.update()

    # ロン判定
    end_flag = False
    for check_player in players:
        # 自身は判定しない
        if check_player != player:
            if check_player.agari_ron(player):
                print("{}→{}：ロン".format(player.name, check_player.name))
                check_player.tehai.yaku()
                end_flag = True
    
    if end_flag:
        break

    # 次のプレイヤーへ
    cur_player = (cur_player + 1) % len(players)

# 手牌をオープンして描画
screen_img = ImageTk.PhotoImage(gp.draw_screen(players, view, yama, True, True))
screen.configure(image=screen_img)
root.update()

print("終了")
root.mainloop()
#while input("> ") != "q":
#    root.update()
