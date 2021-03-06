import copy
from .. import player

# 手なりAI
class Tenari(player.Player):
    # チートイの重みを軽くしたシャンテン数
    def shanten_ex(self):
        return min(self.tehai.shanten_normal(), self.tehai.shanten_chitoi() * 1.5, self.tehai.shanten_kokushi())

    # 選択
    def select(self):
        select_index = -1
        effect_max = 0
        cur_shanten = self.shanten_ex()

        # 残っている牌
        remain_hai = self.game.mjhai_set[:]

        # 自身の手牌
        for hai in self.tehai.hais:
            remain_hai.remove(hai)

        for player in self.game.players:
            # 副露
            for furo in player.tehai.furos:
                for hai in furo.hais:
                    remain_hai.remove(hai)

            # 河
            for kawa_hai in player.kawa.hais:
                if not kawa_hai.furo:
                    remain_hai.remove(kawa_hai.hai)

        # ドラ
        for dora in self.game.yama.doras:
            remain_hai.remove(dora)

        # 裏ドラ
        for uradora in self.game.yama.uradoras:
            remain_hai.remove(uradora)

        for i in range(len(self.tehai)):
            # 1枚ずつ切ってみる
            pop_hai = self.tehai.pop(i)

            # シャンテン数が進むなら
            if self.shanten_ex() <= cur_shanten:
                effect_count = 0

                # 残り全ての牌をツモってみる
                for hai in remain_hai:
                    # 有効牌の数をカウント
                    self.tehai.append(hai)
                    if self.shanten_ex() < cur_shanten:
                        effect_count += 1
                    self.tehai.pop()

                # 有効牌が一番多い牌を選択
                if effect_count >= effect_max:
                    effect_max = effect_count
                    select_index = i

            self.tehai.insert(i, pop_hai)

        return select_index

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
        # シャンテン数が下がらないなら暗槓
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.ankan(target)
        return temp_tehai.shanten() <= self.tehai.shanten()

    # 明槓するか
    def do_minkan(self, hais, target, whose):
        # 門前だったら明槓しない
        if self.tehai.menzen:
            return False

        # シャンテン数が下がらないなら明槓
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.minkan(hais, target, self.relative(whose))
        return temp_tehai.shanten() <= self.tehai.shanten()

    # 加槓するか
    def do_kakan(self, target):
        # シャンテン数が下がらないなら加槓
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.kakan(target)
        return temp_tehai.shanten() <= self.tehai.shanten()

    # ポンするか
    def do_pon(self, hais, target, whose):
        # シャンテン数が進むならポン
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.pon(hais, target, self.relative(whose))
        return temp_tehai.shanten() < self.tehai.shanten()

    # チーするか
    def do_chi(self, hais, target, whose):
        # シャンテン数が進むならチー
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.chi(hais, target, self.relative(whose))
        return temp_tehai.shanten() < self.tehai.shanten()

# 面子手のみ
class Menzen(Tenari):
    def shanten_ex(self):
        return self.tehai.shanten_normal()

    def do_tsumo(self):
        return True

    def do_ron(self, target, whose):
        return True

    def do_richi(self):
        return False

    def do_ankan(self, target):
        return False

    def do_minkan(self, hais, target, whose):
        return False

    def do_kakan(self, target):
        return False

    def do_pon(self, hais, target, whose):
        return False

    def do_chi(self, hais, target, whose):
        return False

# 土田 (チートイだけ)
class Tsuchida(Tenari):
    # シャンテン数
    def shanten_ex(self):
        return self.tehai.shanten_chitoi()

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

# れんたろう (国士だけ)
class Rentaro(Tenari):
    # シャンテン数
    def shanten_ex(self):
        return self.tehai.shanten_kokushi()

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

# やがさき (鳴きまくる)
class Yagasaki(Tenari):
    # シャンテン数
    def shanten_ex(self):
        return self.tehai.shanten_normal()

    # 立直するか
    def do_richi(self):
        return False

    # 暗槓するか
    def do_ankan(self, target):
        return True

    # 明槓するか
    def do_minkan(self, hais, target, whose):
        return True

    # 加槓するか
    def do_kakan(self, target):
        return True

    # ポンするか
    def do_pon(self, hais, target, whose):
        return True

    # チーするか
    def do_chi(self, hais, target, whose):
        return True
