from .. import system as mj

# 多田AI
class TadaAi(mj.Player):
    # 選択
    def select(self):
        return 13

    # ツモ和了
    def do_tsumo(self):
        return True

    # ロン和了
    def do_ron(self, target, whose):
        return True

    # 立直
    def do_richi(self):
        return True

    # 暗槓
    def do_ankan(self, target):
        return False

    # 明槓
    def do_minkan(self, hais, target, whose):
        return False

    # 加槓
    def do_kakan(self, target):
        return False

    # ポン
    def do_pon(self, hais, target, whose):
        return False

    # チー
    def do_chi(self, hais, target, whose):
        return False
