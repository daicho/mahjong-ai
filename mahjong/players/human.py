import sys
from .. import system as mj

# 人間
class Human(mj.Player):
    # 確認メッセージを表示
    def confirm(self, message, default=True):
        select_input = input("{}：{} [{}]> ".format(self.name, message, "Y/n" if default else "y/N"))

        if select_input == "":
            return default

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

            # ツモ切り
            elif select_input == "":
                return -1

            elif 0 <= int(select_input) < len(self.tehai):
                break

        return int(select_input)

    # ツモ和了
    def do_tsumo(self):
        return self.confirm("ツモる？", True)

    # ロン和了
    def do_ron(self, target, whose):
        return self.confirm("ロンする？", True)

    # 立直
    def do_richi(self):
        return self.confirm("立直する？", True)

    # 暗槓
    def do_ankan(self, target):
        return self.confirm("暗槓する？", False)

    # 明槓
    def do_minkan(self, hais, target, whose):
        return self.confirm("明槓する？", False)

    # 加槓
    def do_kakan(self, target):
        return self.confirm("加槓する？", False)

    # ポン
    def do_pon(self, hais, target, whose):
        return self.confirm("ポンする？", False)

    # チー
    def do_chi(self, hais, target, whose):
        return self.confirm("チーする？", False)
