import copy
from .. import core

# イーソー君
class Isokun(core.Player):
    # 選択
    def select(self):
        return 13

    def agari_tumo(self):
        return True

    def agari_ron(self, player):
        return True

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

        for i, hai in enumerate(self.tehai.list):
            # 1枚ずつ切ってみる
            pop_tehai = copy.deepcopy(self.tehai)
            pop_tehai.pop(i)

            # シャンテン数が進むなら
            if pop_tehai.shanten() <= cur_shanten:
                effect_count = 0

                # 残り全ての牌をツモってみる
                for hai in remain_hai:
                    # 有効牌の数をカウント
                    pop_tehai.append(hai)
                    if pop_tehai.shanten() < cur_shanten:
                        effect_count += 1
                    pop_tehai.pop()

                # 有効牌が一番多い牌を選択
                if effect_count > effect_max:
                    effect_max = effect_count
                    select_index = i

        # 待ち牌が2枚以上残っていたらリーチ
        if self.tehai.shanten() <= 0 and effect_max >= 2:
            print("リーチ")
            self.richi = True

        return select_index

    def agari_tumo(self):
        return True

    def agari_ron(self, player):
        return True
