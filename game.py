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

# 全ての牌をセット
# 筒子・索子
mjhai_set = []
for i in range(2):
    for j in range(1, 10):
        mjhai_set.extend(mj.MjHai(i, j) for k in range(4))

# 萬子
mjhai_set.extend(mj.MjHai(2, 1) for i in range(4))
mjhai_set.extend(mj.MjHai(2, 9) for i in range(4))

# 字牌
for i in range(3, 10):
    mjhai_set.extend(mj.MjHai(i) for j in range(4))

# プレイヤー
players = [mp.Tenari("Tenari1"), mp.Tenari("Tenari2"), mp.Tenari("Tenari3")]
#players = [mp.Human("Tenari1"), mp.Human("Tenari2"), mp.Human("Tenari3")]

game = mj.Game(mjhai_set, players)
print(game.kyoku_name())
print()

# 配牌
for player in game.players:
    player.haipai()

view = 0 # 視点
open_tehai = True

while len(game.yama) > 0:
    #view = game.cur_player.chicha

    # 自摸
    game.cur_player.tumo()

    # コンソール表示
    print("{} [残り{}]".format(game.cur_player.name, len(game.yama)))
    game.cur_player.tehai.show()

    # ツモ判定
    if game.cur_player.check_self():
        print()
        print("{}：ツモ".format(game.cur_player.name))

        yaku_agari = game.cur_player.tehai.yaku()
        for yakus in yaku_agari:
            for yaku in yakus:
                print(mj.yaku_list[yaku].fan[0], mj.yaku_list[yaku].name)
            print()

        break

    # 画面描画
    screen_img = ImageTk.PhotoImage(gp.draw_screen(game, view, open_tehai))
    screen.configure(image=screen_img)
    root.update()

    # 打牌
    game.cur_player.dahai()
    print()

    # ロン判定
    end_flag = False
    for check_player in game.players:
        # 自身は判定しない
        if check_player != game.cur_player:
            if check_player.check_other(game.cur_player):
                end_flag = True
                print("{}→{}：ロン".format(game.cur_player.name, check_player.name))

                yaku_agari = check_player.tehai.yaku()
                for yakus in yaku_agari:
                    for yaku in yakus:
                        print(mj.yaku_list[yaku].fan[0], mj.yaku_list[yaku].name)
                    print()
    
    # 画面描画
    screen_img = ImageTk.PhotoImage(gp.draw_screen(game, view, open_tehai))
    screen.configure(image=screen_img)
    root.update()

    if end_flag:
        break

    # 次のプレイヤーへ
    game.next_player()
else:
    print("流局")

# 手牌をオープンして描画
screen_img = ImageTk.PhotoImage(gp.draw_screen(game, view, True, True))
screen.configure(image=screen_img)
root.update()

root.mainloop()
#while input("> ") != "q":
#    root.update()
