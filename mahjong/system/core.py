import os
import random
import time
import copy
import enum
import collections

# ソフト名
APP_NAME = "Mahjong"

# シード値を設定
seed = time.time()
random.seed(seed)
print("seed = {}".format(seed))

# 役の種類
class Yaku(enum.Enum):
    DORA      = enum.auto()
    URADORA   = enum.auto()
    AKADORA   = enum.auto()
    GARI      = enum.auto()
    RICHI     = enum.auto()
    TSUMO     = enum.auto()
    IPPATSU   = enum.auto()
    PINFU     = enum.auto()
    IPEKO     = enum.auto()
    TANYAO    = enum.auto()
    YAKUHAI   = enum.auto()
    HAITEI    = enum.auto()
    HOTEI     = enum.auto()
    RINSYAN   = enum.auto()
    CHANKAN   = enum.auto()
    DABURI    = enum.auto()
    ITTSU     = enum.auto()
    CHANTA    = enum.auto()
    DOJUN     = enum.auto()
    DOKO      = enum.auto()
    SANANKO   = enum.auto()
    SANKANTSU = enum.auto()
    TOITOI    = enum.auto()
    SHOSANGEN = enum.auto()
    HONRO     = enum.auto()
    CHITOI    = enum.auto()
    RYANPEKO  = enum.auto()
    JUNCHAN   = enum.auto()
    HONITSU   = enum.auto()
    NAGASHI   = enum.auto()
    CHINITSU  = enum.auto()
    KOKUSHI   = enum.auto()
    SUANKO    = enum.auto()
    TSUISO    = enum.auto()
    DAISANGEN = enum.auto()
    DAISUSHI  = enum.auto()
    SHOSUSHI  = enum.auto()
    RYUISO    = enum.auto()
    CHINRO    = enum.auto()
    SUKANTSU  = enum.auto()
    CHUREN    = enum.auto()
    TENHO     = enum.auto()
    CHIHO     = enum.auto()
    RENHO     = enum.auto()
    KOKUSHI13 = enum.auto()
    SUTTAN    = enum.auto()
    CHUREN9   = enum.auto()

# 役名
YAKU_NAME = {
    Yaku.DORA:      "ドラ",
    Yaku.URADORA:   "裏ドラ",
    Yaku.AKADORA:   "赤ドラ",
    Yaku.GARI:      "ガリ",
    Yaku.RICHI:     "立直",
    Yaku.TSUMO:     "門前清自摸和",
    Yaku.IPPATSU:   "一発",
    Yaku.PINFU:     "平和",
    Yaku.IPEKO:     "一盃口",
    Yaku.TANYAO:    "タンヤオ",
    Yaku.YAKUHAI:   "役牌",
    Yaku.HAITEI:    "海底摸月",
    Yaku.HOTEI:     "河底撈魚",
    Yaku.RINSYAN:   "嶺上開花",
    Yaku.CHANKAN:   "槍槓",
    Yaku.DABURI:    "ダブル立直",
    Yaku.ITTSU:     "一気通貫",
    Yaku.CHANTA:    "チャンタ",
    Yaku.DOJUN:     "三色同順",
    Yaku.DOKO:      "三色同刻",
    Yaku.SANANKO:   "三暗刻",
    Yaku.SANKANTSU: "三槓子",
    Yaku.TOITOI:    "対々和",
    Yaku.SHOSANGEN: "小三元",
    Yaku.HONRO:     "混老頭",
    Yaku.CHITOI:    "七対子",
    Yaku.RYANPEKO:  "二盃口",
    Yaku.JUNCHAN:   "純チャン",
    Yaku.HONITSU:   "混一色",
    Yaku.NAGASHI:   "流し満貫",
    Yaku.CHINITSU:  "清一色",
    Yaku.KOKUSHI:   "国士無双",
    Yaku.SUANKO:    "四暗刻",
    Yaku.TSUISO:    "字一色",
    Yaku.DAISANGEN: "大三元",
    Yaku.DAISUSHI:  "大四喜",
    Yaku.SHOSUSHI:  "小四喜",
    Yaku.RYUISO:    "緑一色",
    Yaku.CHINRO:    "清老頭",
    Yaku.SUKANTSU:  "四槓子",
    Yaku.CHUREN:    "九蓮宝燈",
    Yaku.TENHO:     "天和",
    Yaku.CHIHO:     "地和",
    Yaku.RENHO:     "人和",
    Yaku.KOKUSHI13: "国士無双十三面待ち",
    Yaku.SUTTAN:    "四暗刻単騎待ち",
    Yaku.CHUREN9:   "純正九蓮宝燈",
}

# 待ちの種類
class Waiting(enum.Enum):
    RYANMEN = enum.auto()
    KANTYAN = enum.auto()
    PENTYAN = enum.auto()
    SHABO   = enum.auto()
    TANKI   = enum.auto()

# 麻雀牌
class MjHai():
    """
    kind[0]:
      0...筒子
      1...索子
      2...萬子
      3...東
      4...南
      5...西
      6...北
      7...白
      8...發
      9...中

    kind[1]:
      0  ...字牌
      1-9...数牌
    """

    color_name = ["p", "s", "m", "Ton", "Nan", "Sha", "Pei", "Hak", "Hat", "Chn"]

    def __init__(self, kind, dora=False):
        self.kind = kind # 種類
        self.dora = dora # ドラかどうか

        # 名称
        self.name = "{}{}{}".format(
            MjHai.color_name[self.kind[0]],
            self.kind[1] if self.kind[1] else "",
            "@" if self.dora else ""
        )

    # 比較演算子
    def __eq__(self, other):
        return self.kind + (self.dora,) == other.kind + (other.dora,)

    def __lt__(self, other):
        return self.kind + (self.dora,) < other.kind + (other.dora,)

    def __gt__(self, other):
        return self.kind + (self.dora,) > other.kind + (other.dora,)

# 面子の種類
class ElementKind(enum.Enum):
    JANTOU  = enum.auto()
    SHUNTSU = enum.auto()
    MINSHUN = enum.auto()
    ANKO    = enum.auto()
    MINKO   = enum.auto()
    ANKAN   = enum.auto()
    MINKAN  = enum.auto()
    KAKAN   = enum.auto()

# 面子
class Element():
    def __init__(self, hais, kind):
        self.kind = kind
        self.hais = hais

        self.table = collections.Counter()
        for hai in self.hais:
            self.table[hai.kind] += 1

    # =演算子
    def __eq__(self, other):
        if self.kind != other.kind:
            return False

        for self_hai, other_hai in zip(self.hais, other.hais):
            if self_hai != other_hai:
                return False

        return True

    # 牌の種類が一致しているかどうか
    def eq_kind(self, other):
        if self.kind != other.kind:
            return False

        for self_hai, other_hai in zip(self.hais, other.hais):
            if self_hai.kind != other_hai.kind:
                return False

        return True

    # 順子かどうか
    def is_shuntsu(self):
        return self.kind in [ElementKind.SHUNTSU, ElementKind.MINSHUN]

    # 刻子かどうか
    def is_kotsu(self):
        return self.kind in [ElementKind.ANKO, ElementKind.MINKO, ElementKind.ANKAN, ElementKind.MINKAN, ElementKind.KAKAN]

# 副露した面子
class FuroElement(Element):
    def __init__(self, hais, kind, direct):
        super().__init__(hais, kind)
        self.direct = direct

# ポンした面子
class PonElement(FuroElement):
    # 加槓
    def kakan(self, hai):
        self.kind = ElementKind.KAKAN
        self.hais.append(hai)
        self.table[hai.kind] += 1

# 河の麻雀牌
class KawaMjHai():
    def __init__(self, hai, tsumogiri=False, richi=False):
        self.hai = hai
        self.tsumogiri = tsumogiri
        self.richi = richi
        self.furo = False
        self.hoju = False

    def set_furo(self):
        self.furo = True

    def set_houju(self):
        self.hoju = True

# 河
class Kawa():
    def __init__(self):
        self.hais = []

    # 追加
    def append(self, hai, tsumogiri=False, richi=False):
        append_hai = KawaMjHai(hai, tsumogiri, richi)
        self.hais.append(append_hai)
        return append_hai

# 山
class Yama():
    def __init__(self, mjhai_set):
        self.hais = copy.deepcopy(mjhai_set)
        random.shuffle(self.hais)
        self.remain = len(self.hais) - 14
        self.doras = []
        self.add_dora()

    # 取り出し
    def pop(self):
        self.remain -= 1
        return self.hais.pop()

    # ドラを増やす
    def add_dora(self):
        new_dora = (self.hais[len(self.doras) * 2], self.hais[len(self.doras) * 2 + 1])
        self.doras.append(new_dora)
        return new_dora
