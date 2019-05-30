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
    combi_table.append(collections.Counter(cur))

for cur in combi_table:
    pass
    print(shanten_min(combi(cur, 0, False), 8))
