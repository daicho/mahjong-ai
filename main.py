import mahjong.core as mj
import mahjong.players as mp
import mahjong.graphic as gp

# 牌をセット
# 筒子・索子
mjhai_set = []
for i in range(2):
    for j in range(1, 10):
        mjhai_set.extend(mj.MjHai((i, j), j == 5 and k == 3) for k in range(4))

# 萬子
mjhai_set.extend(mj.MjHai((2, 1)) for i in range(4))
mjhai_set.extend(mj.MjHai((2, 9)) for i in range(4))

# 字牌
for i in range(3, 10):
    mjhai_set.extend(mj.MjHai((i, 0)) for j in range(4))

# 役
yakus = {
    mj.Yaku.DORA:       (1, 1, False),   # ドラ
    mj.Yaku.URADORA:    (1, 0, False),   # 裏ドラ
    mj.Yaku.AKADORA:    (1, 1, False),   # 赤ドラ
    mj.Yaku.RICHI:      (1, 0, False),   # 立直
    mj.Yaku.TSUMO:      (1, 0, False),   # ツモ
    mj.Yaku.IPPATSU:    (1, 0, False),   # 一発
    mj.Yaku.PINFU:      (1, 0, False),   # 平和
    mj.Yaku.IPEKO:      (1, 0, False),   # 一盃口
    mj.Yaku.TANYAO:     (1, 0, False),   # タンヤオ
    mj.Yaku.YAKUHAI:    (1, 1, False),   # 役牌
    mj.Yaku.HAITEI:     (1, 1, False),   # 海底摸月
    mj.Yaku.HOUTEI:     (1, 1, False),   # 河底撈魚
    mj.Yaku.RINSYAN:    (1, 1, False),   # 嶺上開花
    mj.Yaku.CHANKAN:    (1, 1, False),   # 槍槓
    mj.Yaku.DABURI:     (1, 0, False),   # ダブル立直
    mj.Yaku.ITTSU:      (2, 1, False),   # 一気通貫
    mj.Yaku.CHANTA:     (2, 1, False),   # チャンタ
    mj.Yaku.DOUJUN:     (2, 1, False),   # 三色同順
    mj.Yaku.DOUKO:      (2, 2, False),   # 三色同刻
    mj.Yaku.SANANKO:    (2, 2, False),   # 三暗刻
    mj.Yaku.SANKANTSU:  (2, 2, False),   # 三槓子
    mj.Yaku.TOITOI:     (2, 2, False),   # 対々和
    mj.Yaku.SHOUSANGEN: (2, 2, False),   # 小三元
    mj.Yaku.HONRO:      (2, 2, False),   # 混老頭
    mj.Yaku.CHITOI:     (2, 0, False),   # 七対子
    mj.Yaku.RYANPEKO:   (3, 0, False),   # 二盃口
    mj.Yaku.JUNCHAN:    (3, 2, False),   # 純チャン
    mj.Yaku.HONITSU:    (3, 2, False),   # 混一色
    #mj.Yaku.NAGASHI:    (5, 0, False),   # 流し満貫
    mj.Yaku.CHINITSU:   (6, 5, False),   # 清一色
    mj.Yaku.KOKUSHI:    (13, 0, True),  # 国士無双
    mj.Yaku.SUANKO:     (13, 0, True),  # 四暗刻
    mj.Yaku.TSUISO:     (13, 13, True), # 字一色
    mj.Yaku.DAISANGEN:  (13, 13, True), # 大三元
    mj.Yaku.DAISUSHI:   (26, 26, True), # 大四喜
    mj.Yaku.SHOUSUSHI:  (13, 13, True), # 小四喜
    mj.Yaku.RYUISO:     (13, 13, True), # 緑一色
    mj.Yaku.CHINRO:     (13, 13, True), # 清老頭
    mj.Yaku.SUKANTSU:   (13, 13, True), # 四槓子
    mj.Yaku.CHUREN:     (13, 0, True),  # 九蓮宝燈
    mj.Yaku.TENHOU:     (13, 0, True),  # 天和
    mj.Yaku.CHIHOU:     (13, 0, True),  # 地和
    mj.Yaku.RENHOU:     (13, 0, True),  # 人和
    mj.Yaku.KOKUSHI13:  (26, 0, True),  # 国士無双十三面待ち
    mj.Yaku.SUTTAN:     (26, 0, True),  # 四暗刻単騎待ち
    mj.Yaku.CHUREN9:    (26, 0, True),  # 純正九蓮宝燈
}

# プレイヤー
players = [mp.Tenari("Tenari1"), mp.Tenari("Tenari2"), mp.Tenari("Tenari3")]
#players = [mp.Human("Human"), mp.Tenari("Tenari1"), mp.Tenari("Tenari2")]

game = mj.GraphicalGame(mjhai_set, yakus, players, 35000, players[0], True)
game.start()
