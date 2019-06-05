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

    def agari_tumo(self):
        return True

    def agari_ron(self, player):
        return True
