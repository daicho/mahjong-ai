import sys
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

# シャンテン数計算テーブルを読み込み
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
table_file = open(THIS_PATH + "/shanten_table.bin", "rb")
combi_table = pickle.load(table_file)
table_file.close()

# 麻雀牌
class MjHai():
    color_name = ["p", "s", "m", "Ton", "Nan", "Sha", "Pei", "Hak", "Hat", "Chn"]

    def __init__(self, color, number=0, dora=False):
        self.color = color   # 種類
        self.number = number # 数字
        self.kind = (color, number)
        self.dora = dora     # ドラかどうか
        self.name = MjHai.color_name[self.color] + \
                    (str(self.number) if self.number > 0 else "") + \
                    ("@" if self.dora else "")

    # 比較演算子
    def __eq__(self, other):
        return (self.color, self.number, self.dora) == (other.color, other.number, other.dora)

    def __lt__(self, other):
        return (self.color, self.number, self.dora) < (other.color, other.number, other.dora)

    def __gt__(self, other):
        return (self.color, self.number, self.dora) > (other.color, other.number, other.dora)

# 河の麻雀牌
class KawaMjHai(MjHai):
    def __init__(self, color, number=0, dora=False, tumogiri=False, richi=False, furo=False):
        self.tumogiri = tumogiri
        self.richi = richi
        self.furo = furo
        super().__init__(color, number, dora)

    def setup(self, tumogiri=False, richi=False, furo=False):
        self.tumogiri = tumogiri
        self.richi = richi
        self.furo = furo

# 手牌
class Tehai():
    """
    kind:
      0...雀頭
      1...順子
      2...暗刻
      3...両面塔子
      4...辺張塔子
      5...嵌張塔子
      6...対子
    """

    # 面子・面子候補探索用のノード
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
        self.table = collections.Counter()
        self.menzen = True

    # 追加
    def append(self, hai):
        self.list.append(hai)
        self.table[hai.kind] += 1

    # まとめて追加
    def extend(self, hais):
        for hai in hais:
            self.append(hai)

    # 番号で取り出し
    def pop(self, index=-1):
        hai = self.list.pop(index)
        self.table[hai.kind] -= 1
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
            start = 0
            for i in range(1, 10):
                if table[(color, i)] != 0:
                    start = i
                    break

            end = 0
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

        # 雀頭候補を考慮しないシャンテン数
        shanten_min = shanten_without_jantou(self.table)

        # 全ての雀頭候補を取り出してシャンテン数を計算
        for hai_kind in mjhai_all:
            if self.table[hai_kind] >= 2:
                self.table[hai_kind] -= 2
                shanten_min = min(shanten_min, shanten_without_jantou(self.table) - 1)
                self.table[hai_kind] += 2

        return shanten_min

    # 七対子のシャンテン数
    def shanten_7toitu(self):
        shanten_num = 6

        for hai_kind in mjhai_all:
            if self.table[hai_kind] >= 2:
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

# 河
class Kawa():
    def __init__(self):
        self.list = []

    # 追加
    def append(self, hai, tumogiri=False, richi=False, furo=False):
        hai.__class__ = KawaMjHai
        hai.setup(tumogiri, richi, furo)
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
    def __init__(self, name=""):
        self.name = name
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
        self.tehai.append(yama.pop())

    # 打牌
    def dahai(self, index):
        tumogiri = (index == 13 or index == -1)
        self.kawa.append(self.tehai.pop(index), tumogiri, self.richi)
        self.tehai.sort()

    # 選択
    @abstractmethod
    def select(self, players, mjhai_set):
        pass

# 人間
class Human(Player):
    # 選択
    def select(self, players, mjhai_set):
        # リーチをしていたらツモ切り
        if self.richi:
            return -1

        # 入力
        select_input = input(self.name + "> ")

        if select_input == "q":
            sys.exit()

        # ツモ切り
        elif select_input == "":
            return -1

        return int(select_input)
