import collections
import copy
import itertools
import os
import pickle
import random
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

for i in range(3):
    for j in range(1, 10):
        mjhai_all.append((i, j))

for i in range(3, 10):
    mjhai_all.append((i, 0))

# 幺九牌
mjhai_yaochu = []

for i in range(3):
    for j in [1, 9]:
        mjhai_yaochu.append((i, j))

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
        self.kind = (self.color, self.number)
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

    # 挿入
    def insert(self, index, hai):
        self.list.insert(index, hai)
        self.table[(hai.color, hai.number)] += 1

    # 番号で取り出し
    def pop(self, index=-1):
        hai = self.list.pop(index)
        self.table[(hai.color, hai.number)] -= 1
        return hai

    # 種類で取り出し
    def pop_kind(self, kind):
        for hai in self.list:
            if hai.kind == kind:
                self.list.remove(hai)
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
            combi_key = []

            for i in range(1, 10):
                # 孤立牌は除去
                if table[(color, i)] == 1 and sum(table[(color, i + j)] for j in [-2, -1, 1, 2]) == 0:
                    combi_key.append(0)
                else:
                    combi_key.append(table[(color, i)])

            # 前後の0は切り取り
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
        def shanten_without_jantou(table, furo_num):
            shanten_min = 8 - len(self.furo) * 2

            # 字牌の面子・面子候補
            jihai_combi = [0, 0]
            for i in range(3, 10):
                if table[(i, 0)] >= 3:
                    jihai_combi[0] += 1

                if table[(i, 0)] == 2:
                    jihai_combi[1] += 1

            # 全ての面子・面子候補の組み合わせ
            combi_all = itertools.product([tuple(jihai_combi)], *(combi_table[create_key(self.table, i)] for i in range(3)))

            for cur_combi in combi_all:
                cur_shanten = 8 - furo_num * 2
                count = 0

                # 面子から取り出し
                for i in range(2):
                    for elememt in cur_combi:
                        if count + elememt[i] >= 4 - furo_num:
                            cur_shanten -= (2 if i == 0 else 1) * (4 - furo_num - count)
                            count = 4 - furo_num
                            break
                        else:
                            cur_shanten -= (2 if i == 0 else 1) * elememt[i]
                            count = count + elememt[i]

                shanten_min = min(shanten_min, cur_shanten)

            return shanten_min

        # 雀頭なしのシャンテン数
        shanten_min = shanten_without_jantou(self.table, len(self.furo))

        # 全ての雀頭候補を取り出してシャンテン数を計算
        for key in self.table:
            if self.table[key] >= 2:
                self.table[key] -= 2
                shanten_min = min(shanten_min, shanten_without_jantou(self.table, len(self.furo)) - 1)
                self.table[key] += 2

        return shanten_min

    # 七対子のシャンテン数
    def shanten_7toitu(self):
        if not self.menzen:
            return 13

        shanten_num = 6

        for key in self.table:
            if self.table[key] >= 2:
                shanten_num -= 1

        return shanten_num

    # 国士無双のシャンテン数
    def shanten_kokushi(self):
        if not self.menzen:
            return 13

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
                        for i in range(10):
                            for j in range(10):
                                if temp_table[(i, j)]:
                                    break
                            else:
                                continue
                            break

                        if mentu == 0:
                            # 順子
                            if temp_table[(i, j)] and temp_table[(i, j + 1)] and temp_table[(i, j + 2)]:
                                append_combi[1].append(((i, j), (i, j + 1), (i, j + 2)))
                                for k in range(3):
                                    temp_table[(i, j + k)] -= 1
                            else:
                                break
                        else:
                            # 暗刻
                            if temp_table[(i, j)] >= 3:
                                append_combi[2].append(((i, j), (i, j), (i, j)))
                                temp_table[(i, j)] -= 3
                            else:
                                break
                    else:
                        combi_agari.append(append_combi)

                self.table[key] += 2

        # 全ての組み合わせでの役
        yaku_agari = []
        yaku_common = []
        yakuman = False

        # 役満から先に調べる
        # 字一色
        for key in self.table:
            if self.table[key] > 0 and key[0] < 3:
                break
        else:
            yaku_common.append(33)

        # 緑一色
        for key in self.table:
            if self.table[key] > 0 and not key in [(1, 2), (1, 3), (1, 4), (1, 6), (1, 8), (8, 0)]:
                break
        else:
            yaku_common.append(37)

        # 九蓮宝燈
        for i in range(3):
            for j in range(1, 10):
                if self.table[(i, j)] < (3 if j == 1 or j == 9 else 1):
                    break
            else:
                yaku_common.append(40)

        if len(yaku_common):
            yakuman = True
        else:
            # タンヤオ
            for key in self.table:
                if self.table[key] > 0 and not 2 <= key[1] <= 8:
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
                    if key[0] >= 3:
                        append_id = 24
                    if 2 <= key[1] <= 8:
                        break
            else:
                routou = True
                yaku_common.append(append_id)

            # 七対子
            if self.shanten_7toitu() == -1:
                yaku_agari.append(yaku_common + [25])

        for cur_combi in combi_agari:
            yaku_append = yaku_common[:] if yakuman else []

            # 四暗刻
            if len(cur_combi[2]) == 4:
                yaku_append.append(32)

            # 大四喜
            for i in range(3, 7):
                if not ((i, 0), (i, 0), (i, 0)) in cur_combi[2]:
                    break
            else:
                yaku_append.append(35)
            
            # 小四喜
            for i in range(3, 7):
                if cur_combi[0][0] == ((i, 0), (i, 0)):
                    for j in range(3, 7):
                        if j != i and not ((j, 0), (j, 0), (j, 0)) in cur_combi[2]:
                            break
                    else:
                        yaku_append.append(36)
                    
            # 大三元
            for i in range(7, 10):
                if not ((i, 0), (i, 0), (i, 0)) in cur_combi[2]:
                    break
            else:
                yaku_append.append(34)

            if len(yaku_append) == 0:
                yaku_append = yaku_common[:]

                # 平和
                if len(cur_combi[1]) == 4:
                    yaku_append.append(7)

                # 一盃口・二盃口
                append_id = 0
                for i in range(3):
                    for j in range(1, 8):
                        if cur_combi[1].count(((i, j), (i, j + 1), (i, j + 2))) >= 4:
                            append_id = 26

                        elif cur_combi[1].count(((i, j), (i, j + 1), (i, j + 2))) >= 2:
                            if (append_id == 0):
                                append_id = 8
                            else:
                                append_id = 26
                
                if append_id:
                    yaku_append.append(append_id)

                # 一気通貫
                for i in range(3):
                    for j in range(3):
                        if not ((i, j * 3 + 1), (i, j * 3 + 2), (i, j * 3 + 3)) in cur_combi[1]:
                            break
                    else:
                        yaku_append.append(16)

                # 三色同順
                for i in range(1, 8):
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

            yaku_agari.append(yaku_append)

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
        self.list = copy.deepcopy(mjhai_set)
        random.shuffle(self.list)
    
    # 取り出し
    def pop(self):
        return self.list.pop()

    # 残り個数
    def __len__(self):
        return len(self.list) - 14

# プレイヤー
class Player(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        self.tehai = Tehai()
        self.kawa = Kawa()

        self.point = 35000
        self.richi = False

    def setup(self, chicha, game):
        self.chicha = chicha
        self.game = game

    # 配牌
    def haipai(self):
        for i in range(13):
            self.tumo()
        self.tehai.sort()

    # 自摸
    def tumo(self):
        pop_hai = self.game.yama.pop()
        pop_hai.whose = self
        self.tehai.append(pop_hai)

    # 打牌
    def dahai(self):
        # リーチをしていたらツモ切り
        index = -1 if self.richi else self.select()

        tumogiri = (index == 13 - len(self.tehai.furo) * 3 or index == -1)
        self.kawa.append(self.tehai.pop(index), tumogiri, self.richi)
        self.tehai.sort()

    # ツモ・暗槓・加槓チェック
    def check_self(self):
        if self.tehai.shanten() == -1:
            return self.agari_tumo
        else:
            return False

    # ロン・明槓・ポン・チーチェック
    def check_other(self, player):
        check_hai = player.kawa.list[-1]
        self.tehai.append(check_hai)

        # ロン
        if self.tehai.shanten() == -1 and self.agari_ron(player):
            check_hai.furo = True
            return True

        if not self.richi:
            # 明槓
            if self.tehai.table[check_hai.kind] >= 4 and self.minkan(player):
                check_hai.furo = True
                self.tehai.furo.append([self.tehai.pop_kind(check_hai.kind) for i in range(4)])
                return False

            # ポン
            if self.tehai.table[check_hai.kind] >= 3 and self.pon(player):
                check_hai.furo = True
                self.tehai.furo.append([self.tehai.pop_kind(check_hai.kind) for i in range(3)])
                self.game.change_player(self.chicha)
                self.dahai()
                self.game.next_player()
                return False

        self.tehai.pop()
        return False

    # 選択
    @abstractmethod
    def select(self):
        pass

    # ツモ和了
    @abstractmethod
    def agari_tumo(self):
        pass

    # ロン和了
    @abstractmethod
    def agari_ron(self, player):
        pass

    # 暗槓
    @abstractmethod
    def ankan(self):
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
    bakaze_name = ["東", "南", "西", "北"]

    def __init__(self, mjhai_set, players):
        self.mjhai_set = mjhai_set
        self.players_num = len(players)
        self.players = random.sample(players, self.players_num)

        for i, player in enumerate(self.players):
            player.setup(i, self)

        self.bakaze = 0
        self.kyoku = 0

        self.cur = self.kyoku
        self.cur_player = self.players[self.cur]

        self.yama = Yama(mjhai_set)

    # 局を表す文字列
    def kyoku_name(self):
        return "{}{}局".format(Game.bakaze_name[self.bakaze], self.kyoku + 1)

    # ツモ
    def tumo(self):
        self.cur_player.tumo()
        return self.cur_player.check_self()

    # 打牌
    def dahai(self):
        self.cur_player.dahai()

        for check_player in self.players:
            # 自身は判定しない
            if check_player != self.cur_player:
                if check_player.check_other(self.cur_player):
                    return True
                    break
        else:
            return False

    # プレイヤーのツモ順を変更
    def change_player(self, chicha):
        self.cur = chicha
        self.cur_player = self.players[self.cur]

    # 次のプレイヤーへ
    def next_player(self):
        self.change_player((self.cur + 1) % self.players_num)
