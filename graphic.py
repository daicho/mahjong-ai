import tkinter as tk
from PIL import Image
import mahjong as mj

# 麻雀牌のサイズ
MJHAI_WIDTH = 30
MJHAI_HEIGHT = 38

mjhai_img = {}

# 画像ファイル読み込み
def load_image(mjhai_list):
    for hai in mjhai_list:
        img_name = "image/" + hai.name + ".png"
        mjhai_img[hai.name] = Image.open(img_name)

# 手牌の画像を生成
def draw_tehai(tehai):
    create_img = Image.new(PIL.RGB, (14 * MJHAI_WIDTH, MJHAI_HEIGHT))

    x = 0
    for hai in tehai:
        create_img.paste(mjhai_img[hai.name], (x * MJHAI_WIDTH, 0))
        x += 1

    return create_img

# 河の画像を生成
def draw_kawa(kawa):
    create_img = Image.new(PIL.RGB, (5 * MJHAI_WIDTH + MJHAI_HEIGHT, 4 * MJHAI_HEIGHT))

    x = 0
    y = 0
    for hai in kawa:
        create_img.paste(mjhai_img[hai.name], (x * MJHAI_WIDTH, y * MJHAI_HEIGHT))
        x += 1
        if x >= 6:
            x = 0
            y += 1

    return create_img
