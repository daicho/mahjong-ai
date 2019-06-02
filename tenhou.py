import time
import random
import collections
import mahjong as mj

# 全ての牌をセット
# 筒子・索子
mjhai_set = []
for i in range(2):
    for j in range(1, 10):
        mjhai_set.extend([mj.MjHai(i, j) for k in range(4)])

# 萬子
mjhai_set.extend([mj.MjHai(2, 1) for i in range(4)])
mjhai_set.extend([mj.MjHai(2, 9) for i in range(4)])

# 字牌
for i in range(3, 10):
    mjhai_set.extend([mj.MjHai(i) for j in range(4)])

# 試行回数
number = 1000000
count = collections.Counter()

start_time = time.time() # 開始時間

for i in range(number):
    # 配牌
    tehai = mj.Tehai()
    tehai.extend(random.sample(mjhai_set, 14))

    # シャンテン数計算
    shanten = tehai.shanten()
    count[shanten] += 1

proc_time = time.time() - start_time # 処理時間

# 結果を表示
print("処理時間：{:.4f}秒 (平均：{:.7f}秒)".format(proc_time, proc_time / number))
print("試行回数：{}回".format(number))

shanten_sum = 0
for i in range(-1, 7):
    shanten_sum += i * count[i]

    print("{:>2}シャンテン：{:>6}回 ({:7.4f}% / {:7.1f}回に1回)".format(
        i,
        count[i],
        count[i] / number * 100,
        number / count[i] if count[i] else 0
    ))

print("平均：{:.4f}シャンテン".format(shanten_sum / number))
