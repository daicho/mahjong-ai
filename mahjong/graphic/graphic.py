import os
import copy
import glob
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
from .. import core

# 麻雀牌のサイズ
MJHAI_WIDTH = 30
MJHAI_HEIGHT = 38
SCREEN_SIZE = 12 * MJHAI_HEIGHT + 7 * MJHAI_WIDTH

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
    create_img = Image.new("RGBA", (15 * MJHAI_WIDTH, 2 * MJHAI_HEIGHT))

    x = 0
    for i, hai in enumerate(tehai.list):
        # ツモった牌は離す
        if i == 13 - len(tehai.furo) * 3:
            x += int(MJHAI_WIDTH / 4)

        # 番号
        if not back:
            number_draw = ImageDraw.Draw(create_img)
            number_draw.font = ImageFont.truetype(FONT_FILE, 12)
            w, h = number_draw.textsize(str(i))

            number_draw.text(
                (x + (MJHAI_WIDTH - w) / 2, MJHAI_HEIGHT - h - 4),
                str(i)
            )

        # 麻雀牌
        draw_mjhai = mjhai_img["back"] if back else mjhai_img[hai.name]

        # 他家からの牌は横にする
        if hai.furo:
            rotate_img = draw_mjhai.rotate(90, expand=True)
            create_img.paste(rotate_img, (x, 2 * MJHAI_HEIGHT - MJHAI_WIDTH))
            x += MJHAI_HEIGHT
        else:
            create_img.paste(draw_mjhai, (x, MJHAI_HEIGHT))
            x += MJHAI_WIDTH

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
def draw_screen(game, view, open_tehai=False, uradora=False):
    create_img = Image.new("RGB", (SCREEN_SIZE, SCREEN_SIZE), "green")

    for player in game.players:
        paste_img = Image.new("RGBA", (SCREEN_SIZE, SCREEN_SIZE))

        # 手牌
        tehai_img = draw_tehai(player.tehai, False if open_tehai else player.chicha != view)
        paste_img.paste(
            tehai_img,
            (6 * MJHAI_HEIGHT - int(3.5 * MJHAI_WIDTH), 7 * MJHAI_WIDTH + 10 * MJHAI_HEIGHT)
        )

        # 河
        kawa_img = draw_kawa(player.kawa)
        paste_img.paste(
            kawa_img,
            (6 * MJHAI_HEIGHT + int(0.5 * MJHAI_WIDTH), 7 * MJHAI_WIDTH + 6 * MJHAI_HEIGHT)
        )

        # プレイヤー名
        name_draw = ImageDraw.Draw(paste_img)
        name_draw.font = ImageFont.truetype(FONT_FILE, 16)
        w, h = name_draw.textsize("{} [{}]".format(player.name, player.point))

        name_draw.text(
            ((SCREEN_SIZE - w) / 2, 6.5 * MJHAI_WIDTH + 6 * MJHAI_HEIGHT - h / 2),
            "{} [{}]".format(player.name, player.point)
        )

        # シャンテン数
        if player.chicha == view or open_tehai:
            shaten_draw = ImageDraw.Draw(paste_img)
            shaten_draw.font = ImageFont.truetype(FONT_FILE, 16)
            w, h = shaten_draw.textsize("{}ST".format(player.tehai.shanten()))

            shaten_draw.text(
                (SCREEN_SIZE - w - 3, SCREEN_SIZE - h - 3),
                "{}ST".format(player.tehai.shanten())
            )

        # 回転&合成
        rotate_img = paste_img.rotate((player.chicha - view) * 90)
        create_img.paste(rotate_img, (0, 0), rotate_img)

    # 局
    kyoku_draw = ImageDraw.Draw(create_img)
    kyoku_draw.font = ImageFont.truetype(FONT_FILE, 24)
    w, h = kyoku_draw.textsize(game.kyoku_name())

    kyoku_draw.text(
        ((SCREEN_SIZE - w) / 2, 6 * MJHAI_HEIGHT + MJHAI_WIDTH),
        game.kyoku_name()
    )

    # ドラ
    for i in range(2):
        for j in range(5):
            if (uradora or i == 0) and j == 0:
                paste_img = mjhai_img[game.yama.list[i + j * 2].name]
            else:
                paste_img = mjhai_img["back"]

            create_img.paste(
                paste_img,
                (6 * MJHAI_HEIGHT + (j + 1) * MJHAI_WIDTH, 6 * MJHAI_WIDTH + (i + 4) * MJHAI_HEIGHT)
            )

    return create_img
