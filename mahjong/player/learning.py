import copy
from .. import core

# イーソー君
class Isokun(core.Player):
    # 選択
    def select(self):
        return 13

    # 立直
    def call_richi(self):
        return True

    # ツモ和了
    def agari_tsumo(self):
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

# 手なりAI
class Tenari(core.Player):
    # 選択
    def select(self):
        def shanten_ex():
            return min(self.tehai.shanten_normal(), self.tehai.shanten_chitoi() * 1.5, self.tehai.shanten_kokushi())

        select_index = -1
        effect_max = 0
        cur_shanten = shanten_ex()

        # 残っている牌
        remain_hai = self.game.mjhai_set[:]

        # 自身の手牌
        for hai in self.tehai.hais:
            remain_hai.remove(hai)

        for player in self.game.players:
            # 副露
            for cur_furo in player.tehai.furos:
                for hai in cur_furo:
                    remain_hai.remove(hai)

            # 河
            for hai in player.kawa.hais:
                if not hai.furo:
                    remain_hai.remove(hai)

        # ドラ
        for dora in self.game.yama.doras:
            remain_hai.remove(dora)

        for i in range(len(self.tehai)):
            # 1枚ずつ切ってみる
            pop_hai = self.tehai.pop(i)

            # シャンテン数が進むなら
            if shanten_ex() <= cur_shanten:
                effect_count = 0

                # 残り全ての牌をツモってみる
                for hai in remain_hai:
                    # 有効牌の数をカウント
                    self.tehai.append(hai)
                    if shanten_ex() < cur_shanten:
                        effect_count += 1
                    self.tehai.pop()

                # 有効牌が一番多い牌を選択
                if effect_count >= effect_max:
                    effect_max = effect_count
                    select_index = i

            self.tehai.insert(i, pop_hai)

        return select_index

    # 立直
    def call_richi(self):
        return True

    # ツモ和了
    def agari_tsumo(self):
        return True

    # ロン和了
    def agari_ron(self, player):
        return True

    # 暗槓
    def ankan(self, hai_kind):
        # シャンテン数が下がらないなら明槓
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.furo.append([temp_tehai.pop_kind(hai_kind) for i in range(4)])

        return temp_tehai.shanten() <= self.tehai.shanten()

    # 明槓
    def minkan(self, player):
        # 門前だったら明槓しない
        if self.tehai.menzen:
            return False

        check_hai = player.kawa.hais[-1]
        temp_tehai = copy.deepcopy(self.tehai)

        # シャンテン数が下がらないなら明槓
        append_mentsu = []
        append_mentsu.append(check_hai)
        for i in range(3):
            append_mentsu.append(temp_tehai.pop_kind(check_hai.kind))
        temp_tehai.furo.append(append_mentsu)

        return temp_tehai.shanten() <= self.tehai.shanten()

    # 加槓
    def kakan(self):
        return True

    # ポン
    def pon(self, player):
        check_hai = player.kawa.hais[-1]
        temp_tehai = copy.deepcopy(self.tehai)

        # シャンテン数が進むならポン
        append_mentsu = []
        append_mentsu.append(check_hai)
        for i in range(2):
            append_mentsu.append(temp_tehai.pop_kind(check_hai.kind))
        temp_tehai.furo.append(append_mentsu)

        return temp_tehai.shanten() < self.tehai.shanten()

    # チー
    def chi(self, player):
        return True
