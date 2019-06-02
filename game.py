import time
import tkinter as tk
from PIL import ImageTk
import mahjong as mj

# ウィンドウを作成
root = tk.Tk()
root.title("Mahjong")
size = 13 * mj.MJHAI_HEIGHT + 5 * mj.MJHAI_WIDTH + 4
root.geometry("{}x{}+0+0".format(size, size))
root.resizable(0, 0)

# 画像表示部
screen = tk.Label(root)
screen.grid()

# プレイヤー
players = [mj.Tenari("Tenari"), mj.Tenari("Tenari"), mj.Tenari("Tenari")]

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
cur_player = 0

while len(yama) > 14:
    # 自摸
    player = players[cur_player]
    player.tumo(yama)

    if player.tehai.shanten() == -1:
        print("アガリ！")
        break

    # 画面描画
    screen_img = ImageTk.PhotoImage(mj.draw_screen(players, view, True))
    screen.configure(image=screen_img)
    root.update()

    # コンソール表示
    print("{} [残り{}]".format(player.name, len(yama)))
    player.tehai.show()

    # 打牌
    select_index = player.select(players, mjhai_set)
    player.dahai(select_index)
    print()

    # 画面描画
    screen_img = ImageTk.PhotoImage(mj.draw_screen(players, view, True))
    screen.configure(image=screen_img)
    root.update()

    # 次のプレイヤーへ
    cur_player = (cur_player + 1) % len(players)

# 手牌をオープンして描画
screen_img = ImageTk.PhotoImage(mj.draw_screen(players, view, True))
screen.configure(image=screen_img)
root.update()

print("終了")
root.mainloop()
#while input("> ") != "q":
#    root.update()
