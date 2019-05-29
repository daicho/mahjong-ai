import sys
import random
from abc import ABCMeta, abstractmethod

# 麻雀牌
class MjHai():
    color_name = ["p", "s", "m", "Ton", "Nan", "Sha", "Pei", "Hak", "Hat", "Chn"]

    def __init__(self, color, number=0, dora=False):
        self.color = color   # 種類
        self.number = number # 数字
        self.dora = dora     # ドラかどうか
        self.id = self.color * 10 * 2 + self.number * 2 + int(self.dora) # 識別用ID
        self.name = MjHai.color_name[self.color] + \
                    (str(self.number) if self.number > 0 else "") + \
                    ("@" if self.dora else "")

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

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

        for j in range(len(self.list)):
            print(format(j, "<4d"), end="")
        print()

    # 検索
    def find(self, find_hai):
        count = 0
        for hai in self.list:
            if hai == find_hai:
                count += 1

        return count

    # シャンテン数計算
    def shanten_kokushi(self):
        shanten_num = 13
        toitu = False

        for color in range(0, 10):
            for number in [0, 1, 9]:
                mjhai_num = self.find(MjHai(color, number))
                if mjhai_num:
                    shanten_num -= 1

                if mjhai_num >= 2 and not toitu:
                    shanten_num -= 1
                    toitu = True

        return shanten_num

    def shanten(self):
        return self.shanten_kokushi()

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
