from abc import ABCMeta, abstractmethod
#from .core import *
#from .tehai import *
#from .game import *

print(__package__)

# プレイヤー
class Player(metaclass=ABCMeta):
    def __init__(self, name=""):
        self.name = name
        self.tehai = Tehai()
        self.kawa = Kawa()

        self.point = 35000
        self.richi = False

    def setup(self, game, chicha, point):
        self.game = game
        self.chicha = chicha
        self.point = point

    # 自風
    def jikaze(self):
        return (self.chicha - self.game.kyoku) % self.game.players_num

    # 他家との位置関係
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
        # リーチをしていたらツモ切り
        index = -1 if self.richi else self.select()
        pop_hai = self.tehai.pop(index)

        # 立直
        if not self.richi and self.tehai.shanten() == 0 and self.tehai.menzen:
            self.richi = self.do_richi()

        tsumogiri = (index == len(self.tehai.hais) or index == -1)
        self.kawa.append(pop_hai, tsumogiri, self.richi)
        self.tehai.sort()

        return pop_hai

    # ツモチェック
    def check_tsumo(self):
        if self.tehai.shanten() == -1 and self.do_tsumo():
            return True
        else:
            return False

    # ロンチェック
    def check_ron(self, target, whose):
        self.tehai.tsumo(target)

        if self.tehai.shanten() == -1 and self.do_ron(target, whose):
            target.set_houju()
            return True
        else:
            self.tehai.pop()
            return False

    # 暗槓チェック
    def check_ankan(self):
        for cur_hais in self.tehai.ankan_able():
            if self.do_ankan(cur_hais):
                self.tehai.ankan(cur_hais)
                self.game.yama.add_dora()
                return True

        return False

    # 加槓チェック
    def check_kakan(self):
        for cur_hai in self.tehai.kakan_able():
            if self.do_kakan(cur_hai):
                self.tehai.kakan(cur_hai)
                self.game.yama.add_dora()
                return True

        return False

    # 明槓チェック
    def check_minkan(self, target, whose):
        if not self.richi:
            for cur_hais in self.tehai.minkan_able(target):
                if self.do_minkan(cur_hais, target, whose):
                    target.furo = True
                    self.tehai.minkan(cur_hais, target, self.relative(whose))
                    self.game.yama.add_dora()
                    return True

        return False

    # ポンチェック
    def check_pon(self, target, whose):
        if not self.richi:
            for cur_hais in self.tehai.pon_able(target):
                if self.do_pon(cur_hais, target, whose):
                    target.furo = True
                    self.tehai.pon(cur_hais, target, self.relative(whose))
                    return True

        return False

    # チーチェック
    def check_chi(self, target, whose):
        if not self.richi and self.relative(whose) == 3:
            for cur_hais in self.tehai.chi_able(target):
                if self.do_chi(cur_hais, target, whose):
                    target.furo = True
                    self.tehai.chi(cur_hais, target, self.relative(whose))
                    return True

        return False

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
