from .core import *

# 多田AI
class TadaAi(Player):
    # 選択
    def select(self, players, mjhai_set):
        # リーチをしていたらツモ切り
        if self.richi:
            return -1

        return random.randrange(0, 14)
