import mahjong.core as mj

# 役
yaku = {
    mj.Yaku.DORA:       (1, 1),   # ドラ
    mj.Yaku.URADORA:    (1, 0),   # 裏ドラ
    mj.Yaku.AKADORA:    (1, 1),   # 赤ドラ
    mj.Yaku.RICHI:      (1, 0),   # 立直
    mj.Yaku.TSUMO:      (1, 0),   # ツモ
    mj.Yaku.IPPATSU:    (1, 0),   # 一発
    mj.Yaku.PINFU:      (1, 0),   # 平和
    mj.Yaku.IPEKO:      (1, 0),   # 一盃口
    mj.Yaku.TANYAO:     (1, 0),   # タンヤオ
    mj.Yaku.YAKUHAI:    (1, 1),   # 役牌
    mj.Yaku.HAITEI:     (1, 1),   # 海底摸月
    mj.Yaku.HOUTEI:     (1, 1),   # 河底撈魚
    mj.Yaku.RINSYAN:    (1, 1),   # 嶺上開花
    mj.Yaku.CHANKAN:    (1, 1),   # 槍槓
    mj.Yaku.DABURI:     (1, 0),   # ダブル立直
    mj.Yaku.ITTSU:      (2, 1),   # 一気通貫
    mj.Yaku.CHANTA:     (2, 1),   # チャンタ
    mj.Yaku.DOUJUN:     (2, 1),   # 三色同順
    mj.Yaku.DOUKO:      (2, 2),   # 三色同刻
    mj.Yaku.SANANKO:    (2, 2),   # 三暗刻
    mj.Yaku.SANKANTSU:  (2, 2),   # 三槓子
    mj.Yaku.TOITOI:     (2, 2),   # 対々和
    mj.Yaku.SHOUSANGEN: (2, 2),   # 小三元
    mj.Yaku.HONRO:      (2, 2),   # 混老頭
    mj.Yaku.CHITOI:     (2, 0),   # 七対子
    mj.Yaku.RYANPEKO:   (3, 0),   # 二盃口
    mj.Yaku.JUNCHAN:    (3, 2),   # 純チャン
    mj.Yaku.HONITSU:    (3, 2),   # 混一色
    #mj.Yaku.NAGASHI:    (5, 0),   # 流し満貫
    mj.Yaku.CHINITSU:   (6, 5),   # 清一色
    mj.Yaku.KOKUSHI:    (13, 0),  # 国士無双
    mj.Yaku.SUANKO:     (13, 0),  # 四暗刻
    mj.Yaku.TSUISO:     (13, 13), # 字一色
    mj.Yaku.DAISANGEN:  (13, 13), # 大三元
    mj.Yaku.DAISUSHI:   (26, 26), # 大四喜
    mj.Yaku.SHOUSUSHI:  (13, 13), # 小四喜
    mj.Yaku.RYUISO:     (13, 13), # 緑一色
    mj.Yaku.CHINRO:     (13, 13), # 清老頭
    mj.Yaku.SUKANTSU:   (13, 13), # 四槓子
    mj.Yaku.CHUREN:     (13, 0),  # 九蓮宝燈
    mj.Yaku.TENHOU:     (13, 0),  # 天和
    mj.Yaku.CHIHOU:     (13, 0),  # 地和
    mj.Yaku.RENHOU:     (13, 0),  # 人和
    mj.Yaku.KOKUSHI13:  (26, 0),  # 国士無双十三面待ち
    mj.Yaku.SUTTAN:     (26, 0),  # 四暗刻単騎待ち
    mj.Yaku.CHUREN9:    (26, 0),  # 純正九蓮宝燈
}

tehai = mj.Tehai(
    [
        mj.MjHai((0, 1)),
        mj.MjHai((0, 2)),
        mj.MjHai((0, 3)),
        mj.MjHai((1, 1)),
        mj.MjHai((1, 2)),
        mj.MjHai((1, 3)),
        mj.MjHai((3, 0)),
        mj.MjHai((3, 0)),
        mj.MjHai((3, 0)),
        mj.MjHai((4, 0)),
        mj.MjHai((4, 0)),
        mj.MjHai((4, 0)),
        mj.MjHai((5, 0)),
        mj.MjHai((5, 0)),
    ]
)

for cur_yaku_list in tehai.yaku(True, True, 0, 0, [((0, 2), (0, 2))]):
    for cur_yaku in cur_yaku_list:
        print(yaku[cur_yaku][not tehai.menzen], mj.yaku_name[cur_yaku])
