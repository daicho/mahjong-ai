import random
from .elements import MjHai, Yama, yaku_name
from .. import graphic as gp

# ゲーム
class Game():
    kaze_name = ["東", "南", "西", "北"]

    def __init__(self, mjhai_set, yaku, players, point):
        self.mjhai_set = mjhai_set
        self.yaku = yaku

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
        self.doras.append((self.dora_kind(new_dora[0].kind), self.dora_kind(new_dora[1].kind)))

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

    # 加槓
    def kakan(self, hai):
        self.cur_player.kakan(hai)
        self.add_dora()

    # 明槓
    def minkan(self, hais, target, player):
        player.minkan(hais, target, self.cur_player)
        self.change_player(player.chicha)
        self.add_dora()

    # ポン
    def pon(self, hais, target, player):
        player.pon(hais, target, self.cur_player)
        self.change_player(player.chicha)

    # チー
    def chi(self, hais, target, player):
        player.chi(hais, target, self.cur_player)
        self.change_player(player.chicha)

    # 役
    def yaku(self, player, tsumo):
        # 和了時の面子の組み合わせを探索
        def combi_agari():
            # 全ての雀頭候補を取り出す
            for kind, count in player.tehai.table.items():
                if count >= 2:
                    player.tehai.table[kind] -= 2

                    # 0...順子 1...暗刻
                    mentsu_combi = itertools.product([0, 1], repeat=4 - len(player.tehai.furos))

                    # 左から順番に面子を取り出し
                    for cur_combi in mentsu_combi:
                        return_combi = player.tehai.furos + [Element([player.tehai.find(kind), player.tehai.find(kind)], EK.JANTOU)]
                        temp_table = copy.deepcopy(player.tehai.table)

                        for mentsu_kind in cur_combi:
                            # 開始点
                            for i in range(10):
                                for j in range(10):
                                    if temp_table[(i, j)]:
                                        break
                                else:
                                    continue
                                break

                            if mentsu_kind == 0:
                                # 順子
                                if temp_table[(i, j)] and temp_table[(i, j + 1)] and temp_table[(i, j + 2)]:
                                    return_combi.append(Element([player.tehai.find((i, j)), player.tehai.find((i, j + 1)), player.tehai.find((i, j + 2))], EK.SHUNTSU))
                                    for k in range(3):
                                        temp_table[(i, j + k)] -= 1
                                else:
                                    break
                            else:
                                # 暗刻
                                if temp_table[(i, j)] >= 3:
                                    return_combi.append(Element([player.tehai.find((i, j)), player.tehai.find((i, j)), player.tehai.find((i, j))], EK.ANKO))
                                    temp_table[(i, j)] -= 3
                                else:
                                    break
                        else:
                            yield return_combi

                    player.tehai.table[kind] += 2

        if player.tehai.shanten() > -1:
            return

        # 国士無双
        if player.tehai.shanten_kokushi() == -1:
            yield [Yaku.KOKUSHI]
            return

        # 組み合わせに関係なく共通の役
        yaku_common = []
        yakuman_common = []

        # 副露含め全てのテーブル
        all_table = copy.deepcopy(player.tehai.table)
        for furo in player.tehai.furos:
            all_table += furo.table

        # 役満から先に調べる
        # 字一色
        for kind, count in all_table.items():
            if count > 0 and kind[1]:
                break
        else:
            yakuman_common.append(Yaku.TSUISO)

        # 緑一色
        for kind, count in all_table.items():
            if count > 0 and not kind in [(1, 2), (1, 3), (1, 4), (1, 6), (1, 8), (8, 0)]:
                break
        else:
            yakuman_common.append(Yaku.RYUISO)

        # 九蓮宝燈
        for i in range(3):
            for j in range(1, 10):
                if player.tehai.table[(i, j)] < (3 if j == 1 or j == 9 else 1):
                    break
            else:
                yakuman_common.append(Yaku.CHUREN)
                break

        # 清老頭
        for kind, count in all_table.items():
            if count > 0 and kind[1] != 1 and kind[1] != 9:
                break
        else:
            yakuman_common.append(Yaku.CHINRO)

        if len(yakuman_common) == 0:
            # ツモ
            if tsumo and player.tehai.menzen:
                yaku_common.append(Yaku.TSUMO)

            # 立直
            if player.richi:
                yaku_common.append(Yaku.RICHI)

            # ドラ・裏ドラ・赤ドラ
            for hai in player.tehai.hais + [player.tehai.tsumo_hai] + [hai for furo in player.tehai.furos for hai in furo.hais]:
                if hai is not None:
                    for dora in self.doras:
                        if hai.kind == dora[0]:
                            yaku_common.append(Yaku.DORA)

                        if player.richi and hai.kind == dora[1]:
                                yaku_common.append(Yaku.URADORA)

                    if hai.dora:
                        yaku_common.append(Yaku.AKADORA)

            # タンヤオ
            for kind, count in all_table.items():
                if count > 0 and not 2 <= kind[1] <= 8:
                    break
            else:
                yaku_common.append(Yaku.TANYAO)

            # 混一色・清一色
            append_yaku = Yaku.CHINITSU
            for i in range(3):
                for kind, count in all_table.items():
                    if count > 0 and kind[0] != i:
                        if kind[1] == 0:
                            append_yaku = Yaku.HONITSU
                        else:
                            break
                else:
                    yaku_common.append(append_yaku)
                    break

            # 混老頭
            for kind, count in all_table.items():
                if count > 0 and 2 <= kind[1] <= 8:
                        honro = False
                        break
            else:
                honro = True
                yaku_common.append(Yaku.HONRO)

            # 七対子
            if player.tehai.shanten_chitoi() == -1:
                yield yaku_common + [Yaku.CHITOI]

        # 全ての組み合わせでの役
        for cur_combi in combi_agari():
            yaku_list = yakuman_common[:]

            # 四暗刻
            if sum(1 for element in cur_combi if element.kind == EK.ANKO or element.kind == EK.ANKAN) == 4:
                yaku_list.append(Yaku.SUANKO)

            # 大四喜・小四喜
            append_yaku = Yaku.DAISUSHI
            for i in range(3, 7):
                for element in cur_combi:
                    if element.kind == EK.JANTOU and element.hais[0].kind[0] == i:
                        append_yaku = Yaku.SHOUSUSHI
                        break

                    elif element.is_kotsu() and element.hais[0].kind[0] == i:
                        break
                else:
                    break
            else:
                yaku_list.append(append_yaku)

            # 大三元
            for i in range(7, 10):
                for element in cur_combi:
                    if element.is_kotsu() and element.hais[0].kind[0] == i:
                        break
                else:
                    break
            else:
                yaku_list.append(Yaku.DAISANGEN)

            if len(yaku_list) == 0:
                yaku_list = yaku_common[:]

                if player.tehai.menzen:
                    # 平和
                    if sum(1 for element in cur_combi if element.kind == EK.SHUNTSU) == 4:
                        yaku_list.append(Yaku.PINFU)

                    # 一盃口・二盃口
                    peko_num = 0

                    for peko_combi in itertools.combinations(cur_combi, 2):
                        if peko_combi[0].eq_kind(peko_combi[1]):
                            peko_num += 1

                    if peko_num == 1:
                        yaku_list.append(Yaku.IPEKO)
                    elif peko_num == 2:
                        yaku_list.append(Yaku.RYANPEKO)

                # 一気通貫
                for i in range(3):
                    for j in range(3):
                        for element in cur_combi:
                            if element.is_shuntsu() and sum(element.table[(i, j * 3 + k)] for k in range(1, 4)) == 3:
                                break
                        else:
                            break
                    else:
                        yaku_list.append(Yaku.ITTSU)
                        break

                # 三色同順
                for i in range(1, 8):
                    for j in range(3):
                        for element in cur_combi:
                            if element.is_shuntsu() and sum(element.table[(j, i + k)] for k in range(3)) == 3:
                                break
                        else:
                            break
                    else:
                        yaku_list.append(Yaku.DOUJUN)
                        break

                # 三色同刻
                for i in range(1, 10):
                    for j in range(3):
                        for element in cur_combi:
                            if element.is_kotsu() and element.table[(j, i)] >= 3:
                                break
                        else:
                            break
                    else:
                        yaku_list.append(Yaku.DOUKO)
                        break

                # 場風の役牌
                for element in cur_combi:
                    if element.is_kotsu() and element.hais[0].kind[0] == player.bakaze + 3:
                        yaku_list.append(Yaku.YAKUHAI)

                # 自風の役牌
                for element in cur_combi:
                    if element.is_kotsu() and element.hais[0].kind[0] == player.jikaze() + 3:
                        yaku_list.append(Yaku.YAKUHAI)

                # 三元牌
                for element in cur_combi:
                    if element.is_kotsu() and 7 <= element.hais[0].kind[0] <= 9:
                        yaku_list.append(Yaku.YAKUHAI)

                # 三暗刻
                if sum(1 for element in cur_combi if element.kind == EK.ANKO or element.kind == EK.ANKAN) == 3:
                    yaku_list.append(Yaku.SANANKO)

                # 対々和
                if sum(1 for element in cur_combi if element.is_kotsu()) == 4:
                    yaku_list.append(Yaku.TOITOI)

                # チャンタ・純チャン
                if not honro:
                    append_yaku = Yaku.JUNCHAN
                    for element in cur_combi:
                        for hai in element.hais:
                            if hai.kind[1] == 1 or hai.kind[1] == 9:
                                break

                            elif hai.kind[1] == 0:
                                append_yaku = Yaku.CHANTA
                                break
                        else:
                            break
                    else:
                        yaku_list.append(append_yaku)

            yield yaku_list

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
        self.doras = []
        self.uradoras = []

        for player in self.players:
            player.reset()

    # 局開始
    def start_kyoku(self):
        print(self.kyoku_name())
        print()

        self.haipai() # 配牌
        self.add_dora()

        while self.yama.remain > 0:
            # ツモ
            if len(self.cur_player.tehai) % 3 <= 1:
                self.tsumo()

            # ツモ判定
            if self.cur_player.check_tsumo():
                print("{}：ツモ".format(self.cur_player.name))
                for cur_yaku_list in self.cur_player.tehai.yaku(True, self.cur_player.richi, self.bakaze, self.cur_player.jikaze() ,self.doras):
                    for cur_yaku in cur_yaku_list:
                        print(self.yaku[cur_yaku][not self.cur_player.tehai.menzen], yaku_name[cur_yaku])

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
            print("{} [残り{}]".format(self.cur_player.name, self.yama.remain))
            self.cur_player.tehai.show()

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

                        print("{}→{}：ロン".format(self.cur_player.name, check_player.name))
                        for cur_yaku_list in check_player.tehai.yaku(False, check_player.richi, self.bakaze, check_player.jikaze(), self.doras):
                            for cur_yaku in cur_yaku_list:
                                print(self.yaku[cur_yaku][not check_player.tehai.menzen], yaku_name[cur_yaku])

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

            print()
            self.next_player()

        print("流局")

        for player in self.players:
            print("{}：{}".format(player.name, "テンパイ" if player.tehai.shanten() <= 0 else "ノーテン"))

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

    def __init__(self, mjhai_set, yaku, players, point, view=None, open=False):
        self.screen = gp.Screen(self, view, open)
        super().__init__(mjhai_set, yaku, players, point)

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
