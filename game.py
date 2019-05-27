import sys
import random
import tkinter as tk
import mahjong as mj
import graphic as gp

# 摸打
def callback(select):
    def mouda():
        global player
        global cur_player

        # 打牌
        player.dahai(select)

        # 終了判定
        if len(yama) <= 14:
            root.destroy()
            sys.exit()

        # 次のプレイヤーへ
        cur_player = (cur_player + 1) % len(players)
        player = players[cur_player]
        player.tumo(yama)

        # 画面描画
        screen_img = gp.draw_screen(players, cur_player)
        screen.configure(image=screen_img)

        root.mainloop()

    return mouda

# ウィンドウを作成
root = tk.Tk()
root.title("Iso-kun")
size = 13 * gp.MJHAI_HEIGHT + 5 * gp.MJHAI_WIDTH + 4
root.geometry(str(size) + "x" + str(size))
root.resizable(0, 0)

# 画像表示部
screen = tk.Label(root)
screen.grid()

# 選択ボタン
select_button = []
for i in range(14):
    select_button.append(tk.Button(root, text=str(i), command=callback(i)))
    select_button[i].place(
        x = 6 * gp.MJHAI_HEIGHT + (i - 4) * gp.MJHAI_WIDTH + 2,
        y = 4 * gp.MJHAI_WIDTH + 12 * gp.MJHAI_HEIGHT + 2,
        width = gp.MJHAI_WIDTH,
        height = gp.MJHAI_WIDTH
    )

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

# ゲームスタート
cur_player = 0
player = players[cur_player]
player.tumo(yama)

# 画面描画
screen_img = gp.draw_screen(players, cur_player)
screen.configure(image=screen_img)

root.mainloop()
