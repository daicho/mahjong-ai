import copy
import itertools

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
    def __init__(self, elememt, kind, children):
        self.element = elememt
        self.kind = kind
        self.children = children

# 面子・面子候補の組み合わせを探索
def combi(table, count, atama):
    tree = []
    shanten_min = 8

    if not atama:
        # 雀頭
        for hai_kind in range(1, 10):
            if table[hai_kind] >= 2:
                table_pop = copy.deepcopy(table)
                table_pop[hai_kind] -= 2

                for pop_kind in range(1, 10):
                    if pop_kind >= hai_kind:
                        break
                    table_pop[pop_kind] = 0

                tree.append(Node(
                    [hai_kind, hai_kind],
                    0,
                    combi(table_pop, count, True)
                ))

    if count < 4:
        # 順子
        for i in range(1, 8):
                if table[i] and table[i] and table[i + 2]:
                    table_pop = copy.deepcopy(table)
                    table_pop[i] -= 1
                    table_pop[i + 1] -= 1
                    table_pop[i + 2] -= 1

                    for pop_kind in range(1, 10):
                        if pop_kind >= i:
                            break
                        table_pop[pop_kind] = 0

                    tree.append(Node(
                        [i, i + 1, i + 2],
                        1,
                        combi(table_pop, count + 1, atama)
                    ))

        # 暗刻
        for hai_kind in range(1, 10):
            if table[hai_kind] >= 3:
                table_pop = copy.deepcopy(table)
                table_pop[hai_kind] -= 3

                for pop_kind in range(1, 10):
                    if pop_kind >= hai_kind:
                        break
                    table_pop[pop_kind] = 0

                tree.append(Node(
                    [hai_kind, hai_kind, hai_kind],
                    2,
                    combi(table_pop, count + 1, atama)
                ))

        # 両面塔子
        for i in range(2, 8):
            if table[i] and table[i + 1]:
                table_pop = copy.deepcopy(table)
                table_pop[i] -= 1
                table_pop[i + 1] -= 1

                for pop_kind in range(1, 10):
                    if pop_kind >= i:
                        break

                    table_pop[pop_kind] = 0

                tree.append(Node(
                    [i, i + 1],
                    3,
                    combi(table_pop, count + 1, atama)
                ))

        # 辺張塔子
        for i in [1, 8]:
            if table[i] and table[i + 1]:
                table_pop = copy.deepcopy(table)
                table_pop[i] -= 1
                table_pop[i + 1] -= 1

                for pop_kind in range(1, 10):
                    if pop_kind >= i:
                        break

                    table_pop[pop_kind] = 0

                tree.append(Node(
                    [i, i + 1],
                    4,
                    combi(table_pop, count + 1, atama)
                ))

        # 嵌張塔子
        for i in range(1, 8):
            if table[i] and table[i + 2]:
                table_pop = copy.deepcopy(table)
                table_pop[i] -= 1
                table_pop[i + 2] -= 1

                for pop_kind in range(1, 10):
                    if pop_kind >= i:
                        break

                    table_pop[pop_kind] = 0

                tree.append(Node(
                    [i, i + 2],
                    5,
                    combi(table_pop, count + 1, atama)
                ))

        # 対子
        for hai_kind in range(1, 10):
            if table[hai_kind] >= 2:
                table_pop = copy.deepcopy(table)
                table_pop[hai_kind] -= 2

                for pop_kind in range(1, 10):
                    if pop_kind >= hai_kind:
                        break
                    table_pop[pop_kind] = 0

                tree.append(Node(
                    [hai_kind, hai_kind],
                    6,
                    combi(table_pop, count + 1, atama)
                ))

    return tree

# 各ノードの最小シャンテン数を探索
def shanten_min(tree, s_re):
    s_table = (1, 2, 2, 1, 1, 1, 1)
    s_min = s_re

    for leaf in tree:
        s_min = min(s_min, s_re - s_table[leaf.kind], shanten_min(leaf.children, s_re))
    return s_min

suhai = []
for i in range(1, 10):
    suhai.extend([i for j in range(4)])

combi_rt = []
for i in range(1, 6):
    combi_rt.extend(dict.fromkeys(itertools.combinations(suhai, i)))

combi_table = []
for cur in combi_rt:
    cur_table = {}
    for i in range(1, 10):
        cur_table[i] = 0

    for num in cur:
        cur_table[num] += 1    

    combi_table.append(cur_table)

for cur in combi_table:
    print(shanten_min(combi(cur, 0, False), 8))
