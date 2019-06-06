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
#players = [mp.Tenari("Tenari1"), mp.Tenari("Tenari2"), mp.Tenari("Tenari3")]
#players = [mp.Human("Human1"), mp.Human("Human2"), mp.Human("Human3")]

human = mp.Human("Human")
players = [human, mp.Tenari("Tenari1"), mp.Tenari("Tenari2")]

game = mj.Game(mjhai_set, players)
print(game.kyoku_name())
print()

# 配牌
game.haipai()

view = human.chicha # 視点
open_tehai = False

while len(game.yama) > 0:
    #view = game.cur_player.chicha

    # ツモ
    if game.tumo():
        print("{}：ツモ".format(game.cur_player.name))
        break

    # コンソール表示
    print("{} [残り{}]".format(game.cur_player.name, len(game.yama)))
    game.cur_player.tehai.show()

    # 画面描画
    screen_img = ImageTk.PhotoImage(gp.draw_screen(game, view, open_tehai))
    screen.configure(image=screen_img)
    root.update()

    # 打牌
    if game.dahai():
        print("{}：ロン".format(game.cur_player.name))
        break

    print()
    
    # 画面描画
    screen_img = ImageTk.PhotoImage(gp.draw_screen(game, view, open_tehai))
    screen.configure(image=screen_img)
    root.update()

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
