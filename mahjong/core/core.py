import os
import copy
import random
import pickle
import itertools
import collections
from abc import ABCMeta, abstractmethod

"""
color:
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

number:
  0  ...字牌
  1-9...数牌
"""

# 全種の牌
mjhai_all = []

# 数牌
for i in range(3):
    for j in range(1, 10):
        mjhai_all.append((i, j))

# 字牌
for i in range(3, 10):
    mjhai_all.append((i, 0))

# 幺九牌
mjhai_yaochu = []

# 数牌
for i in range(3):
    for j in [1, 9]:
        mjhai_yaochu.append((i, j))

# 字牌
for i in range(3, 10):
    mjhai_yaochu.append((i, 0))

# 役
class Yaku():
    def __init__(self, name, fan):
        self.name = name
        self.fan = fan

# 役一覧
yaku_list = {
     0: Yaku("ドラ", (1, 1)),
     1: Yaku("裏ドラ", (1, 0)),
     2: Yaku("赤ドラ", (1, 1)),
     3: Yaku("ガリ", (1, 1)),
     4: Yaku("立直", (1, 0)),
     5: Yaku("門前清自摸和", (1, 0)),
     6: Yaku("一発", (1, 0)),
     7: Yaku("平和", (1, 0)),
     8: Yaku("一盃口", (1, 0)),
     9: Yaku("タンヤオ", (1, 1)),
    10: Yaku("役牌", (1, 1)),
    11: Yaku("海底摸月", (1, 1)),
    12: Yaku("河底撈魚", (1, 1)),
    13: Yaku("嶺上開花", (1, 1)),
    14: Yaku("槍槓", (1, 1)),
    15: Yaku("ダブル立直", (1, 0)),
    16: Yaku("一気通貫", (2, 1)),
    17: Yaku("チャンタ", (2, 1)),
    18: Yaku("三色同順", (2, 1)),
    19: Yaku("三色同刻", (2, 2)),
    20: Yaku("三暗刻", (2, 2)),
    21: Yaku("三槓子", (2, 2)),
    22: Yaku("対々和", (2, 2)),
    23: Yaku("小三元", (2, 2)),
    24: Yaku("混老頭", (2, 2)),
    25: Yaku("七対子", (2, 0)),
    26: Yaku("二盃口", (3, 0)),
    27: Yaku("純チャン", (3, 2)),
    28: Yaku("混一色", (3, 2)),
    29: Yaku("流し満貫", (5, 0)),
    30: Yaku("清一色", (6, 5)),
    31: Yaku("国士無双", (13, 0)),
    32: Yaku("四暗刻", (13, 0)),
    33: Yaku("字一色", (13, 13)),
    34: Yaku("大三元", (13, 13)),
    35: Yaku("大四喜", (26, 26)),
    36: Yaku("小四喜", (13, 13)),
    37: Yaku("緑一色", (13, 13)),
    38: Yaku("清老頭", (13, 13)),
    39: Yaku("四槓子", (13, 13)),
    40: Yaku("九蓮宝燈", (13, 0)),
    41: Yaku("天和", (13, 0)),
    42: Yaku("地和", (13, 0)),
    43: Yaku("人和", (13, 0)),
    44: Yaku("国士無双十三面待ち", (26, 0)),
    45: Yaku("四暗刻単騎待ち", (26, 0)),
    46: Yaku("純正九蓮宝燈", (26, 0)),
}

# シャンテン数計算テーブルを読み込み
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(THIS_PATH + "/shanten_table.bin", "rb") as table_file:
    combi_table = pickle.load(table_file)

# 麻雀牌
class MjHai():
    color_name = ["p", "s", "m", "Ton", "Nan", "Sha", "Pei", "Hak", "Hat", "Chn"]

    def __init__(self, color, number=0, dora=False):
        self.color = color    # 種類
        self.number = number  # 数字
        self.dora = dora      # ドラかどうか

        self.whose = None     # 誰のものか
        self.tumogiri = False # ツモ切り
        self.richi = False    # リーチ
        self.furo = False     # 副露

        self.name = MjHai.color_name[self.color] + \
                    (str(self.number) if self.number > 0 else "") + \
                    ("@" if self.dora else "")

    def put_kawa(self, tumogiri=False, richi=False, furo=False):
        self.tumogiri = tumogiri
        self.richi = richi
        self.furo = furo

    # 比較演算子
    def __eq__(self, other):
        return (self.color, self.number, self.dora) == (other.color, other.number, other.dora)

    def __lt__(self, other):
        return (self.color, self.number, self.dora) < (other.color, other.number, other.dora)

    def __gt__(self, other):
        return (self.color, self.number, self.dora) > (other.color, other.number, other.dora)

# 手牌
class Tehai():
    # 面子探索用のノード
    class Node():
        def __init__(self, elememt, kind, shanten, count, parent, children):
            self.element = elememt
            self.kind = kind
            self.shanten = shanten
            self.count = count
            self.parent = parent
            self.children = children

    # 面子・面子候補の組み合わせを探索
    @staticmethod
    def combi(table, shanten, count, jantou):
        # テーブルを切り取り
        def cut_table(table, until):
            cut_table = copy.deepcopy(table)

            for pop_kind in mjhai_all:
                if pop_kind >= until:
                    break
                cut_table[pop_kind] = 0

            return cut_table

        tree = Tehai.Node((), -1, 8, 4, None, [])

        if not jantou:
            # 雀頭
            for hai_kind in mjhai_all:
                if table[hai_kind] >= 2:
                    table_pop = cut_table(table, hai_kind)
                    table_pop[hai_kind] -= 2

                    tree.children.append(Tehai.Node(
                        (hai_kind, hai_kind), 0, shanten - 1, count, tree,
                        Tehai.combi(table_pop, shanten - 1, count, True).children
                    ))

        # 面子・面子候補は4つまで
        if count < 4:
            # 順子
            for i in range(3):
                for j in range(1, 8):
                    if table[(i, j)] and table[(i, j + 1)] and table[(i, j + 2)]:
                        table_pop = cut_table(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 1)] -= 1
                        table_pop[(i, j + 2)] -= 1

                        tree.children.append(Tehai.Node(
                            ((i, j), (i, j + 1), (i, j + 2)), 1, shanten - 2, count + 1, tree,
                            Tehai.combi(table_pop, shanten - 2, count + 1, jantou).children
                        ))

            # 暗刻
            for hai_kind in mjhai_all:
                if table[hai_kind] >= 3:
                    table_pop = cut_table(table, hai_kind)
                    table_pop[hai_kind] -= 3

                    tree.children.append(Tehai.Node(
                        (hai_kind, hai_kind, hai_kind), 2, shanten - 2, count + 1, tree,
                        Tehai.combi(table_pop, shanten - 2, count + 1, jantou).children
                    ))

            # 両面塔子
            for i in range(3):
                for j in range(2, 8):
                    if table[(i, j)] and table[(i, j + 1)]:
                        table_pop = cut_table(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 1)] -= 1

                        tree.children.append(Tehai.Node(
                            ((i, j), (i, j + 1)), 3, shanten - 1, count + 1, tree,
                            Tehai.combi(table_pop, shanten - 1, count + 1, jantou).children
                        ))

            # 辺張塔子
            for i in range(3):
                for j in [1, 8]:
                    if table[(i, j)] and table[(i, j + 1)]:
                        table_pop = cut_table(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 1)] -= 1

                        tree.children.append(Tehai.Node(
                            ((i, j), (i, j + 1)), 4, shanten - 1, count + 1, tree,
                            Tehai.combi(table_pop, shanten - 1, count + 1, jantou).children
                        ))

            # 嵌張塔子
            for i in range(3):
                for j in range(1, 8):
                    if table[(i, j)] and table[(i, j + 2)]:
                        table_pop = cut_table(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 2)] -= 1

                        tree.children.append(Tehai.Node(
                            ((i, j), (i, j + 2)), 5, shanten - 1, count + 1, tree,
                            Tehai.combi(table_pop, shanten - 1, count + 1, jantou).children
                        ))

            # 対子
            for hai_kind in mjhai_all:
                if table[hai_kind] >= 2:
                    table_pop = cut_table(table, hai_kind)
                    table_pop[hai_kind] -= 2

                    tree.children.append(Tehai.Node(
                        (hai_kind, hai_kind), 6, shanten - 1, count + 1, tree,
                        Tehai.combi(table_pop, shanten - 1, count + 1, jantou).children
                    ))

        return tree

    def __init__(self):
        self.list = []
        self.furo = []
        self.table = collections.Counter()
        self.menzen = True

    # 残り個数
    def __len__(self):
        return len(self.list)

    # 追加
    def append(self, *hais):
        for hai in hais:
            self.list.append(hai)
            self.table[(hai.color, hai.number)] += 1

    # 番号で取り出し
    def pop(self, index=-1):
        hai = self.list.pop(index)
        self.table[(hai.color, hai.number)] -= 1
        return hai

    # 並べ替え
    def sort(self):
        self.list.sort()

    # 表示
    def show(self):
        for hai in self.list:
            print(format(hai.name, "<4s"), end="")
        print()

        for j in range(len(self.list)):
            print(format(j, "<4d"), end="")
        print()

    # 通常手のシャンテン数
    def shanten_normal(self):
        # シャンテン数計算テーブル用のキーを作成
        def create_key(table, color):
            # 前後の0は切り取り
            for i in range(1, 10):
                if table[(color, i)] != 0:
                    start = i
                    break
            else: # 全て0だったら
                return (0,)

            for i in range(9, 0, -1):
                if table[(color, i)] != 0:
                    end = i
                    break

            combi_key = []
            for i in range(start, end + 1):
                combi_key.append(table[(color, i)])

            return tuple(combi_key)

        # 雀頭を考慮しないシャンテン数
        def shanten_without_jantou(table):
            shanten_min = 8

            # 孤立牌を除去
            opti_table = copy.deepcopy(table)
            for i in range(3):
                for j in range(1, 10):
                    if opti_table[(i, j)] == 1 and sum(opti_table[(i, j + k)] for k in [-2, -1, 1, 2]) == 0:
                        opti_table[(i, j)] = 0

            # 字牌の面子・面子候補
            jihai_combi = [0, 0]
            for i in range(3, 10):
                if opti_table[(i, 0)] >= 3:
                    jihai_combi[0] += 1

                if opti_table[(i, 0)] == 2:
                    jihai_combi[1] += 1

            # 全ての面子・面子候補の組み合わせ
            combi_all = itertools.product([tuple(jihai_combi)], *(combi_table[create_key(opti_table, i)] for i in range(3)))

            for cur_combi in combi_all:
                cur_shanten = 8
                count = 0

                # 面子から取り出し
                for i in range(2):
                    for elememt in cur_combi:
                        # 面子・面子候補は4つまで
                        if count + elememt[i] >= 4:
                            cur_shanten -= (2 if i == 0 else 1) * (4 - count)
                            count = 4
                            break
                        else:
                            cur_shanten -= (2 if i == 0 else 1) * elememt[i]
                            count = count + elememt[i]

                shanten_min = min(shanten_min, cur_shanten)

            return shanten_min

        # 雀頭なしのシャンテン数
        shanten_min = shanten_without_jantou(self.table)

        # 全ての雀頭候補を取り出してシャンテン数を計算
        for key in self.table:
            if self.table[key] >= 2:
                self.table[key] -= 2
                shanten_min = min(shanten_min, shanten_without_jantou(self.table) - 1)
                self.table[key] += 2

        return shanten_min

    # 七対子のシャンテン数
    def shanten_7toitu(self):
        shanten_num = 6

        for key in self.table:
            if self.table[key] >= 2:
                shanten_num -= 1

        return shanten_num

    # 国士無双のシャンテン数
    def shanten_kokushi(self):
        shanten_num = 13
        toitu = False

        for hai_kind in mjhai_yaochu:
            if self.table[hai_kind]:
                shanten_num -= 1

            if self.table[hai_kind] >= 2 and not toitu:
                shanten_num -= 1
                toitu = True

        return shanten_num

    # シャンテン数
    def shanten(self):
        return min(self.shanten_normal(), self.shanten_7toitu(), self.shanten_kokushi())

    # 役
    def yaku(self):
        if self.shanten() > -1:
            return []

        if self.shanten_kokushi() == -1:
            return [[31]]

        # 和了時の面子の組み合わせを探索
        combi_agari = []

        # 全ての雀頭候補を取り出す
        for key in self.table:
            if self.table[key] >= 2:
                self.table[key] -= 2

                # 0...順子 1...暗刻
                mentu_combi = itertools.product([0, 1], repeat=4)

                # 左から順番に面子を取り出し
                for cur_combi in mentu_combi:
                    append_combi = [[(key, key)], [], []]
                    temp_table = copy.deepcopy(self.table)

                    for mentu in cur_combi:
                        # 開始点
                        for hai_kind in mjhai_all:
                            if temp_table[hai_kind]:
                                i, j = hai_kind
                                break

                        if mentu == 0:
                            # 順子
                            if temp_table[(i, j)] and temp_table[(i, j + 1)] and temp_table[(i, j + 2)]:
                                append_combi[1].append(tuple((i, j + k) for k in range(3)))
                                for k in range(3):
                                    temp_table[(i, j + k)] -= 1
                            else:
                                break
                        else:
                            # 暗刻
                            if temp_table[(i, j)] >= 3:
                                append_combi[2].append(tuple((i, j) for k in range(3)))
                                temp_table[(i, j)] -= 3
                            else:
                                break
                    else:
                        combi_agari.append(append_combi)

                self.table[key] += 2

        print(combi_agari)

        # 役の一覧
        yaku_agari = []
        yaku_common = []

        # タンヤオ
        for hai_kind in mjhai_yaochu:
            if self.table[hai_kind] > 0:
                break
        else:
            yaku_common.append(9)

        # 混一色・清一色
        append_id = 30
        for i in range(3):
            for key in self.table:
                if self.table[key] > 0 and key[0] != i:
                    if key[0] >= 3:
                        append_id = 28
                    else:
                        break
            else:
                yaku_common.append(append_id)

        # 混老頭・清老頭
        routou = False
        append_id = 38
        for key in self.table:
            if self.table[key] > 0:
                if 2 <= key[1] <= 8:
                    break
                elif key[0] >= 3:
                    append_id = 24
        else:
            routou = True
            yaku_common.append(append_id)

        # 七対子
        if self.shanten_7toitu() == -1:
            yaku_agari.append(yaku_common + [25])

        for cur_combi in combi_agari:
            yaku_append = yaku_common[:]

            # 平和
            if len(cur_combi[1]) == 4:
                yaku_append.append(7)

            # 一盃口
            if len(cur_combi[1]) != len(set(cur_combi[1])):
                yaku_append.append(8)

            # 一気通貫
            for i in range(3):
                for j in range(3):
                    if not ((i, j * 3 + 1), (i, j * 3 + 2), (i, j * 3 + 3)) in cur_combi[1]:
                        break
                else:
                    yaku_append.append(16)

            # 三色同順
            for i in range(1, 10):
                for j in range(3):
                    if not ((j, i), (j, i + 1), (j, i + 2)) in cur_combi[1]:
                        break
                else:
                    yaku_append.append(18)

            # 三色同刻
            for i in range(1, 10):
                for j in range(3):
                    if not ((j, i), (j, i), (j, i)) in cur_combi[2]:
                        break
                else:
                    yaku_append.append(19)

            # 役牌
            for anko in cur_combi[2]:
                if anko[0][0] >= 3:
                    yaku_append.append(10)

            # チャンタ・純チャン
            if not routou:
                append_id = 27
                for elements in cur_combi:
                    for element in elements:
                        for hai_kind in element:
                            if hai_kind[1] == 1 or hai_kind[1] == 9:
                                break
                            elif hai_kind[0] >= 3:
                                append_id = 17
                                break
                        else:
                            break
                    else:
                        continue
                    break
                else:
                    yaku_append.append(append_id)

            # 三暗刻
            if len(cur_combi[2]) == 3:
                yaku_append.append(20)

            # 四暗刻
            if len(cur_combi[2]) == 4:
                yaku_append.append(32)

            yaku_agari.append(yaku_append)

        for yakus in yaku_agari:
            for yaku in yakus:
                print(yaku_list[yaku].name)
            print()

        return yaku_agari

# 河
class Kawa():
    def __init__(self):
        self.list = []

    # 追加
    def append(self, hai, tumogiri=False, richi=False, furo=False):
        hai.put_kawa(tumogiri, richi, furo)
        self.list.append(hai)

# 山
class Yama():
    def __init__(self, mjhai_set):
        self.list = mjhai_set[:]
        random.shuffle(self.list)
    
    # 取り出し
    def pop(self):
        return self.list.pop()

    # 残り個数
    def __len__(self):
        return len(self.list)

# プレイヤー
class Player(metaclass=ABCMeta):
    def __init__(self, name, chicha):
        self.name = name
        self.chicha = chicha
        self.tehai = Tehai()
        self.kawa = Kawa()
        self.richi = False

    # 配牌
    def haipai(self, yama):
        for i in range(13):
            self.tumo(yama)
        self.tehai.sort()

    # 自摸
    def tumo(self, yama):
        pop_hai = yama.pop()
        pop_hai.whose = self
        self.tehai.append(pop_hai)

    # 打牌
    def dahai(self, index):
        tumogiri = (index == 13 - len(self.tehai.furo) or index == -1)
        self.kawa.append(self.tehai.pop(index), tumogiri, self.richi)
        self.tehai.sort()

    # ツモ和了
    def agari_tumo(self):
        if self.tehai.shanten() == -1:
            return True
        else:
            return False

    # ロン和了
    def agari_ron(self, player):
        self.tehai.append(player.kawa.list[-1])

        if self.tehai.shanten() == -1:
            player.kawa.list[-1].furo = True
            return True
        else:
            self.tehai.pop()
            return False

    # 選択
    @abstractmethod
    def select(self, players, mjhai_set):
        pass
