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

# シード値を設定
seed = time.time()
random.seed(seed)
print("seed = {}".format(seed))

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

        for self_hai, other_hai in zip(self.hais, other.hais):
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
class Furo(Element):
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
        return len(self.hais) + (0 if self.tsumo_hai is None else 1)

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
    def append(self, *hais):
        for hai in hais:
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
        self.hais.remove(hai)
        self.table[hai.kind] -= 1
        return hai

    # 牌の種類を指定して検索
    def find(self, kind):
        for hai in self.hais + [self.tsumo_hai]:
            if hai is not None and hai.kind == kind:
                return hai

        return None

    def find_multi(self, kinds):
        temp_tehai = copy.deepcopy(self)
        hais = []

        for kind in kinds:
            hais.append(temp_tehai.remove(temp_tehai.find(kind)))
        return hais

    # 並べ替え
    def sort(self):
        self.hais.sort()

    # 暗槓可能な牌
    def ankan_able(self):
        for kind, count in self.table.items():
            if count >= 4:
                yield self.find_multi([kind for i in range(4)])

    # 加槓可能な牌
    def kakan_able(self):
        for furo in self.furos:
            # 明刻だったら
            if furo.kind == EK.MINKO:
                for kind, count in self.table.items():
                    # 明刻と同じ牌だったら
                    if furo[0].kind == kind:
                        yield [self.find(kind)]

    # 明槓可能な牌
    def minkan_able(self, target):
        if self.table[target.kind] >= 3:
            yield self.find_multi([target.kind for i in range(3)])

    # ポン可能な牌
    def pon_able(self, target):
        if self.table[target.kind] >= 2:
            yield self.find_multi([target.kind for i in range(2)])

    # チー可能な牌
    def chi_able(self, target):
        for i in range(-2, 1):
            for j in range(3):
                if i + j and self.table[(target.kind[0], target.kind[1] + i + j)] == 0:
                    break
            else:
                yield self.find_multi([(target.kind[0], target.kind[1] + i + j) for j in range(3) if i + j])

    # 暗槓
    def ankan(self, hais):
        ankan_hais = [self.remove(hai) for hai in hais]
        self.furos.append(Element(ankan_hais, EK.ANKAN))

    # 明槓
    def minkan(self, hais, target, whose):
        self.menzen = False
        minkan_hais = [self.remove(hai) for hai in hais] + [target]
        self.furos.append(Furo(minkan_hais, EK.MINKAN, whose))

    # ポン
    def pon(self, hais, target, whose):
        self.menzen = False
        pon_hais = [self.remove(hai) for hai in hais] + [target]
        self.furos.append(Furo(pon_hais, EK.MINKO, whose))

    # チー
    def chi(self, hais, target, whose):
        self.menzen = False
        pon_hais = [self.remove(hai) for hai in hais] + [target]
        self.furos.append(Furo(pon_hais, EK.MINSHUN, whose))

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

        if self.tsumo_hai is not None:
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
            combi_all = itertools.product(*(combi_table.get(create_key(self.table, i), ((0, 0),)) for i in range(3)), [tuple(jihai_combi)])

            for cur_combi in combi_all:
                cur_shanten = 8 - len(self.furos) * 2
                mentsu_num = 0

                # 面子から取り出し
                for i in range(2):
                    for element in cur_combi:
                        if mentsu_num + element[i] >= mentsu_max:
                            cur_shanten -= (2 if i == 0 else 1) * (mentsu_max - mentsu_num)
                            mentsu_num = mentsu_max
                            break
                        else:
                            cur_shanten -= (2 if i == 0 else 1) * element[i]
                            mentsu_num = mentsu_num + element[i]

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
                    mentsu_combi = itertools.product([0, 1], repeat=4 - len(self.furos))

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
            return

        # 国士無双
        if self.shanten_kokushi() == -1:
            yield [Yaku.KOKUSHI]
            return

        # 組み合わせに関係なく共通の役
        yakuman_common = []
        yaku_common = []

        # 副露含め全てのテーブル
        all_table = copy.deepcopy(self.table)
        for furo in self.furos:
            all_table += furo.table

        # 役満から先に調べる
        # 字一色
        for kind, count in all_table.items():
            if count > 0 and kind[1]:
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

        # 清老頭
        for kind, count in all_table.items():
            if count > 0 and kind[1] != 1 and kind[1] != 9:
                break
        else:
            yakuman_common.append(Yaku.CHINRO)

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
                        if kind[1] == 0:
                            append_yaku = Yaku.HONITSU
                        else:
                            break
                else:
                    yaku_common.append(append_yaku)
                    break

            # 混老頭
            for kind, count in all_table.items():
                if count > 0 and 2 <= kind[1] <= 8:
                        honro = False
                        break
            else:
                honro = True
                yaku_common.append(Yaku.HONRO)

            # 七対子
            if self.shanten_chitoi() == -1:
                yield yaku_common + [Yaku.CHITOI]

        # 全ての組み合わせでの役
        for cur_combi in combi_agari():
            yaku_list = yakuman_common[:]

            # 四暗刻
            if sum(1 for element in cur_combi if element.kind == EK.ANKO or element.kind == EK.ANKAN) == 4:
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
                    if sum(1 for element in cur_combi if element.kind == EK.SHUNTSU) == 4:
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
                    if element.is_kotsu() and element.hais[0].kind[1] == 0:
                        yaku_list.append(Yaku.YAKUHAI)

                # 三暗刻
                if sum(1 for element in cur_combi if element.kind == EK.ANKO or element.kind == EK.ANKAN) == 3:
                    yaku_list.append(Yaku.SANANKO)

                # 対々和
                if sum(1 for element in cur_combi if element.is_kotsu()) == 4:
                    yaku_list.append(Yaku.TOITOI)

                # チャンタ・純チャン
                if not honro:
                    append_yaku = Yaku.JUNCHAN
                    for element in cur_combi:
                        for hai in element.hais:
                            if hai.kind[1] == 1 or hai.kind[1] == 9:
                                break

                            elif hai.kind[1] == 0:
                                append_yaku = Yaku.CHANTA
                                break
                        else:
                            break
                    else:
                        yaku_list.append(append_yaku)

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
        self.houju = False

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

    def setup(self, game, chicha, point):
        self.game = game
        self.chicha = chicha
        self.point = point

    # 自風
    def jikaze(self):
        return (self.chicha - self.game.kyoku) % self.game.players_num

    # 配牌
    def haipai(self):
        # リセット
        self.tehai = Tehai()
        self.kawa = Kawa()
        self.richi = False

        self.tehai.append(*(self.game.yama.pop() for i in range(13)))
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
            self.richi = self.do_richi()

        tsumogiri = (index == len(self.tehai.hais) or index == -1)
        self.kawa.append(pop_hai, tsumogiri, self.richi)
        self.tehai.sort()

    # ツモチェック
    def check_tsumo(self):
        if self.tehai.shanten() == -1 and self.do_tsumo():
            return True
        else:
            return False

    # ロンチェック
    def check_ron(self, whose):
        check_hai = whose.kawa.hais[-1]
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.tsumo(check_hai)

        # ロン
        if temp_tehai.shanten() == -1 and self.do_ron(check_hai, whose):
            check_hai.houju = True
            return True
        else:
            False

    # 暗槓チェック
    def check_ankan(self):
        # 暗槓
        for cur_ankan in self.tehai.ankan_able():
            if self.do_ankan(cur_ankan):
                self.tehai.ankan(cur_ankan)
                return True

        return False

    # 加槓チェック
    def check_kakan(self):
        pass

    # 副露チェック
    def check_furo(self, whose):
        if not self.richi:
            check_hai = whose.kawa.hais[-1]

            # 明槓
            for cur_minkan in self.tehai.minkan_able(check_hai):
                if self.do_minkan(cur_minkan, check_hai, whose):
                    check_hai.furo = True
                    self.tehai.minkan(cur_minkan, check_hai, whose)
                    return True

            # ポン
            for cur_pon in self.tehai.pon_able(check_hai):
                if self.do_pon(cur_pon, check_hai, whose):
                    check_hai.furo = True
                    self.tehai.pon(cur_pon, check_hai, whose)
                    return True

            """
            # チー
            for cur_chi in self.tehai.chi_able(check_hai):
                if self.do_chi(cur_chi, check_hai, whose):
                    check_hai.furo = True
                    self.tehai.chi(cur_chi, check_hai, whose)

                    self.game.change_player(self.chicha)
                    return True
            """

        return False

    # 選択
    @abstractmethod
    def select(self):
        pass

    # ツモ和了するか
    @abstractmethod
    def do_tsumo(self):
        pass

    # ロン和了するか
    @abstractmethod
    def do_ron(self, target, whose):
        pass

    # 立直するか
    @abstractmethod
    def do_richi(self):
        pass

    # 暗槓するか
    @abstractmethod
    def do_ankan(self, target):
        pass

    # 明槓するか
    @abstractmethod
    def do_minkan(self, hais, target, whose):
        pass

    # 加槓するか
    @abstractmethod
    def do_kakan(self, target):
        pass

    # ポンするか
    @abstractmethod
    def do_pon(self, hais, target, whose):
        pass

    # チーするか
    @abstractmethod
    def do_chi(self, hais, target, whose):
        pass

# ゲーム
class Game():
    kaze_name = ["東", "南", "西", "北"]

    def __init__(self, mjhai_set, yaku, players, point):
        self.mjhai_set = mjhai_set
        self.yaku = yaku

        self.players_num = len(players)
        self.players = random.sample(players, self.players_num)

        for i, player in enumerate(self.players):
            player.setup(self, i, point)

        self.bakaze = 0  # 場風
        self.kyoku = 0   # 局
        self.honba = 0   # 本場
        self.kyotaku = 0 # 供託

        self.turn = self.kyoku
        self.cur_player = self.players[self.turn]
        self.yama = Yama(self.mjhai_set) # 牌山

    # 局を表す文字列
    def kyoku_name(self):
        return "{}{}局".format(Game.kaze_name[self.bakaze], self.kyoku + 1)

    # 配牌
    def haipai(self):
        for player in self.players:
            player.haipai()

    # ツモ
    def tsumo(self):
        self.cur_player.tsumo()

    # 打牌
    def dahai(self):
        self.cur_player.dahai()

    # プレイヤーのツモ順を変更
    def change_player(self, chicha):
        self.turn = chicha
        self.cur_player = self.players[self.turn]

    # 次のプレイヤーへ
    def next_player(self):
        self.change_player((self.turn + 1) % self.players_num)

    # 次の局へ
    def next_kyoku(self, renchan, ryukyoku):
        if not renchan:
            self.kyoku += 1
            if self.kyoku >= self.players_num:
                self.kyoku = 0
                self.bakaze += 1

        if renchan or ryukyoku:
            self.honba += 1
        else:
            self.honba = 0

        self.change_player(self.kyoku)
        self.yama = Yama(self.mjhai_set) # 牌山

    # 局開始
    def start_kyoku(self):
        print(self.kyoku_name())
        print()

        self.haipai() # 配牌

        while self.yama.remain > 0:
            # ツモ
            if len(self.cur_player.tehai) % 3 <= 1:
                self.tsumo()

            if self.cur_player.check_tsumo():
                print("{}：ツモ".format(self.cur_player.name))
                for cur_yaku_list in self.cur_player.tehai.yaku():
                    for cur_yaku in cur_yaku_list:
                        print(self.yaku[cur_yaku][not self.cur_player.tehai.menzen], yaku_name[cur_yaku])

                return self.cur_player.jikaze() == 0, False

            if self.cur_player.check_ankan():
                continue

            # コンソール表示
            print("{} [残り{}]".format(self.cur_player.name, self.yama.remain))
            self.cur_player.tehai.show()

            # 打牌
            self.dahai()

            end = False
            renchan = False
            furo = False

            for check_player in self.players:
                # 自身は判定しない
                if check_player != self.cur_player:
                    if check_player.check_ron(self.cur_player):
                        print("{}→{}：ロン".format(self.cur_player.name, check_player.name))
                        for cur_yaku_list in check_player.tehai.yaku():
                            for cur_yaku in cur_yaku_list:
                                print(self.yaku[cur_yaku][not check_player.tehai.menzen], yaku_name[cur_yaku])

                        end = True
                        if check_player.jikaze() == 0:
                            renchan = True

            if end:
                return renchan, False

            for check_player in self.players:
                # 自身は判定しない
                if check_player != self.cur_player:
                    if check_player.check_furo(self.cur_player):
                        furo = True
                        self.change_player(check_player.chicha)
                        break

            if furo:
                continue

            print()
            self.next_player()

        print("流局")

        for player in self.players:
            print("{}：{}".format(player.name, "テンパイ" if player.tehai.shanten() <= 0 else "ノーテン"))

        return self.players[self.kyoku].tehai.shanten() <= 0, True

    # ゲーム開始
    def start(self):
        while self.bakaze <= 1:
            renchan, ryukyoku = self.start_kyoku()

            if ryukyoku:
                for player in self.players:
                    if player.richi:
                        self.kyotaku += 1
            else:
                self.kyotaku = 0

            self.next_kyoku(renchan, ryukyoku)

# グラフィカルなゲーム
class GraphicalGame(Game):
    kaze_name = ["東", "南", "西", "北"]

    def __init__(self, mjhai_set, yaku, players, point, view=None, open=False):
        self.screen = gp.Screen(self, view, open)
        super().__init__(mjhai_set, yaku, players, point)

    # 配牌
    def haipai(self):
        super().haipai()
        self.screen.draw()

    # ツモ
    def tsumo(self):
        super().tsumo()
        self.screen.draw()

    # 打牌
    def dahai(self):
        super().dahai()
        self.screen.draw()

    # 局開始
    def start_kyoku(self):
        renchan, ryukyoku = super().start_kyoku()
        self.screen.draw_result()
        return renchan, ryukyoku
