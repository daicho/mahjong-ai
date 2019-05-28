import sys
import random
from abc import ABCMeta, abstractmethod

# 麻雀牌
class MjHai():
    color_name = ["p", "s", "m", "Ton", "Nan", "Sha", "Pei", "Hak", "Hat", "Chn"]

    def __init__(self, color, number = 0, dora = False):
        self.color = color   # 種類
        self.number = number # 数字
        self.dora = dora     # ドラかどうか
        self.id = self.color * 10 + self.number # ソート用ID
        self.name = MjHai.color_name[self.color] + \
                    (str(self.number) if self.number > 0 else "") + \
                    ("@" if self.dora else "")

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

# 手牌
class Tehai(list):
    def __init__(self):
        self.list = []
        self.menzen = True

    # 追加
    def append(self, hai):
        self.list.append(hai)

    # 取り出し
    def pop(self, index=-1):
        return self.list.pop(index)

    # 並べ替え
    def sort(self):
        self.list.sort()

    # 表示
    def show(self):
        for hai in self.list:
            print(format(hai.name, "<4s"), end="")
        print()

        for j in range(len(self)):
            print(format(j, "<4d"), end="")
        print()

    def shanten(self):
        pass

# 河
class Kawa():
    def __init__(self):
        self.list = []

    # 追加
    def append(self, hai):
        self.list.append(hai)

    # 取り出し
    def pop(self, index=-1):
        return self.list.pop(index)

# プレイヤー
class Player():
    def __init__(self, name):
        self.name = name
        self.tehai = Tehai()
        self.kawa = []

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
        self.kawa.append(self.tehai.pop(index))
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
