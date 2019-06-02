import os
import copy
import glob
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
from .core import *

# 麻雀牌のサイズ
MJHAI_WIDTH = 30
MJHAI_HEIGHT = 38

# フォントファイル
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = THIS_PATH + "/font/YuGothB.ttc"

# 画像ファイル読み込み
mjhai_img = {}
mjhai_files = glob.glob(THIS_PATH + "/mjhai/*.png") # ファイル一覧を取得

for mjhai_file in mjhai_files:
    img_key, ext = os.path.splitext(os.path.basename(mjhai_file)) # ファイル名を抽出
    mjhai_img[img_key] = Image.open(mjhai_file)

# 手牌の画像を生成
def draw_tehai(tehai, back=False):
    create_img = Image.new("RGBA", (14 * MJHAI_WIDTH, 2 * MJHAI_HEIGHT))

    i = 0
    for hai in tehai.list:
        # 番号
        if not back:
            number_draw = ImageDraw.Draw(create_img)
            number_draw.font = ImageFont.truetype(FONT_FILE, 12)

            w, h = number_draw.textsize(str(i))
            number_draw.text(
                ((i + 0.5) * MJHAI_WIDTH - w / 2, MJHAI_HEIGHT - 16),
                str(i)
            )

        # 麻雀牌
        draw_mjhai = mjhai_img["back"] if back else mjhai_img[hai.name]
        create_img.paste(draw_mjhai, (i * MJHAI_WIDTH, MJHAI_HEIGHT))

        i += 1

    return create_img

# 河の画像を生成
def draw_kawa(kawa):
    create_img = Image.new("RGBA", (5 * MJHAI_WIDTH + MJHAI_HEIGHT, 4 * MJHAI_HEIGHT))
    tumogiri_img = Image.new("RGBA", (MJHAI_WIDTH, MJHAI_HEIGHT), (0, 0, 0, 47))
    furo_img = Image.new("RGBA", (MJHAI_WIDTH, MJHAI_HEIGHT), (255, 0, 0, 47))

    x = 0
    y = 0
    already_richi = False

    for hai in kawa.list:
        paste_img = Image.new("RGBA", (MJHAI_WIDTH, MJHAI_HEIGHT))
        paste_img.paste(mjhai_img[hai.name])

        # ツモ切りは暗くする
        if hai.tumogiri:
            paste_img.paste(tumogiri_img, (0, 0), tumogiri_img)

        # 鳴かれた牌は赤くする
        if hai.furo:
            paste_img.paste(furo_img, (0, 0), furo_img)

        # リーチ宣言牌は横にする
        if not already_richi and hai.richi:
            already_richi = True
            rotate_img = paste_img.rotate(90, expand=True)
            create_img.paste(rotate_img, (x, y + MJHAI_HEIGHT - MJHAI_WIDTH))
            x += MJHAI_HEIGHT
        else:
            create_img.paste(paste_img, (x, y))
            x += MJHAI_WIDTH

        # 6枚で改行
        if x >= 6 * MJHAI_WIDTH:
            x = 0
            y += MJHAI_HEIGHT

    return create_img

# ゲーム画面の画像を生成
def draw_screen(players, target, open=False):
    size = 13 * MJHAI_HEIGHT + 5 * MJHAI_WIDTH
    create_img = Image.new("RGB", (size, size), "green")

    for i, player in enumerate(players):
        paste_img = Image.new("RGBA", (size, size))

        # 手牌
        tehai_img = draw_tehai(player.tehai, False if open else i != target)
        paste_img.paste(
            tehai_img,
            (6 * MJHAI_HEIGHT - 4 * MJHAI_WIDTH, 5 * MJHAI_WIDTH + 11 * MJHAI_HEIGHT)
        )

        # 河
        kawa_img = draw_kawa(player.kawa)
        paste_img.paste(
            kawa_img,
            (6 * MJHAI_HEIGHT, 5 * MJHAI_WIDTH + 7 * MJHAI_HEIGHT)
        )

        # プレイヤー名
        name_draw = ImageDraw.Draw(paste_img)
        name_draw.font = ImageFont.truetype(FONT_FILE, 16)

        w, h = name_draw.textsize(player.name)
        name_draw.text(
            ((size - w) / 2, 5 * MJHAI_WIDTH + 7 * MJHAI_HEIGHT - h - 5),
            player.name
        )

        # シャンテン数
        if i == target or open:
            shaten_draw = ImageDraw.Draw(paste_img)
            shaten_draw.font = ImageFont.truetype(FONT_FILE, 16)

            w, h = shaten_draw.textsize("{}ST".format(player.tehai.shanten()))
            shaten_draw.text(
                (size - w - 3, size - h - 3),
                "{}ST".format(player.tehai.shanten())
            )

        # 回転&合成
        rotate_img = paste_img.rotate((i - target) * 90)
        create_img.paste(rotate_img, (0, 0), rotate_img)

    return create_img
