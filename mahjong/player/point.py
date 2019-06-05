from .. import core

# 多田AI
class TadaAi(core.Player):
    # 選択
    def select(self):
        return 13

    def agari_tumo(self):
        return True

    def agari_ron(self, player):
        return True
