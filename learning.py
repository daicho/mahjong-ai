from mahjong import *

# イーソー君
class Isokun(Player):
    # 選択
    def select(self, players=[], yama=[]):
        return 13

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
        MjHai(0, 9),
    ])

    isokun.tehai.show()
    print(isokun.select())
