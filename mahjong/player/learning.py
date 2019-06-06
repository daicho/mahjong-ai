import copy
from .. import core

# イーソー君
class Isokun(core.Player):
    # 選択
    def select(self):
        return 13

    # ツモ和了
    def agari_tumo(self):
        return True

    # ロン和了
    def agari_ron(self, player):
        return True

    # 暗槓
    def ankan(self):
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

# 手なりAI
class Tenari(core.Player):
    # 選択
    def select(self):
        select_index = -1
        effect_max = 0
        cur_shanten = self.tehai.shanten()

        # 残っている牌
        remain_hai = self.game.mjhai_set[:]

        # 自身の手牌
        for hai in self.tehai.list:
            remain_hai.remove(hai)

        # 河
        for player in self.game.players:
            for hai in player.kawa.list:
                remain_hai.remove(hai)

        # ドラ
        remain_hai.remove(self.game.yama.list[0])

        for i in range(len(self.tehai)):
            # 1枚ずつ切ってみる
            pop_hai = self.tehai.pop(i)

            # シャンテン数が進むなら
            if self.tehai.shanten() <= cur_shanten:
                effect_count = 0

                # 残り全ての牌をツモってみる
                for hai in remain_hai:
                    # 有効牌の数をカウント
                    self.tehai.append(hai)
                    if self.tehai.shanten() < cur_shanten:
                        effect_count += 1
                    self.tehai.pop()

                # 有効牌が一番多い牌を選択
                if effect_count > effect_max:
                    effect_max = effect_count
                    select_index = i

            self.tehai.insert(i, pop_hai)

        # 待ち牌が2枚以上残っていたらリーチ
        if self.tehai.shanten() <= 0 and effect_max >= 2:
            print("リーチ")
            self.richi = True

        return select_index

    # ツモ和了
    def agari_tumo(self):
        return True

    # ロン和了
    def agari_ron(self, player):
        return True

    # 暗槓
    def ankan(self):
        return True

    # 明槓
    def minkan(self, player):
        return False

    # 加槓
    def kakan(self):
        return True

    # ポン
    def pon(self, player):
        return True

    # チー
    def chi(self, player):
        return True
