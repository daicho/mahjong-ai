import copy
import itertools
from abc import ABCMeta, abstractmethod
from .elements import *
from .tehai import Tehai

# プレイヤー
class Player(metaclass=ABCMeta):
    def __init__(self, name=""):
        self.name = name
        self.tehai = Tehai()
        self.kawa = Kawa()
        self.richi = False

        self.game = None
        self.chicha = None
        self.point = None

    def setup(self, game, chicha, point):
        self.game = game
        self.chicha = chicha
        self.point = point

    # 自風
    def jikaze(self):
        return (self.chicha - self.game.kyoku) % self.game.players_num

    # 下家・対面・上家
    def relative(self, other):
        return (other.chicha - self.chicha) % 4

    # 手牌・河をリセット
    def reset(self):
        self.tehai = Tehai()
        self.kawa = Kawa()
        self.richi = False

    # 配牌
    def haipai(self):
        self.tehai.append(*(self.game.yama.pop() for i in range(13)))
        self.tehai.sort()

    # 自摸
    def tsumo(self):
        pop_hai = self.game.yama.pop()
        self.tehai.tsumo(pop_hai)

    # 打牌
    def dahai(self):
        # 立直をしていたらツモ切り
        index = -1 if self.richi else self.select()
        pop_hai = self.tehai.pop(index)

        # 立直
        if not self.richi and self.tehai.shanten() == 0 and self.tehai.menzen:
            self.richi = self.do_richi()

        tsumogiri = (index == len(self.tehai.hais) or index == -1)
        self.kawa.append(pop_hai, tsumogiri, self.richi)
        self.tehai.sort()

        return pop_hai

    # ロン
    def ron(self, target, whose):
        target.set_houju()
        self.tehai.tsumo(target)

    # 暗槓
    def ankan(self, hais):
        self.tehai.ankan(hais)

    # 加槓
    def kakan(self, hai):
        self.tehai.kakan(hai)

    # 明槓
    def minkan(self, hais, target, whose):
        target.furo = True
        self.tehai.minkan(hais, target, self.relative(whose))

    # 役
    def yaku(self, tsumo):
        # 和了時の面子の組み合わせを探索
        def combi_agari():
            return_combi = []

            # 全ての雀頭候補を取り出す
            for kind, count in self.tehai.table.items():
                if count >= 2:
                    self.tehai.table[kind] -= 2

                    # 0...順子 1...暗刻
                    mentsu_combi = itertools.product([0, 1], repeat=4 - len(self.tehai.furos))

                    # 左から順番に面子を取り出し
                    for cur_combi in mentsu_combi:
                        temp_combi = self.tehai.furos + [Element([self.tehai.find(kind), self.tehai.find(kind)], EK.JANTOU)]
                        temp_table = copy.deepcopy(self.tehai.table)

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
                                    temp_combi.append(Element([self.tehai.find((i, j)), self.tehai.find((i, j + 1)), self.tehai.find((i, j + 2))], EK.SHUNTSU))
                                    for k in range(3):
                                        temp_table[(i, j + k)] -= 1
                                else:
                                    break
                            else:
                                # 暗刻
                                if temp_table[(i, j)] >= 3:
                                    temp_combi.append(Element([self.tehai.find((i, j)), self.tehai.find((i, j)), self.tehai.find((i, j))], EK.ANKO))
                                    temp_table[(i, j)] -= 3
                                else:
                                    break
                        else:
                            return_combi.append(temp_combi)

                    self.tehai.table[kind] += 2

            return return_combi

        if self.tehai.shanten() > -1:
            return

        # 国士無双
        if self.tehai.shanten_kokushi() == -1:
            yield [Yaku.KOKUSHI]
            return

        # 組み合わせに関係なく共通の役
        yaku_common = []
        yakuman_common = []

        # 副露含め全てのテーブル
        all_table = copy.deepcopy(self.tehai.table)
        for furo in self.tehai.furos:
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
                if self.tehai.table[(i, j)] < (3 if j == 1 or j == 9 else 1):
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
            if tsumo and self.tehai.menzen:
                yaku_common.append(Yaku.TSUMO)

            # 立直
            if self.richi:
                yaku_common.append(Yaku.RICHI)

            # ドラ・裏ドラ・赤ドラ
            for hai in self.tehai.hais + [self.tehai.tsumo_hai] + [hai for furo in self.tehai.furos for hai in furo.hais]:
                if hai is not None:
                    for dora in self.game.doras:
                        if hai.kind == dora[0]:
                            yaku_common.append(Yaku.DORA)

                        if self.richi and hai.kind == dora[1]:
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
            if self.tehai.shanten_chitoi() == -1:
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

                if self.tehai.menzen:
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
                    if element.is_kotsu() and element.hais[0].kind[0] == self.game.bakaze + 3:
                        yaku_list.append(Yaku.YAKUHAI)

                # 自風の役牌
                for element in cur_combi:
                    if element.is_kotsu() and element.hais[0].kind[0] == self.jikaze() + 3:
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

    # ポン
    def pon(self, hais, target, whose):
        target.furo = True
        self.tehai.pon(hais, target, self.relative(whose))

    # チー
    def chi(self, hais, target, whose):
        target.furo = True
        self.tehai.chi(hais, target, self.relative(whose))

    # ツモチェック
    def check_tsumo(self):
        for cur_yaku in self.yaku(True):
            return self.do_tsumo()

    # ロンチェック
    def check_ron(self, target, whose):
        self.tehai.tsumo(target)
        for cur_yaku in self.yaku(False):
            self.tehai.pop()
            return self.do_ron(target, whose)

        self.tehai.pop()

    # 暗槓チェック
    def check_ankan(self):
        for cur_hais in self.tehai.ankan_able():
            if self.do_ankan(cur_hais):
                return cur_hais

    # 加槓チェック
    def check_kakan(self):
        for cur_hai in self.tehai.kakan_able():
            if self.do_kakan(cur_hai):
                return cur_hai

    # 明槓チェック
    def check_minkan(self, target, whose):
        if not self.richi:
            for cur_hais in self.tehai.minkan_able(target):
                if self.do_minkan(cur_hais, target, whose):
                    return cur_hais

    # ポンチェック
    def check_pon(self, target, whose):
        if not self.richi:
            for cur_hais in self.tehai.pon_able(target):
                if self.do_pon(cur_hais, target, whose):
                    return cur_hais

    # チーチェック
    def check_chi(self, target, whose):
        if not self.richi and self.relative(whose) == 3:
            for cur_hais in self.tehai.chi_able(target):
                if self.do_chi(cur_hais, target, whose):
                    return cur_hais

    # 選択
    @abstractmethod
    def select(self):
        pass

    # ツモ和了するか
    @abstractmethod
    def do_tsumo(self):
        pass

    # ロン和了するか
    @abstractmethod
    def do_ron(self, target, whose):
        pass

    # 立直するか
    @abstractmethod
    def do_richi(self):
        pass

    # 暗槓するか
    @abstractmethod
    def do_ankan(self, target):
        pass

    # 明槓するか
    @abstractmethod
    def do_minkan(self, hais, target, whose):
        pass

    # 加槓するか
    @abstractmethod
    def do_kakan(self, target):
        pass

    # ポンするか
    @abstractmethod
    def do_pon(self, hais, target, whose):
        pass

    # チーするか
    @abstractmethod
    def do_chi(self, hais, target, whose):
        pass
