from .. import core as mj

# イーソー君
class Isokun(mj.Player):
    # 選択
    def select(self):
        return 13

    # ツモ和了するか
    def do_tsumo(self):
        return True

    # ロン和了するか
    def do_ron(self, target, whose):
        return True

    # 立直するか
    def do_richi(self):
        return True

    # 暗槓するか
    def do_ankan(self, target):
        return False

    # 明槓するか
    def do_minkan(self, hais, target, whose):
        return False

    # 加槓するか
    def do_kakan(self, target):
        return False

    # ポンするか
    def do_pon(self, hais, target, whose):
        return False

    # チーするか
    def do_chi(self, hais, target, whose):
        return False
