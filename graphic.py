import tkinter as tk
import mahjong as mj

# 麻雀牌のサイズ
MJHAI_WIDTH = 30
MJHAI_HEIGHT = 40

mjhai_img = {}

# 画像ファイル読み込み
def load_image(mjhai_list):
    for hai in mjhai_list:
        file_img = "image/" + hai.name + ".gif"
        mjhai_img[hai.name] = tk.PhotoImage(file=file_img)

# 手牌を表示
def show_tehai(canvas, player):
    # 河
    x = 0
    y = 0
    for hai in player.kawa:
        canvas.create_image(
            x * MJHAI_WIDTH + 3,
            y * MJHAI_HEIGHT + 3,
            image=mjhai_img[hai.name],
            anchor=tk.NW
        )

        x += 1
        if x >= 6:
            x = 0
            y += 1

    # 手牌
    x = 0
    for hai in player.tehai:
        canvas.create_image(
            x * MJHAI_WIDTH + 3,
            MJHAI_HEIGHT * 5 + 3,
            image=mjhai_img[hai.name],
            anchor=tk.NW
        )
        x += 1
