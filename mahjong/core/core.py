import os
import random
import time
import copy
import enum
from operator import add
import collections
import itertools
import pickle
from abc import ABCMeta, abstractmethod
from .. import graphic as gp

# ソフト名
APP_NAME = "Mahjong"

# シャンテン数計算テーブルを読み込み
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(THIS_PATH + "/shanten_table.bin", "rb") as table_file:
    combi_table = pickle.load(table_file)

# 役の種類
class Yaku(enum.Enum):
    DORA       = enum.auto()
    URADORA    = enum.auto()
    AKADORA    = enum.auto()
    GARI       = enum.auto()
    RICHI      = enum.auto()
    TSUMO      = enum.auto()
    IPPATSU    = enum.auto()
    PINFU      = enum.auto()
    IPEKO      = enum.auto()
    TANYAO     = enum.auto()
    YAKUHAI    = enum.auto()
    HAITEI     = enum.auto()
    HOUTEI     = enum.auto()
    RINSYAN    = enum.auto()
    CHANKAN    = enum.auto()
    DABURI     = enum.auto()
    ITTSU      = enum.auto()
    CHANTA     = enum.auto()
    DOUJUN     = enum.auto()
    DOUKO      = enum.auto()
    SANANKO    = enum.auto()
    SANKANTSU  = enum.auto()
    TOITOI     = enum.auto()
    SHOUSANGEN = enum.auto()
    HONRO      = enum.auto()
    CHITOI     = enum.auto()
    RYANPEKO   = enum.auto()
    JUNCHAN    = enum.auto()
    HONITSU    = enum.auto()
    NAGASHI    = enum.auto()
    CHINITSU   = enum.auto()
    KOKUSHI    = enum.auto()
    SUANKO     = enum.auto()
    TSUISO     = enum.auto()
    DAISANGEN  = enum.auto()
    DAISUSHI   = enum.auto()
    SHOUSUSHI  = enum.auto()
    RYUISO     = enum.auto()
    CHINRO     = enum.auto()
    SUKANTSU   = enum.auto()
    CHUREN     = enum.auto()
    TENHO      = enum.auto()
    CHIHO      = enum.auto()
    RENHO      = enum.auto()
    KOKUSHI13  = enum.auto()
    SUTTAN     = enum.auto()
    CHUREN9    = enum.auto()

# 役名
yaku_name = {
    Yaku.DORA:       "ドラ",
    Yaku.URADORA:    "裏ドラ",
    Yaku.AKADORA:    "赤ドラ",
    Yaku.GARI:       "ガリ",
    Yaku.RICHI:      "立直",
    Yaku.TSUMO:      "門前清自摸和",
    Yaku.IPPATSU:    "一発",
    Yaku.PINFU:      "平和",
    Yaku.IPEKO:      "一盃口",
    Yaku.TANYAO:     "タンヤオ",
    Yaku.YAKUHAI:    "役牌",
    Yaku.HAITEI:     "海底摸月",
    Yaku.HOUTEI:     "河底撈魚",
    Yaku.RINSYAN:    "嶺上開花",
    Yaku.CHANKAN:    "槍槓",
    Yaku.DABURI:     "ダブル立直",
    Yaku.ITTSU:      "一気通貫",
    Yaku.CHANTA:     "チャンタ",
    Yaku.DOUJUN:     "三色同順",
    Yaku.DOUKO:      "三色同刻",
    Yaku.SANANKO:    "三暗刻",
    Yaku.SANKANTSU:  "三槓子",
    Yaku.TOITOI:     "対々和",
    Yaku.SHOUSANGEN: "小三元",
    Yaku.HONRO:      "混老頭",
    Yaku.CHITOI:     "七対子",
    Yaku.RYANPEKO:   "二盃口",
    Yaku.JUNCHAN:    "純チャン",
    Yaku.HONITSU:    "混一色",
    Yaku.NAGASHI:    "流し満貫",
    Yaku.CHINITSU:   "清一色",
    Yaku.KOKUSHI:    "国士無双",
    Yaku.SUANKO:     "四暗刻",
    Yaku.TSUISO:     "字一色",
    Yaku.DAISANGEN:  "大三元",
    Yaku.DAISUSHI:   "大四喜",
    Yaku.SHOUSUSHI:  "小四喜",
    Yaku.RYUISO:     "緑一色",
    Yaku.CHINRO:     "清老頭",
    Yaku.SUKANTSU:   "四槓子",
    Yaku.CHUREN:     "九蓮宝燈",
    Yaku.TENHO:      "天和",
    Yaku.CHIHO:      "地和",
    Yaku.RENHO:      "人和",
    Yaku.KOKUSHI13:  "国士無双十三面待ち",
    Yaku.SUTTAN:     "四暗刻単騎待ち",
    Yaku.CHUREN9:    "純正九蓮宝燈",
}

# 役の翻数
yaku_fan = {
    Yaku.DORA:       (1, 1),
    Yaku.URADORA:    (1, 0),
    Yaku.AKADORA:    (1, 1),
    Yaku.GARI:       (1, 1),
    Yaku.RICHI:      (1, 0),
    Yaku.TSUMO:      (1, 0),
    Yaku.IPPATSU:    (1, 0),
    Yaku.PINFU:      (1, 0),
    Yaku.IPEKO:      (1, 0),
    Yaku.TANYAO:     (1, 1),
    Yaku.YAKUHAI:    (1, 1),
    Yaku.HAITEI:     (1, 1),
    Yaku.HOUTEI:     (1, 1),
    Yaku.RINSYAN:    (1, 1),
    Yaku.CHANKAN:    (1, 1),
    Yaku.DABURI:     (1, 0),
    Yaku.ITTSU:      (2, 1),
    Yaku.CHANTA:     (2, 1),
    Yaku.DOUJUN:     (2, 1),
    Yaku.DOUKO:      (2, 2),
    Yaku.SANANKO:    (2, 2),
    Yaku.SANKANTSU:  (2, 2),
    Yaku.TOITOI:     (2, 2),
    Yaku.SHOUSANGEN: (2, 2),
    Yaku.HONRO:      (2, 2),
    Yaku.CHITOI:     (2, 0),
    Yaku.RYANPEKO:   (3, 0),
    Yaku.JUNCHAN:    (3, 2),
    Yaku.HONITSU:    (3, 2),
    Yaku.NAGASHI:    (5, 0),
    Yaku.CHINITSU:   (6, 5),
    Yaku.KOKUSHI:    (13, 0),
    Yaku.SUANKO:     (13, 0),
    Yaku.TSUISO:     (13, 13),
    Yaku.DAISANGEN:  (13, 13),
    Yaku.DAISUSHI:   (26, 26),
    Yaku.SHOUSUSHI:  (13, 13),
    Yaku.RYUISO:     (13, 13),
    Yaku.CHINRO:     (13, 13),
    Yaku.SUKANTSU:   (13, 13),
    Yaku.CHUREN:     (13, 0),
    Yaku.TENHO:      (13, 0),
    Yaku.CHIHO:      (13, 0),
    Yaku.RENHO:      (13, 0),
    Yaku.KOKUSHI13:  (26, 0),
    Yaku.SUTTAN:     (26, 0),
    Yaku.CHUREN9:    (26, 0),
}

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
        return self.kind == other.kind

    def __lt__(self, other):
        return self.kind + (self.dora,) < other.kind + (other.dora,)

    def __gt__(self, other):
        return self.kind + (self.dora,) > other.kind + (other.dora,)

# 面子の種類
class EK(enum.Enum):
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

        for self_hai, other_hai in zip(self, other):
            if self_hai.kind != other_hai.kind:
                break
        else:
            return True

        return False

    # 順子かどうか
    def is_shuntsu(self):
        return self.kind in [EK.SHUNTSU, EK.MINSHUN]

    # 刻子かどうか
    def is_kotsu(self):
        return self.kind in [EK.ANKO, EK.MINKO, EK.ANKAN, EK.MINKAN, EK.KAKAN]

# 副露した面子
def Furo(Elememt):
    def __init__(self, hais, kind, whose):
        self.whose = whose
        super().__init__(hais, kind)

# 手牌
class Tehai():
    def __init__(self):
        self.hais = []
        self.furos = []
        self.table = collections.Counter()

        self.tsumo_hai = None
        self.menzen = True

    def __len__(self):
        return len(self.hais) + (0 if self.tsumo is None else 1)

    # ツモ牌を手牌に格納
    def store(self):
        if self.tsumo_hai is not None:
            self.hais.append(self.tsumo_hai)
            self.tsumo_hai = None

    # ツモ
    def tsumo(self, hai):
        self.store()
        self.tsumo_hai = hai
        self.table[hai.kind] += 1

    # 追加
    def append(self, hai):
        self.hais.append(hai)
        self.table[hai.kind] += 1

    # 挿入
    def insert(self, index, hai):
        self.hais.insert(index, hai)
        self.table[hai.kind] += 1

    # 番号で取り出し
    def pop(self, index=-1):
        self.store()
        pop_hai = self.hais.pop(index)
        self.table[pop_hai.kind] -= 1
        return pop_hai

    # 牌を指定して取り出し
    def remove(self, hai):
        self.store()
        remove_hai = self.hais.remove(hai)
        self.table[remove_hai.kind] -= 1
        return remove_hai

    # 牌の種類を指定して検索
    def find(self, kind, dora=False):
        for i, hai in enumerate(self.hais + [self.tsumo]):
            if hai.kind == kind:
                return hai
        return None

    # 並べ替え
    def sort(self):
        self.hais.sort()

    # 暗槓可能な牌
    def ankan_able(self):
        for kind, count in self.table.items():
            if count >= 4:
                yield [self.find(kind) for i in range(4)]

    # 加槓可能な牌
    def kakan_able(self):
        for furo in self.furos:
            # 明刻だったら
            if furo.kind == EK.MINKO:
                for kind, count in self.table.items():
                    # 明刻と同じ牌だったら
                    if furo[0].kind == kind:
                        yield [self.find(kind)]

    # ポン可能な牌
    def pon_able(self, hai):
        if self.table[hai.kind] >= 2:
            yield [self.find(kind) for i in range(2)]

    # チー可能な牌
    def chi_able(self, hai):
        for i in range(-2, 1):
            for j in range(3):
                if i + j and self.table[hai.kind[0], hai.kind[1] + i + j]:
                    break
            else:
                yield [self.find(hai.kind[0], hai.kind[1] + i + j) for j in range(3) if i + j]

    # 明槓可能な牌
    def minkan_able(self, hai):
        if self.table[hai.kind] >= 3:
            yield [self.find(kind) for i in range(3)]

    # 暗槓
    def ankan(self, hais):
        ankan_hais = [self.remove(hai) for hai in hais]
        self.furos.append(Element(furo_hais, EK.ANKAN))

    # 明槓
    def minkan(self, hais, whose):
        furo_hais = [self.remove(hai) for hai in hais]
        self.furos.append(Furo(furo_hais, EK.MINKAN, whose))

    # ポン
    def pon(self, hais, whose):
        furo_hais = [self.remove(hai) for hai in hais]
        self.furos.append(Furo(furo_hais, EK.MINKO, whose))

    # チー
    def chi(self, hais, whose):
        furo_hais = [self.remove(hai) for hai in hais]
        self.furos.append(Furo(furo_hais, EK.MINSHUN, whose))

    # 表示
    def show(self):
        for hai in self.hais:
            print(format(hai.name, "<4s"), end="")

        if self.tsumo_hai is not None:
            print(" {}".format(self.tsumo_hai.name))
        else:
            print()

        for j in range(len(self.hais)):
            print(format(j, "<4d"), end="")

        if self.tsumo is not None:
            print(" {}".format(j + 1))
        else:
            print()

    # 通常手のシャンテン数
    def shanten_normal(self):
        # シャンテン数計算テーブル用のキーを作成
        def create_key(table, color):
            combi_key = []

            for i in range(1, 10):
                # 孤立牌は除去
                if table[(color, i)] == 1 and sum(table[(color, i + j)] for j in [-2, -1, 1, 2]) == 0:
                    combi_key.append(0)
                else:
                    combi_key.append(table[(color, i)])

            # 前後の0を切り取り
            for i in range(9):
                if combi_key[0] == 0:
                    combi_key.pop(0)
                else:
                    break
            else: # 全て0だったら
                return (0,)

            while True:
                if combi_key[-1] == 0:
                    combi_key.pop()
                else:
                    break

            return tuple(combi_key)

        # 雀頭を考慮しないシャンテン数
        def shanten_without_jantou(table):
            mentsu_max = 4 - len(self.furos)
            shanten_min = 8 - len(self.furos) * 2

            # 字牌の面子・面子候補
            jihai_combi = [0, 0]
            for i in range(3, 10):
                if table[(i, 0)] >= 3:
                    jihai_combi[0] += 1

                if table[(i, 0)] == 2:
                    jihai_combi[1] += 1

            # 全ての面子・面子候補の組み合わせ
            combi_all = itertools.product(*(combi_table[create_key(self.table, i)] for i in range(3)), [tuple(jihai_combi)])

            for cur_combi in combi_all:
                cur_shanten = 8 - len(self.furos) * 2
                mentsu_num = 0

                # 面子から取り出し
                for i in range(2):
                    for elememt in cur_combi:
                        if mentsu_num + elememt[i] >= mentsu_max:
                            cur_shanten -= (2 if i == 0 else 1) * (mentsu_max - mentsu_num)
                            mentsu_num = mentsu_max
                            break
                        else:
                            cur_shanten -= (2 if i == 0 else 1) * elememt[i]
                            mentsu_num = mentsu_num + elememt[i]

                if cur_shanten < shanten_min:
                    shanten_min = cur_shanten

            return shanten_min

        # 雀頭なしのシャンテン数
        shanten_min = shanten_without_jantou(self.table)

        # 全ての雀頭候補を取り出してシャンテン数を計算
        for kind, count in self.table.items():
            if count >= 2:
                self.table[kind] -= 2

                cur_shanten = shanten_without_jantou(self.table) - 1
                if cur_shanten < shanten_min:
                    shanten_min = cur_shanten

                self.table[kind] += 2

        return shanten_min

    # 七対子のシャンテン数
    def shanten_chitoi(self):
        if not self.menzen:
            return 13

        shanten_num = 6
        for count in self.table.values():
            if count >= 2:
                shanten_num -= 1

        return shanten_num

    # 国士無双のシャンテン数
    def shanten_kokushi(self):
        if not self.menzen:
            return 13

        shanten_num = 13
        jantou = False

        for kind, count in self.table.items():
            if count and kind[1] in [0, 1, 9]:
                # 雀頭
                if count >= 2 and not jantou:
                    shanten_num -= 2
                    jantou = True
                else:
                    shanten_num -= 1

        return shanten_num

    # シャンテン数
    def shanten(self):
        return min(self.shanten_normal(), self.shanten_chitoi(), self.shanten_kokushi())

    # 役
    def yaku(self):
        # 和了時の面子の組み合わせを探索
        def combi_agari():
            # 全ての雀頭候補を取り出す
            for kind, count in self.table.items():
                if count >= 2:
                    self.table[kind] -= 2

                    # 0...順子 1...暗刻
                    mentsu_combi = itertools.product([0, 1], 4 - len(self.furos))

                    # 左から順番に面子を取り出し
                    for cur_combi in mentsu_combi:
                        return_combi = self.furos + [Element([self.find(kind), self.find(kind)], EK.JANTOU)]
                        temp_table = copy.deepcopy(self.table)

                        for mentsu_kind in cur_combi:
                            # 開始点
                            for i in range(10):
                                for j in range(10):
                                    if temp_table[(i, j)]:
                                        break
                                else:
                                    continue
                                break

                            if mentsu_kind == 0:
                                # 順子
                                if temp_table[(i, j)] and temp_table[(i, j + 1)] and temp_table[(i, j + 2)]:
                                    return_combi.append(Element([self.find((i, j)), self.find((i, j + 1)), self.find((i, j + 2))], EK.SHUNTSU))
                                    for k in range(3):
                                        temp_table[(i, j + k)] -= 1
                                else:
                                    break
                            else:
                                # 暗刻
                                if temp_table[(i, j)] >= 3:
                                    return_combi.append(Element([self.find((i, j)), self.find((i, j)), self.find((i, j))], EK.ANKO))
                                    temp_table[(i, j)] -= 3
                                else:
                                    break
                        else:
                            yield return_combi

                    self.table[kind] += 2

        if self.shanten() > -1:
            return []

        # 国士無双
        if self.shanten_kokushi() == -1:
            return [[Yaku.KOKUSHI]]

        # 組み合わせに関係なく共通の役
        yakuman_common = []
        yaku_common = []

        # 副露含め全てのテーブル
        all_table = self.table
        for furo in self.furos:
            all_table += furo.table

        # 役満から先に調べる
        # 字一色
        for kind, count in all_table.items():
            if count > 0 and kind[0] < 3:
                break
        else:
            yakuman_common.append(Yaku.TSUISO)

        # 緑一色
        for kind, count in all_table.items():
            if count > 0 and not kind in [(1, 2), (1, 3), (1, 4), (1, 6), (1, 8), (8, 0)]:
                break
        else:
            yakuman_common.append(Yaku.RYUISO)

        # 九蓮宝燈
        for i in range(3):
            for j in range(1, 10):
                if self.table[(i, j)] < (3 if j == 1 or j == 9 else 1):
                    break
            else:
                yakuman_common.append(Yaku.CHUREN)
                break

        if len(yakuman_common) == 0:
            # タンヤオ
            for kind, count in all_table.items():
                if count > 0 and not 2 <= kind[1] <= 8:
                    break
            else:
                yaku_common.append(Yaku.TANYAO)

            # 混一色・清一色
            append_yaku = Yaku.CHINITSU
            for i in range(3):
                for kind, count in all_table.items():
                    if count > 0 and kind[0] != i:
                        if kind[0] >= 3:
                            append_yaku = Yaku.HONITSU
                        else:
                            break
                else:
                    yaku_common.append(append_yaku)
                    break

            # 混老頭・清老頭
            routou = False
            append_yaku = Yaku.CHINRO
            for kind, count in all_table.items():
                if count > 0:
                    if kind[0] >= 3:
                        append_yaku = Yaku.HONRO
                    if 2 <= kind[1] <= 8:
                        break
            else:
                routou = True
                yaku_common.append(append_yaku)

            # 七対子
            if self.shanten_chitoi() == -1:
                return [yaku_common + [Yaku.CHITOI]]

        # 全ての組み合わせでの役
        for cur_combi in combi_agari():
            yaku_list = yakuman_common[:]

            # 四暗刻
            if sum(1 for elememt in cur_combi if element.kind == EK.ANKO or element.kind == EK.ANKAN) == 4:
                yaku_list.append(Yaku.SUANKO)

            # 大四喜・小四喜
            append_yaku = Yaku.DAISUSHI
            for i in range(3, 7):
                for element in cur_combi:
                    if element.kind == EK.JANTOU and element.hais[0].kind[0] == i:
                        append_yaku = Yaku.SHOUSUSHI
                        break

                    elif element.is_kotsu() and element.hais[0].kind[0] == i:
                        break
                else:
                    break
            else:
                yaku_list.append(append_yaku)

            # 大三元
            for i in range(7, 10):
                for element in cur_combi:
                    if element.is_kotsu() and element.hais[0].kind[0] == i:
                        break
                else:
                    break
            else:
                yaku_list.append(Yaku.DAISANGEN)

            if len(yaku_list) == 0:
                yaku_list = yaku_common[:]

                if self.menzen:
                    # 平和
                    if sum(1 for elememt in cur_combi if element.kind == EK.SHUNTSU) == 4:
                        yaku_list.append(Yaku.PINFU)

                    # 一盃口・二盃口
                    peko_num = 0

                    for peko_combi in itertools.combinations(cur_combi, 2):
                        if peko_combi[0] == peko_combi[1]:
                            peko_num += 1
                        
                    if peko_num == 1:
                        yaku_list.append(Yaku.IPEKO)
                    elif peko_num == 2:
                        yaku_list.append(Yaku.RYANPEKO)

                # 一気通貫
                for i in range(3):
                    for j in range(3):
                        for element in cur_combi:
                            if element.is_shuntsu() and sum(element.table[(i, j * 3 + k)] for k in range(1, 4)) == 3:
                                break
                        else:
                            break
                    else:
                        yaku_list.append(Yaku.ITTSU)
                        break

                # 三色同順
                for i in range(1, 8):
                    for j in range(3):
                        for element in cur_combi:
                            if element.is_shuntsu() and sum(element.table[(j, i + k)] for k in range(3)) == 3:
                                break
                        else:
                            break
                    else:
                        yaku_list.append(Yaku.DOUJUN)
                        break

                # 三色同刻
                for i in range(1, 10):
                    for j in range(3):
                        for element in cur_combi:
                            if element.is_kotsu() and element.table[(j, i)] >= 3:
                                break
                        else:
                            break
                    else:
                        yaku_list.append(Yaku.DOUKO)
                        break

                # 役牌
                for element in cur_combi:
                    if element.is_kotsu() and element.hais[0].kind[0] >= 3:
                        yaku_list.append(Yaku.YAKUHAI)

                # チャンタ・純チャン
                if not routou:
                    append_yaku = Yaku.JUNCHAN
                    for element in cur_combi:
                        for hai in element.hais:
                            if hai.kind[1] == 1 or hai.kind[1] == 9:
                                break

                            elif hai.kind[0] >= 3:
                                append_yaku = Yaku.CHANTA
                                break
                        else:
                            continue
                        break
                    else:
                        yaku_list.append(append_yaku)

                # 三暗刻
                if sum(1 for elememt in cur_combi if element.kind == EK.ANKO or element.kind == EK.ANKAN) == 3:
                    yaku_list.append(Yaku.SANANKO)

            yield yaku_list

# 河の麻雀牌
class KawaMjHai(MjHai):
    def __init__(self, hai, tsumogiri, richi, furo):
        self.kind = hai.kind
        self.dora = hai.dora
        self.name = hai.name
        self.tsumogiri = tsumogiri
        self.richi = richi
        self.furo = furo

# 河
class Kawa():
    def __init__(self):
        self.hais = []

    # 追加
    def append(self, hai, tsumogiri=False, richi=False, furo=False):
        self.hais.append(KawaMjHai(hai, tsumogiri, richi, furo))

# 山
class Yama():
    def __init__(self, mjhai_set):
        seed = time.time() #1559974153.2062666
        print("seed = {}".format(seed))
        random.seed(seed)

        self.hais = copy.deepcopy(mjhai_set)
        random.shuffle(self.hais)
        self.remain = len(self.hais) - 14

        self.doras = [self.hais[0]]
        self.uradoras = [self.hais[1]]
        self.dora_num = 1
    
    # 取り出し
    def pop(self):
        self.remain -= 1
        return self.hais.pop()

    # ドラを増やす
    def add_dora(self):
        self.doras.append(self.hais[self.dora_num * 2])
        self.uradoras.append(self.hais[self.dora_num * 2 + 1])
        self.dora_num += 1

# プレイヤー
class Player(metaclass=ABCMeta):
    def __init__(self, name=""):
        self.name = name
        self.tehai = Tehai()
        self.kawa = Kawa()

        self.point = 35000
        self.richi = False

    def setup(self, chicha, game):
        self.chicha = chicha
        self.game = game

    # 自風
    def jikaze(self):
        return (self.chicha - self.game.kyoku) % self.game.players_num

    # 配牌
    def haipai(self):
        for i in range(13):
            pop_hai = self.game.yama.pop()
            self.tehai.append(pop_hai)
        self.tehai.sort()

    # 自摸
    def tsumo(self):
        pop_hai = self.game.yama.pop()
        self.tehai.tsumo(pop_hai)

    # 打牌
    def dahai(self):
        # リーチをしていたらツモ切り
        index = -1 if self.richi else self.select()
        pop_hai = self.tehai.pop(index)

        # 立直
        if not self.richi and self.tehai.shanten() == 0 and self.tehai.menzen:
            self.richi = self.call_richi()

        tsumogiri = (index == len(self.tehai.hais) or index == -1)
        self.kawa.append(pop_hai, tsumogiri, self.richi)
        self.tehai.sort()

    # ツモ・暗槓・加槓チェック
    def check_self(self):
        if self.tehai.shanten() == -1:
            return self.agari_tsumo()

        """
        # 暗槓
        for cur_ankan in self.tehai.ankan_able():
            if self.ankan(cur_ankan):
                self.tehai.ankan(cur_ankan)
                self.game.tsumo()

            return False
        """
        return False

    # ロン・明槓・ポン・チーチェック
    def check_other(self, player):
        check_hai = player.kawa.hais[-1]
        self.tehai.tsumo(check_hai)

        # ロン
        if self.tehai.shanten() == -1 and self.agari_ron(player):
            check_hai.furo = True
            return True

        self.tehai.pop()

        """
        if not self.richi:
            # 明槓
            if self.tehai.table[check_hai.kind] >= 3 and self.minkan(player):
                self.tehai.menzen = False
                check_hai.furo = True

                append_mentsu = []
                for i in range(4):
                    if int(((player.chicha - self.chicha) % 4 - 1) * 1.5) == i:
                        append_mentsu.append(check_hai)
                    else:
                        append_mentsu.append(self.tehai.pop_kind(check_hai.kind))

                self.tehai.furo.append(append_mentsu)
                self.game.change_player(self.chicha)
                self.game.tsumo()
                self.game.dahai()

                return False

            # ポン
            if self.tehai.table[check_hai.kind] >= 2 and self.pon(player):
                self.tehai.menzen = False
                check_hai.furo = True

                append_mentsu = []
                for i in range(3):
                    if (player.chicha - self.chicha) % 4 - 1 == i:
                        append_mentsu.append(check_hai)
                    else:
                        append_mentsu.append(self.tehai.pop_kind(check_hai.kind))

                self.tehai.furo.append(append_mentsu)
                self.game.change_player(self.chicha)
                self.game.dahai()

                return False
        """

        return False

    # 選択
    @abstractmethod
    def select(self):
        pass

    # ツモ和了
    @abstractmethod
    def agari_tsumo(self):
        pass

    # ロン和了
    @abstractmethod
    def agari_ron(self, player):
        pass

    # 立直
    @abstractmethod
    def call_richi(self):
        pass

    # 暗槓
    @abstractmethod
    def ankan(self, hai_kind):
        pass

    # 明槓
    @abstractmethod
    def minkan(self, player):
        pass

    # 加槓
    @abstractmethod
    def kakan(self):
        pass

    # ポン
    @abstractmethod
    def pon(self, player):
        pass

    # チー
    @abstractmethod
    def chi(self, player):
        pass

# ゲーム
class Game():
    kaze_name = ["東", "南", "西", "北"]

    def __init__(self, mjhai_set, players):
        self.mjhai_set = mjhai_set
        self.players_num = len(players)
        self.players = random.sample(players, self.players_num)

        for i, player in enumerate(self.players):
            player.setup(i, self)

        self.bakaze = 0
        self.kyoku = 0
        self.honba = 0
        self.kyotaku = 0

        self.cur = self.kyoku
        self.cur_player = self.players[self.cur]

        self.yama = Yama(mjhai_set)
        self.screen = gp.Screen(self, True, self.players[1])

    # 局を表す文字列
    def kyoku_name(self):
        return "{}{}局".format(Game.kaze_name[self.bakaze], self.kyoku + 1)

    # 配牌
    def haipai(self):
        for player in self.players:
            player.haipai()

        self.screen.draw()

    # ツモ
    def tsumo(self):
        self.cur_player.tsumo()
        self.screen.draw()

        return self.cur_player.check_self()

    # 打牌
    def dahai(self):
        self.cur_player.dahai()
        self.screen.draw()

        for check_player in self.players:
            # 自身は判定しない
            if check_player != self.cur_player:
                if check_player.check_other(self.cur_player):
                    return check_player
        else:
            return None

    # プレイヤーのツモ順を変更
    def change_player(self, chicha):
        self.cur = chicha
        self.cur_player = self.players[self.cur]

    # 次のプレイヤーへ
    def next_player(self):
        self.change_player((self.cur + 1) % self.players_num)
