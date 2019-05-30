import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
from mahjong.core import *

# 麻雀牌のサイズ
MJHAI_WIDTH = 30
MJHAI_HEIGHT = 38

font_file = "font/YuGothB.ttc"

mjhai_img = {}
mjhai_img["back"] = Image.open("image/back.png")

# 画像ファイル読み込み
def load_image(mjhai_set):
    for hai in mjhai_set:
        if hai.name not in mjhai_img:
            mjhai_img[hai.name] = Image.open("image/" + hai.name + ".png")

# 手牌の画像を生成
def draw_tehai(tehai, back_flag=False):
    create_img = Image.new("RGBA", (14 * MJHAI_WIDTH, 2 * MJHAI_HEIGHT))

    x = 0
    for hai in tehai.list:
        # 番号
        number_draw = ImageDraw.Draw(create_img)
        number_draw.font = ImageFont.truetype(font_file, 12)

        w, h = number_draw.textsize(str(x))
        number_draw.text(
            ((x + 0.5) * MJHAI_WIDTH - w / 2, MJHAI_HEIGHT - 16),
            str(x)
        )

        # 麻雀牌
        draw_mjhai = mjhai_img["back"] if back_flag else mjhai_img[hai.name]
        create_img.paste(draw_mjhai, (x * MJHAI_WIDTH, MJHAI_HEIGHT))

        x += 1

    return create_img

# 河の画像を生成
def draw_kawa(kawa):
    create_img = Image.new("RGBA", (5 * MJHAI_WIDTH + MJHAI_HEIGHT, 4 * MJHAI_HEIGHT))
    gray_img = Image.new("RGBA", (MJHAI_WIDTH, MJHAI_HEIGHT), (0, 0, 0, 47))

    x = 0
    y = 0
    for hai in kawa.list:
        create_img.paste(mjhai_img[hai.name], (x * MJHAI_WIDTH, y * MJHAI_HEIGHT))

        # ツモ切り
        if hai.tumogiri:
            create_img.paste(gray_img, (x * MJHAI_WIDTH, y * MJHAI_HEIGHT), gray_img)

        x += 1
        if x >= 6:
            x = 0
            y += 1

    return create_img

# ゲーム画面の画像を生成
def draw_screen(players, target, open=False):
    size = 13 * MJHAI_HEIGHT + 5 * MJHAI_WIDTH
    create_img = Image.new("RGB", (size, size), "green")

    for i, player in enumerate(players):
        kawa_img = draw_kawa(player.kawa)
        tehai_img = draw_tehai(player.tehai, False if open else i != target)

        # 河と手牌を合成
        paste_img = Image.new("RGBA", (size, size))
        paste_img.paste(
            kawa_img,
            (6 * MJHAI_HEIGHT, 5 * MJHAI_WIDTH + 7 * MJHAI_HEIGHT)
        )
        paste_img.paste(
            tehai_img,
            (6 * MJHAI_HEIGHT - 4 * MJHAI_WIDTH, 5 * MJHAI_WIDTH + 11 * MJHAI_HEIGHT)
        )

        # プレイヤー名
        name_draw = ImageDraw.Draw(paste_img)
        name_draw.font = ImageFont.truetype(font_file, 16)

        w, h = name_draw.textsize(player.name)
        name_draw.text(
            ((size - w) / 2, 5 * MJHAI_WIDTH + 7 * MJHAI_HEIGHT - h - 5),
            player.name
        )

        # シャンテン数
        if i == target or open:
            shaten_draw = ImageDraw.Draw(paste_img)
            shaten_draw.font = ImageFont.truetype(font_file, 16)

            w, h = shaten_draw.textsize("{}シャンテン".format(player.tehai.shanten()))
            shaten_draw.text(
                (size - w - 3, size - h - 3),
                "{}シャンテン".format(player.tehai.shanten())
            )

        # 回転&合成
        rotate_img = paste_img.rotate((i - target) * 90)
        create_img.paste(rotate_img, (0, 0), rotate_img)

    return create_img
