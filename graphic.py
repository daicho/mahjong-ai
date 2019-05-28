import tkinter as tk
from PIL import Image, ImageTk
import mahjong as mj

# 麻雀牌のサイズ
MJHAI_WIDTH = 30
MJHAI_HEIGHT = 38

mjhai_img = {}
mjhai_back = Image.open("image/back.png")

# 画像ファイル読み込み
def load_image(mjhai_list):
    for hai in mjhai_list:
        mjhai_img[hai.name] = Image.open("image/" + hai.name + ".png")

# 手牌の画像を生成
def draw_tehai(tehai):
    create_img = Image.new("RGBA", (14 * MJHAI_WIDTH, MJHAI_HEIGHT))

    x = 0
    for hai in tehai:
        create_img.paste(mjhai_img[hai.name], (x * MJHAI_WIDTH, 0))
        x += 1

    return create_img

# 裏返しの手牌の画像を生成
def draw_back(tehai):
    create_img = Image.new("RGBA", (14 * MJHAI_WIDTH, MJHAI_HEIGHT))

    x = 0
    for hai in tehai:
        create_img.paste(mjhai_back, (x * MJHAI_WIDTH, 0))
        x += 1

    return create_img

# 河の画像を生成
def draw_kawa(kawa):
    create_img = Image.new("RGBA", (5 * MJHAI_WIDTH + MJHAI_HEIGHT, 4 * MJHAI_HEIGHT))

    x = 0
    y = 0
    for hai in kawa:
        create_img.paste(mjhai_img[hai.name], (x * MJHAI_WIDTH, y * MJHAI_HEIGHT))
        x += 1
        if x >= 6:
            x = 0
            y += 1

    return create_img

# ゲーム画面の画像を生成
def draw_screen(players, target):
    size = 13 * MJHAI_HEIGHT + 5 * MJHAI_WIDTH
    create_img = Image.new("RGB", (size, size), (0, 127, 0))

    for i, player in enumerate(players):
        kawa_img = draw_kawa(player.kawa)
        tehai_img = draw_tehai(player.tehai) if i == target else draw_back(player.tehai)

        # 河と手牌を合成
        paste_img = Image.new("RGBA", (size, size))
        paste_img.paste(
            kawa_img,
            (6 * MJHAI_HEIGHT, 5 * MJHAI_WIDTH + 7 * MJHAI_HEIGHT)
        )
        paste_img.paste(
            tehai_img,
            (6 * MJHAI_HEIGHT - 4 * MJHAI_WIDTH, 5 * MJHAI_WIDTH + 12 * MJHAI_HEIGHT)
        )

        # 回転&合成
        rotate_img = paste_img.rotate((i - target) * 90)
        create_img.paste(rotate_img, (0, 0), rotate_img.split()[3])

    return ImageTk.PhotoImage(create_img)
