import copy
from abc import ABCMeta, abstractmethod
from .elements import Kawa
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
        return self.tehai.shanten() == -1 and self.do_tsumo()

    # ロンチェック
    def check_ron(self, target, whose):
        temp_tehai = copy.deepcopy(self.tehai)
        temp_tehai.tsumo(target)
        return temp_tehai.shanten() == -1 and self.do_ron(target, whose)

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
