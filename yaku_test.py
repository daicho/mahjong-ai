import mahjong.core as mj

tehai = mj.Tehai()
tehai.append(
    mj.MjHai((1, 1)),
    mj.MjHai((1, 1)),
    mj.MjHai((1, 1)),
    mj.MjHai((0, 1)),
    mj.MjHai((0, 1)),
    mj.MjHai((0, 1)),
    mj.MjHai((2, 1)),
    mj.MjHai((2, 2)),
    mj.MjHai((2, 3)),
    mj.MjHai((2, 9)),
    mj.MjHai((2, 9)),
    mj.MjHai((2, 9)),
    mj.MjHai((1, 9)),
    mj.MjHai((1, 9)),
)

tehai.show()
print()

for cur_yaku_list in tehai.yaku():
    for cur_yaku in cur_yaku_list:
        print(mj.yaku_name[cur_yaku])
    print()
