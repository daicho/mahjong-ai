import sys
import copy
import random
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

    def __eq__(self, other):
        return (self.color, self.number, self.dora) == (other.color, other.number, other.dora)

    def __lt__(self, other):
        return (self.color, self.number, self.dora) < (other.color, other.number, other.dora)

    def __gt__(self, other):
        return (self.color, self.number, self.dora) > (other.color, other.number, other.dora)

# 河の麻雀牌
class KawaMjHai(MjHai):
    def __init__(self, color, number=0, dora=False):
        self.tumogiri = False
        self.richi = False
        self.furo = False
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
        def __init__(self, elememt, kind, shanten, node):
            self.element = elememt
            self.kind = kind
            self.shanten = shanten
            self.node = node

    # 面子・面子候補の組み合わせを探索
    @staticmethod
    def combi(table, shanten, count, atama):
        # テーブルを切り取り
        def cut(table, until):
            cut_table = copy.deepcopy(table)

            for pop_kind in mjhai_all:
                if pop_kind >= until:
                    break
                cut_table[pop_kind] = 0

            return cut_table

        tree = []
        shanten_min = 8

        if not atama:
            # 雀頭
            for hai_kind in mjhai_all:
                if table[hai_kind] >= 2:
                    table_pop = cut(table, hai_kind)
                    table_pop[hai_kind] -= 2

                    tree.append(Tehai.Node(
                        (hai_kind, hai_kind), 0, shanten - 1,
                        Tehai.combi(table_pop, shanten - 1, count, True)
                    ))

        if count < 4:
            # 順子
            for i in range(3):
                for j in range(1, 8):
                    if table[(i, j)] and table[(i, j + 1)] and table[(i, j + 2)]:
                        table_pop = cut(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 1)] -= 1
                        table_pop[(i, j + 2)] -= 1

                        tree.append(Tehai.Node(
                            ((i, j), (i, j + 1), (i, j + 2)), 1, shanten - 2,
                            Tehai.combi(table_pop, shanten - 2, count + 1, atama)
                        ))

            # 暗刻
            for hai_kind in mjhai_all:
                if table[hai_kind] >= 3:
                    table_pop = cut(table, hai_kind)
                    table_pop[hai_kind] -= 3

                    tree.append(Tehai.Node(
                        (hai_kind, hai_kind, hai_kind), 2, shanten - 2,
                        Tehai.combi(table_pop, shanten - 2, count + 1, atama)
                    ))

            # 両面塔子
            for i in range(3):
                for j in range(2, 8):
                    if table[(i, j)] and table[(i, j + 1)]:
                        table_pop = cut(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 1)] -= 1

                        tree.append(Tehai.Node(
                            ((i, j), (i, j + 1)), 3, shanten - 1,
                            Tehai.combi(table_pop, shanten - 1, count + 1, atama)
                        ))

            # 辺張塔子
            for i in range(3):
                for j in [1, 8]:
                    if table[(i, j)] and table[(i, j + 1)]:
                        table_pop = cut(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 1)] -= 1

                        tree.append(Tehai.Node(
                            ((i, j), (i, j + 1)), 4, shanten - 1,
                            Tehai.combi(table_pop, shanten - 1, count + 1, atama)
                        ))

            # 嵌張塔子
            for i in range(3):
                for j in range(1, 8):
                    if table[(i, j)] and table[(i, j + 2)]:
                        table_pop = cut(table, (i, j))
                        table_pop[(i, j)] -= 1
                        table_pop[(i, j + 2)] -= 1

                        tree.append(Tehai.Node(
                            ((i, j), (i, j + 2)), 5, shanten - 1,
                            Tehai.combi(table_pop, shanten - 1, count + 1, atama)
                        ))

            # 対子
            for hai_kind in mjhai_all:
                if table[hai_kind] >= 2:
                    table_pop = cut(table, hai_kind)
                    table_pop[hai_kind] -= 2

                    tree.append(Tehai.Node(
                        (hai_kind, hai_kind), 6, shanten - 1,
                        Tehai.combi(table_pop, shanten - 1, count + 1, atama)
                    ))

        return tree

    # 各ノードの最小シャンテン数を探索
    @staticmethod
    def shanten_min(tree):
        s_min = 8

        if len(tree) == 0:
            return s_min

        for leaf in tree:
            if leaf.shanten < s_min:
                s_min = leaf.shanten

            shanten = Tehai.shanten_min(leaf.node)
            if shanten < s_min:
                s_min = shanten

        return s_min

    def __init__(self):
        self.list = []
        self.menzen = True

    # 追加
    def append(self, hai):
        self.list.append(hai)

    # 結合
    def extend(self, hais):
        for hai in hais:
            self.append(hai)

    # 番号で取り出し
    def pop(self, index=-1):
        hai_pop = self.list.pop(index)
        return hai_pop

    # 牌を指定して取り出し
    def pop_mjhai(self, mjhai):
        for i, hai in enumerate(self.list):
            if hai == mjhai:
                return self.pop(i)

        return None

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

    # 通常手のシャンテン数計算
    def shanten_normal(self, table):
        return Tehai.shanten_min(Tehai.combi(table, 8, 0, False))

    # 国士無双のシャンテン数計算
    def shanten_kokushi(self, table):
        shanten_num = 13
        toitu = False

        for hai_kind in mjhai_yaochu:
            mjhai_num = table[hai_kind]

            if mjhai_num:
                shanten_num -= 1

            if mjhai_num >= 2 and not toitu:
                shanten_num -= 1
                toitu = True

        return shanten_num

    # 七対子のシャンテン数計算
    def shanten_7toitu(self, table):
        shanten_num = 6

        for hai_kind in mjhai_all:
            mjhai_num = table[hai_kind]
            if mjhai_num >= 2:
                shanten_num -= 1

        return shanten_num

    # シャンテン数計算
    def shanten(self):
        kind_list = []
        for hai in self.list:
            kind_list.append(hai.kind)

        table = collections.Counter(kind_list)
        return min(self.shanten_normal(table), self.shanten_7toitu(table), self.shanten_kokushi(table))

# 河
class Kawa():
    def __init__(self):
        self.list = []

    # 追加
    def append(self, hai, tumogiri=False, richi=False, furo=False):
        hai.__class__ = KawaMjHai
        hai.setup(tumogiri, richi, furo)
        self.list.append(hai)

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
    def __init__(self, name):
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
        self.kawa.append(self.tehai.pop(index), tumogiri)
        self.tehai.sort()

    # 選択
    @abstractmethod
    def select(self, players, yama):
        pass

# 人間
class Human(Player):
    # 選択
    def select(self, players=[], yama=[]):
        # 入力
        select_input = input(self.name + "> ")

        if select_input == "q":
            sys.exit()

        # ツモ切り
        elif select_input == "":
            return -1

        return int(select_input)

if __name__ == "__main__":
    tehai = Tehai()
    tehai.extend([
        MjHai(0, 2),
        MjHai(0, 2),
        MjHai(0, 3),
        MjHai(0, 3),
        MjHai(0, 4),
        MjHai(0, 4),
        MjHai(0, 5),
        MjHai(0, 5),
        MjHai(0, 6),
        MjHai(0, 6),
        MjHai(0, 7),
        MjHai(0, 7),
        MjHai(0, 8),
        MjHai(0, 8),
    ])

    tehai.show()
    print("{}シャンテン".format(tehai.shanten()))
