import copy

if __name__ == "__main__":
    from core import *
else:
    from .core import *

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
        effect_max = 0
        cur_shanten = self.tehai.shanten()

        for i, hai in enumerate(self.tehai.list):
            pop_tehai = copy.deepcopy(self.tehai)
            pop_tehai.pop(i)

            if pop_tehai.shanten() <= cur_shanten:
                effect_count = 0

                for hai in yama.list:
                    pop_tehai.append(hai)
                    if pop_tehai.shanten() < cur_shanten:
                        effect_count += 1
                    pop_tehai.pop()
                
                if effect_count > effect_max:
                    effect_max = effect_count
                    select_index = i

        return select_index

if __name__ == "__main__":
    isokun = Fast()
    isokun.tehai.extend([
        MjHai(0, 1),
        MjHai(0, 2),
        MjHai(0, 5),
        MjHai(0, 7),
        MjHai(0, 8),
        MjHai(0, 9),
        MjHai(0, 9),
        MjHai(0, 1),
        MjHai(0, 1),
        MjHai(0, 5),
        MjHai(0, 5),
        MjHai(0, 6),
        MjHai(0, 9),
        MjHai(0, 9),
    ])

    isokun.tehai.show()
    print(isokun.select())
