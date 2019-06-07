import os
import time
import glob
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np
import cv2
from .. import core as mj

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

# Pillow→OpenCV変換
def pil2cv(image):
    new_image = np.array(image)
    if new_image.shape[2] == 3: # カラー
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4: # 透過
        new_image = new_image[:, :, [2, 1, 0, 3]]
    return new_image

# 横向きの麻雀牌を生成
def draw_side(img):
    w, h = img.size
    create_img = Image.new("RGBA", (h, h))

    rotate_img = img.rotate(90, expand=True)
    create_img.paste(rotate_img, (0, h - w))

    return create_img

# 手牌の画像を生成
def draw_tehai(tehai, back=False):
    create_img = Image.new("RGBA", (14 * MJHAI_WIDTH + 4 * MJHAI_HEIGHT, 2 * MJHAI_HEIGHT))

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
        mjhai_draw = mjhai_img["back" if back else hai.name]

        # 他家からの牌は横にする
        if hai.furo:
            create_img.paste(draw_side(mjhai_draw), (x, MJHAI_HEIGHT))
            x += MJHAI_HEIGHT
        else:
            create_img.paste(mjhai_draw, (x, MJHAI_HEIGHT))
            x += MJHAI_WIDTH

    x = create_img.size[0]
    for cur_furo in tehai.furo:
        for hai in cur_furo:
            # 麻雀牌
            mjhai_draw = mjhai_img[hai.name]

            # 他家からの牌は横にする
            if hai.furo:
                create_img.paste(draw_side(mjhai_draw), (x - MJHAI_HEIGHT, MJHAI_HEIGHT))
                x -= MJHAI_HEIGHT
            else:
                create_img.paste(mjhai_draw, (x - MJHAI_WIDTH, MJHAI_HEIGHT))
                x -= MJHAI_WIDTH

    return create_img

# 河の画像を生成
def draw_kawa(kawa):
    create_img = Image.new("RGBA", (5 * MJHAI_WIDTH + MJHAI_HEIGHT, 4 * MJHAI_HEIGHT))
    tumogiri_img = Image.new("RGBA", (MJHAI_WIDTH, MJHAI_HEIGHT), (0, 0, 0, 47))
    furo_img = Image.new("RGBA", (MJHAI_WIDTH, MJHAI_HEIGHT), (255, 63, 63, 47))

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
            create_img.paste(draw_side(paste_img), (x, y))
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
def draw_screen(game, view, open=False, uradora=False):
    create_img = Image.new("RGB", (SCREEN_SIZE, SCREEN_SIZE), "green")

    for player in game.players:
        paste_img = Image.new("RGBA", (SCREEN_SIZE, SCREEN_SIZE))

        # 手牌
        tehai_img = draw_tehai(player.tehai, False if open else player != view)
        paste_img.paste(
            tehai_img,
            (SCREEN_SIZE - tehai_img.size[0], 7 * MJHAI_WIDTH + 10 * MJHAI_HEIGHT)
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
        if player.chicha == view or open:
            shaten_draw = ImageDraw.Draw(paste_img)
            shaten_draw.font = ImageFont.truetype(FONT_FILE, 16)
            w, h = shaten_draw.textsize("{}ST".format(player.tehai.shanten()))

            shaten_draw.text(
                (SCREEN_SIZE - tehai_img.size[0], SCREEN_SIZE - tehai_img.size[1]),
                "{}ST".format(player.tehai.shanten())
            )

        # 回転&合成
        rotate_img = paste_img.rotate((player.chicha - view.chicha) * 90)
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

class Screen():
    def __init__(self, game, open=False, view=None):
        self.game = game
        self.view = view
        self.open = open

        # ウィンドウ名
        if view is None:
            self.win_name = mj.APP_NAME
        else:
            self.win_name = "{} [{}]".format(mj.APP_NAME, view.name)

    # 画面描画
    def draw(self):
        cur_view = self.game.cur_player if self.view is None else self.view
        img = pil2cv(draw_screen(self.game, cur_view, self.open))
        cv2.imshow(self.win_name, img)
        cv2.waitKey(1)

    # 流局後画面描画
    def draw_ryukyoku(self):
        cur_view = self.game.cur_player if self.view is None else self.view
        img = pil2cv(draw_screen(self.game, cur_view, True, True))
        cv2.imshow(self.win_name, img)
        cv2.waitKey(0)
