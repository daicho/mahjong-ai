import copy
import itertools
import collections

"""
kind:
  0...雀頭
  1...順子
  2...暗刻
  3...両面塔子
  4...辺張塔子
  5...嵌張塔子
  6...対子
"""

# 面子・面子候補探索用のノード
class Node():
    def __init__(self, elememt, kind, shanten, count, parent, children):
        self.element = elememt
        self.kind = kind
        self.shanten = shanten
        self.count = count
        self.score = (self.shanten, self.count)
        self.parent = parent
        self.children = children

# 面子・面子候補の組み合わせを探索
def combi(table, shanten, count, atama):
    # テーブルを切り取り
    def cut(table, until):
        cut_table = copy.deepcopy(table)

        for pop_kind in range(1, 10):
            if pop_kind >= until:
                break
            cut_table[pop_kind] = 0

        return cut_table

    tree = []
    shanten_min = 8

    if not atama:
        # 雀頭
        for hai_kind in range(1, 10):
            if table[hai_kind] >= 2:
                table_pop = cut(table, hai_kind)
                table_pop[hai_kind] -= 2

                tree.append(Node(
                    (hai_kind, hai_kind), 0, shanten - 1, count, tree,
                    combi(table_pop, shanten - 1, count, True)
                ))

    if count < 4:
        # 順子
        for i in range(1, 8):
            if table[i] and table[i + 1] and table[i + 2]:
                table_pop = cut(table, i)
                table_pop[i] -= 1
                table_pop[i + 1] -= 1
                table_pop[i + 2] -= 1

                tree.append(Node(
                    (i, i + 1, i + 2), 1, shanten - 2, count + 1, tree,
                    combi(table_pop, shanten - 2, count + 1, atama)
                ))

        # 暗刻
        for hai_kind in range(1, 10):
            if table[hai_kind] >= 3:
                table_pop = cut(table, hai_kind)
                table_pop[hai_kind] -= 3

                tree.append(Node(
                    (hai_kind, hai_kind, hai_kind), 2, shanten - 2, count + 1, tree,
                    combi(table_pop, shanten - 2, count + 1, atama)
                ))

        # 両面塔子
        for i in range(3):
            for j in range(2, 8):
                if table[i] and table[i + 1]:
                    table_pop = cut(table, i)
                    table_pop[i] -= 1
                    table_pop[i + 1] -= 1

                    tree.append(Node(
                        (i, i + 1), 3, shanten - 1, count + 1, tree,
                        combi(table_pop, shanten - 1, count + 1, atama)
                    ))

        # 辺張塔子
        for i in [1, 8]:
            if table[i] and table[i + 1]:
                table_pop = cut(table, i)
                table_pop[i] -= 1
                table_pop[i + 1] -= 1

                tree.append(Node(
                    (i, i + 1), 4, shanten - 1, count + 1, tree,
                    combi(table_pop, shanten - 1, count + 1, atama)
                ))

        # 嵌張塔子
        for i in range(1, 8):
            if table[i] and table[i + 2]:
                table_pop = cut(table, i)
                table_pop[i] -= 1
                table_pop[i + 2] -= 1

                tree.append(Node(
                    (i, i + 2), 5, shanten - 1, count + 1, tree,
                    combi(table_pop, shanten - 1, count + 1, atama)
                ))

        # 対子
        for hai_kind in range(1, 10):
            if table[hai_kind] >= 2:
                table_pop = cut(table, hai_kind)
                table_pop[hai_kind] -= 2

                tree.append(Node(
                    (hai_kind, hai_kind), 6, shanten - 1, count + 1, tree,
                    combi(table_pop, shanten - 1, count + 1, atama)
                ))

    return tree

# シャンテン数と使用面子数が最小となる組み合わせを探索
def combi_min(tree):
    node_min = Node((), -1, 8, 4, None, None)

    for leaf in tree:
        if leaf.score < node_min.score:
            node_min = leaf

        child_min = combi_min(leaf.children)
        if child_min.score < node_min.score:
            node_min = child_min

    return node_min

suhai = []
for i in range(1, 10):
    suhai.extend([i for j in range(4)])

combi_rt = []
for i in range(1, 6):
    combi_rt.extend(dict.fromkeys(itertools.combinations(suhai, i)))

combi_table = []
for cur in combi_rt:
    combi_table.append(collections.Counter(cur))

for cur in combi_table:
    pass
    cur_min = combi_min(combi(cur, 8, 0, False))
    print(cur_min.element)
    print(cur_min.shanten, cur_min.count)
