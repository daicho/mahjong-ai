from .. import core

# 人間
class Human(core.Player):
    # 選択
    def select(self, players, mjhai_set):
        # リーチをしていたらツモ切り
        if self.richi:
            return -1

        # 入力
        select_input = input(self.name + "> ")

        if select_input == "q":
            sys.exit()

        # ツモ切り
        elif select_input == "":
            return -1

        return int(select_input)
