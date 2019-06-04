import sys
from .. import core

# 人間
class Human(core.Player):
    # 選択
    def select(self, players, mjhai_set):
        # リーチをしていたらツモ切り
        if self.richi:
            return -1

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