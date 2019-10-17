import copy
import itertools
import pickle
import collections
from .core import *

# シャンテン数計算テーブルを読み込み
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(THIS_PATH + "/shanten_table.bin", "rb") as table_file:
    combi_table = pickle.load(table_file)

# 手牌
class Tehai():
    def __init__(self, hais=[], furos=[]):
        self.hais = hais[:]
        self.furos = furos[:]

        self.table = collections.Counter()
        for hai in self.hais:
            self.table[hai.kind] += 1

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

    # 複数の牌を検索
    def find_multi(self, kinds):
        temp_kinds = kinds[:]
        found_hais = []

        for hai in self.hais + [self.tsumo_hai]:
            for kind in temp_kinds:
                if hai is not None and hai.kind == kind:
                    found_hais.append(hai)
                    temp_kinds.remove(kind)
                    break
        return found_hais

    # 並べ替え
    def sort(self):
        self.hais.sort()

    # 和了時の面子の組み合わせを探索
    def combi_agari(self):
        return_combi = []

        # 全ての雀頭候補を取り出す
        for kind, count in self.table.items():
            if count >= 2:
                self.table[kind] -= 2

                # 0...順子 1...暗刻
                mentsu_combi = itertools.product([0, 1], repeat=4 - len(self.furos))

                # 左から順番に面子を取り出し
                for cur_combi in mentsu_combi:
                    temp_combi = self.furos + [Element([self.find(kind), self.find(kind)], ElementKind.JANTOU)]
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
                                temp_combi.append(Element([self.find((i, j)), self.find((i, j + 1)), self.find((i, j + 2))], ElementKind.SHUNTSU))
                                for k in range(3):
                                    temp_table[(i, j + k)] -= 1
                            else:
                                break
                        else:
                            # 暗刻
                            if temp_table[(i, j)] >= 3:
                                temp_combi.append(Element([self.find((i, j)), self.find((i, j)), self.find((i, j))], ElementKind.ANKO))
                                temp_table[(i, j)] -= 3
                            else:
                                break
                    else:
                        return_combi.append(temp_combi)

                self.table[kind] += 2

        return return_combi

    # 暗槓可能な牌
    def ankan_able(self):
        for kind, count in self.table.items():
            if count >= 4:
                yield self.find_multi([kind for i in range(4)])

    # 加槓可能な牌
    def kakan_able(self):
        for furo in self.furos:
            if furo.kind == ElementKind.MINKO:
                for kind, count in self.table.items():
                    # 明刻と同じ牌だったら
                    if count > 0 and furo.hais[0].kind == kind:
                        yield self.find(kind)

    # 明槓可能な牌
    def minkan_able(self, target):
        if self.table[target.hai.kind] >= 3:
            yield self.find_multi([target.hai.kind for i in range(3)])

    # ポン可能な牌
    def pon_able(self, target):
        if self.table[target.hai.kind] >= 2:
            yield self.find_multi([target.hai.kind for i in range(2)])

    # チー可能な牌
    def chi_able(self, target):
        for i in range(-2, 1):
            for j in range(3):
                if i + j and self.table[(target.hai.kind[0], target.hai.kind[1] + i + j)] == 0:
                    break
            else:
                yield self.find_multi([(target.hai.kind[0], target.hai.kind[1] + i + j) for j in range(3) if i + j])

    # 暗槓
    def ankan(self, hais):
        append_hais = [self.remove(hai) for hai in hais]
        self.furos.append(Element(append_hais, ElementKind.ANKAN))

    # 加槓
    def kakan(self, hai):
        for furo in self.furos:
            if furo.kind == ElementKind.MINKO:
                # 明刻と同じ牌だったら
                if furo.hais[0].kind == hai.kind:
                    furo.kakan(self.remove(hai))

    # 明槓
    def minkan(self, hais, target, direct):
        self.menzen = False

        append_hais = [self.remove(hai) for hai in hais]
        append_hais.insert(int((direct - 1) * 1.5), target.hai)
        self.furos.append(FuroElement(append_hais, ElementKind.MINKAN, direct))

    # ポン
    def pon(self, hais, target, direct):
        self.menzen = False

        append_hais = [self.remove(hai) for hai in hais]
        append_hais.insert(direct - 1, target.hai)
        self.furos.append(PonElement(append_hais, ElementKind.MINKO, direct))

    # チー
    def chi(self, hais, target, direct):
        self.menzen = False

        append_hais = [self.remove(hai) for hai in hais]
        append_hais.insert(direct - 1, target.hai)
        self.furos.append(FuroElement(append_hais, ElementKind.MINSHUN, direct))

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
