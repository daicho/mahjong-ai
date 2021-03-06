import random
from .core import *
from .. import graphic as gp

# ゲーム
class Game():
    kaze_name = ["東", "南", "西", "北"]

    def __init__(self, mjhai_set, yakus, players, point):
        self.mjhai_set = mjhai_set
        self.yakus = yakus

        self.players_num = len(players)
        self.players = random.sample(players, self.players_num)

        for i, player in enumerate(self.players):
            player.setup(self, i, point)

        self.bakaze = 0  # 場風
        self.kyoku = 0   # 局
        self.honba = 0   # 本場
        self.kyotaku = 0 # 供託

        # 番
        self.turn = self.kyoku
        self.cur_player = self.players[self.turn]

        # 牌山
        self.yama = Yama(self.mjhai_set)
        self.doras = [self.dora_kind(self.yama.doras[0].kind)]
        self.uradoras = [self.dora_kind(self.yama.uradoras[0].kind)]

    # 局を表す文字列
    def kyoku_name(self):
        return "{}{}局".format(Game.kaze_name[self.bakaze], self.kyoku + 1)

    # ドラ表示牌に対応するドラ
    def dora_kind(self, kind):
        # 数牌
        if kind[1]:
            next_num = kind[1]
            while True:
                next_num = next_num % 9 + 1
                if MjHai((kind[0], next_num)) in self.mjhai_set or MjHai((kind[0], next_num), True) in self.mjhai_set:
                    return (kind[0], next_num)

        # 東南西北
        elif 3 <= kind[0] <= 6:
            return ((kind[0] - 3 + 1) % 4 + 3, 0)

        # 白發中
        elif 7 <= kind[0] <= 9:
            return ((kind[0] - 7 + 1) % 3 + 7, 0)

    # ドラ追加
    def add_dora(self):
        new_dora = self.yama.add_dora()
        self.doras.append(self.dora_kind(self.yama.doras[-1].kind))
        self.uradoras.append(self.dora_kind(self.yama.uradoras[-1].kind))

    # 配牌
    def haipai(self):
        for player in self.players:
            player.haipai()

    # ツモ
    def tsumo(self):
        self.cur_player.tsumo()

    # 打牌
    def dahai(self):
        return self.cur_player.dahai()

    # ロン
    def ron(self, target, player):
        player.ron(target, self.cur_player)

    # 暗槓
    def ankan(self, hais):
        self.cur_player.ankan(hais)
        self.add_dora()

        for player in self.players:
            player.ippatsu = False

    # 加槓
    def kakan(self, hai):
        self.cur_player.kakan(hai)
        self.add_dora()
        for player in self.players:
            player.ippatsu = False

    # 明槓
    def minkan(self, hais, target, player):
        player.minkan(hais, target, self.cur_player)
        self.change_player(player.chicha)
        self.add_dora()
        for player in self.players:
            player.ippatsu = False

    # ポン
    def pon(self, hais, target, player):
        player.pon(hais, target, self.cur_player)
        self.change_player(player.chicha)
        for player in self.players:
            player.ippatsu = False

    # チー
    def chi(self, hais, target, player):
        player.chi(hais, target, self.cur_player)
        self.change_player(player.chicha)
        for player in self.players:
            player.ippatsu = False

    # プレイヤーのツモ順を変更
    def change_player(self, chicha):
        self.turn = chicha
        self.cur_player = self.players[self.turn]

    # 次のプレイヤーへ
    def next_player(self):
        self.change_player((self.turn + 1) % self.players_num)

    # 次の局へ
    def next_kyoku(self, renchan, ryukyoku):
        # 局を更新
        if not renchan:
            self.kyoku += 1
            if self.kyoku >= self.players_num:
                self.kyoku = 0
                self.bakaze += 1

        # 本場
        if renchan or ryukyoku:
            self.honba += 1
        else:
            self.honba = 0

        # リセット
        self.change_player(self.kyoku)
        self.yama = Yama(self.mjhai_set)
        self.doras = [self.dora_kind(self.yama.doras[0].kind)]
        self.uradoras = [self.dora_kind(self.yama.uradoras[0].kind)]

        for player in self.players:
            player.reset()

    # 局開始
    def start_kyoku(self):
        #print(self.kyoku_name())
        #print()

        self.haipai() # 配牌

        while self.yama.remain > 0:
            # ツモ
            if len(self.cur_player.tehai) % 3 <= 1:
                self.tsumo()

            # ツモ判定
            if self.cur_player.check_tsumo():
                #print("{}：ツモ".format(self.cur_player.name))
                for cur_yaku_list in self.cur_player.yaku(True):
                    for cur_yaku in cur_yaku_list:
                        pass#print(self.yakus[cur_yaku][not self.cur_player.tehai.menzen], YAKU_NAME[cur_yaku])

                return self.cur_player.jikaze() == 0, False

            # 暗槓
            cur_hais = self.cur_player.check_ankan()
            if cur_hais is not None:
                self.ankan(cur_hais)
                continue

            # 加槓
            cur_hai = self.cur_player.check_kakan()
            if cur_hai is not None:
                self.kakan(cur_hai)
                continue

            # コンソール表示
            #print("{} [残り{}]".format(self.cur_player.name, self.yama.remain))
            #self.cur_player.tehai.show()

            # 打牌
            check_hai = self.dahai()

            end = False
            renchan = False
            furo = False

            # ロン判定
            for check_player in self.players:
                # 自身は判定しない
                if check_player != self.cur_player:
                    if check_player.check_ron(check_hai, self.cur_player):
                        self.ron(check_hai, check_player)

                        #print("{}→{}：ロン".format(self.cur_player.name, check_player.name))
                        for cur_yaku_list in check_player.yaku(False):
                            for cur_yaku in cur_yaku_list:
                                pass#print(self.yakus[cur_yaku][not check_player.tehai.menzen], YAKU_NAME[cur_yaku])

                        end = True
                        if check_player.jikaze() == 0:
                            renchan = True

            if end:
                return renchan, False

            # 副露判定
            for check_player in self.players:
                # 自身は判定しない
                if check_player != self.cur_player:
                    # 明槓
                    cur_hais = check_player.check_minkan(check_hai, self.cur_player)
                    if cur_hais is not None:
                        furo = True
                        self.minkan(cur_hais, check_hai, check_player)
                        break

                    # ポン
                    cur_hais = check_player.check_pon(check_hai, self.cur_player)
                    if cur_hais is not None:
                        furo = True
                        self.pon(cur_hais, check_hai, check_player)
                        break

                    """
                    # チー
                    cur_hais = check_player.check_chi(check_hai, self.cur_player)
                    if cur_hais is not None:
                        furo = True
                        self.chi(cur_hais, check_hai, check_player)
                        break
                    """

            if furo:
                continue

            #print()
            self.next_player()

        #print("流局")

        for player in self.players:
            pass#print("{}：{}".format(player.name, "テンパイ" if player.tehai.shanten() <= 0 else "ノーテン"))

        return self.players[self.kyoku].tehai.shanten() <= 0, True

    # ゲーム開始
    def start(self):
        while self.bakaze <= 1:
            renchan, ryukyoku = self.start_kyoku()

            if ryukyoku:
                for player in self.players:
                    if player.richi:
                        self.kyotaku += 1
            else:
                self.kyotaku = 0

            self.next_kyoku(renchan, ryukyoku)

# グラフィカルなゲーム
class GraphicalGame(Game):
    kaze_name = ["東", "南", "西", "北"]

    def __init__(self, mjhai_set, yakus, players, point, view=None, open=False):
        self.screen = gp.Screen(self, view, open)
        super().__init__(mjhai_set, yakus, players, point)

    # 配牌
    def haipai(self):
        super().haipai()
        self.screen.draw()

    # ツモ
    def tsumo(self):
        super().tsumo()
        self.screen.draw()

    # 打牌
    def dahai(self):
        hai = super().dahai()
        self.screen.draw()
        return hai

    # 暗槓
    def ankan(self, hais):
        super().ankan(hais)
        self.screen.draw()

    # 加槓
    def kakan(self, hai):
        super().kakan(hai)
        self.screen.draw()

    # 明槓
    def minkan(self, hais, target, player):
        super().minkan(hais, target, player)
        self.screen.draw()

    # ポン
    def pon(self, hais, target, player):
        super().pon(hais, target, player)
        self.screen.draw()

    # チー
    def chi(self, hais, target, player):
        super().chi(hais, target, player)
        self.screen.draw()

    # 局開始
    def start_kyoku(self):
        renchan, ryukyoku = super().start_kyoku()
        self.screen.draw_result()
        return renchan, ryukyoku

class GameReader():
    def __init__(self, mjhai_set, yakus, players, point):
        self.mjhai_set = mjhai_set
        self.yakus = yakus

        self.players_num = len(players)
        self.players = random.sample(players, self.players_num)

        for i, player in enumerate(self.players):
            player.setup(self, i, point)

        self.bakaze = 0  # 場風
        self.kyoku = 0   # 局
        self.honba = 0   # 本場
        self.kyotaku = 0 # 供託

        self.turn = self.kyoku
        self.cur_player = self.players[self.turn]
        self.yama = Yama(self.mjhai_set) # 牌山
        self.doras = []
