import sys
from .. import core

# 人間
class Human(core.Player):
    # 確認メッセージを表示
    def confirm(self, message, default_yes=True):
        select_input = input("{}：{} [{}]> ".format(self.name, message, "Y/n" if default_yes else "y/N"))

        if select_input == "":
            return default_yes

        if select_input == "Y" or select_input == "y":
            return True
        elif select_input == "N" or select_input == "n":
            return False

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

    # 立直
    def call_richi(self):
        return self.confirm("立直する？", True)

    # ツモ和了
    def agari_tumo(self):
        return self.confirm("ツモる？", True)

    # ロン和了
    def agari_ron(self, player):
        return self.confirm("ロンする？", True)

    # 暗槓
    def ankan(self, hai_kind):
        return self.confirm("暗槓する？", False)

    # 明槓
    def minkan(self, player):
        return self.confirm("明槓する？", False)

    # 加槓
    def kakan(self):
        return self.confirm("加槓する？", False)

    # ポン
    def pon(self, player):
        return self.confirm("ポンする？", False)

    # チー
    def chi(self, player):
        return self.confirm("チーする？", False)
