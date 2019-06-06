import sys
from .. import core

# 人間
class Human(core.Player):
    # 選択
    def select(self):
        # 入力
        while True:
            select_input = input(self.name + "> ")

            if select_input == "q":
                sys.exit()

            # リーチ
            elif select_input == "r" and self.tehai.shanten() <= 0:
                print("リーチ")
                self.richi = True

            # ツモ切り
            elif select_input == "":
                return -1

            elif 0 <= int(select_input) < 14:
                break

        return int(select_input)

    # ツモ和了
    def agari_tumo(self):
        return True

    # ロン和了
    def agari_ron(self, player):
        return True

    # 暗槓
    def ankan(self):
        return False

    # 明槓
    def minkan(self, player):
        return False

    # 加槓
    def kakan(self):
        return False

    # ポン
    def pon(self, player):
        return False

    # チー
    def chi(self, player):
        return False
