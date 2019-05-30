from .core import *

# 多田AI
class TadaAi(Player):
    # 選択
    def select(self, players=[], yama=[]):
        return 13

if __name__ == "__main__":
    tada_ai = TadaAi("TadaAi")
    tada_ai.extend([
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

    tada_ai.tehai.show()
    print(tada_ai.select())
