import tkinter as tk
import mahjong as mj

# 麻雀牌のサイズ
MJHAI_WIDTH = 30
MJHAI_HEIGHT = 38

mjhai_img = {}

# 画像ファイル読み込み
def load_image(mjhai_list):
    for hai in mjhai_list:
        file_img = "image/" + hai.name + ".png"
        mjhai_img[hai.name] = tk.PhotoImage(file=file_img)

# 手牌を表示
def show_tehai(canvas, player):
    # 河
    x = 0
    y = 0
    for hai in player.kawa:
        canvas.create_image(
            x * MJHAI_WIDTH + 4 * MJHAI_HEIGHT + 2,
            y * MJHAI_HEIGHT + 6 * MJHAI_WIDTH + 2,
            image=mjhai_img[hai.name],
            anchor=tk.NW
        )

        x += 1
        if x >= 6:
            x = 0
            y += 1

    # 手牌
    for i, hai in enumerate(player.tehai):
        canvas.create_text(
            (i - 3.5) * MJHAI_WIDTH + 4 * MJHAI_HEIGHT + 2,
            5 * MJHAI_HEIGHT + 6 * MJHAI_WIDTH - 10,
            text=str(i)
        )

        canvas.create_image(
            (i - 4) * MJHAI_WIDTH + 4 * MJHAI_HEIGHT + 2,
            5 * MJHAI_HEIGHT + 6 * MJHAI_WIDTH + 2,
            image=mjhai_img[hai.name],
            anchor=tk.NW
        )
