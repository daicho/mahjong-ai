from .. import core

# 多田AI
class TadaAi(core.Player):
    # 選択
    def select(self):
        return 13

    # 立直
    def call_richi(self):
        return True

    # ツモ和了
    def agari_tumo(self):
        return True

    # ロン和了
    def agari_ron(self, player):
        return True

    # 暗槓
    def ankan(self, hai_kind):
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
