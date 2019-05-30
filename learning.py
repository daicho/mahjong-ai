import copy
from mahjong import *

# イーソー君
class Isokun(Player):
    # 選択
    def select(self, players=[], yama=[]):
        select_index = 13
        return select_index

# 最速
class Fast(Player):
    # 選択
    def select(self, players=[], yama=[]):
        select_index = -1
        shanten_min = 13

        for i, hai in enumerate(self.tehai.list):
            pop_tehai = copy.deepcopy(self.tehai)
            pop_tehai.pop(i)

            shanten_num = pop_tehai.shanten()
            if shanten_num <= shanten_min:
                select_index = i
                shanten_min = shanten_num

        return select_index

if __name__ == "__main__":
    isokun = Isokun("Isokun")
    isokun.tehai.extend([
        MjHai(0, 1),
        MjHai(0, 1),
        MjHai(0, 1),
        MjHai(0, 2),
        MjHai(0, 3),
        MjHai(0, 4),
        MjHai(0, 5),
        MjHai(0, 5),
        MjHai(0, 6),
        MjHai(0, 7),
        MjHai(0, 8),
        MjHai(0, 9),
        MjHai(0, 9),
        MjHai(0, 9)
    ])

    isokun.tehai.show()
    print(isokun.select())
