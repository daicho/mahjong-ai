import random

# 麻雀牌
class MjHai():
    color_name = ["p", "s", "m", "東", "南", "西", "北", "白", "發", "中"]

    def __init__(self, color, number = 0, dora = False):
        self.color = color   # 種類
        self.number = number # 数字
        self.dora = dora     # ドラかどうか
        self.id = self.color * 10 + self.number # ソート用ID

    def __str__(self):
        return (str(self.number) if self.number > 0 else "") + MjHai.color_name[self.color]
    
    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

# ゲーム
class Game():
    def __init__(self, player_num, mjhai_set):
        self.player_num = player_num # プレイヤーの人数
        self.yama = mjhai_set        # 山
        self.tehai = [[] for i in range(player_num)] # 手牌
        self.kawa  = [[] for i in range(player_num)] # 河
        random.shuffle(self.yama)

    # 配牌
    def haipai(self):
        for i in range(self.player_num):
            for j in range(13):
                self.tumo(i)
            self.tehai[i].sort()

    # 自摸
    def tumo(self, player):
        self.tehai[player].append(self.yama.pop())

    # 打牌
    def dahai(self, player, index = -1):
        self.kawa[player].append(self.tehai[player].pop(index))
        self.tehai[player].sort()

    # 手牌を表示
    def show(self, player):
        for hai in self.tehai[player]:
            print(str(hai) + " ", end="")
        print()
