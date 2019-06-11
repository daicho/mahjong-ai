import mahjong.core as mj

tehai = mj.Tehai()
tehai.append(
    mj.MjHai((0, 2)),
    mj.MjHai((0, 3)),
    mj.MjHai((0, 4)),
    mj.MjHai((0, 5)),
    mj.MjHai((0, 6)),
    mj.MjHai((0, 7)),
    mj.MjHai((0, 8)),
    mj.MjHai((0, 8)),
    mj.MjHai((0, 8)),
    mj.MjHai((1, 2)),
    mj.MjHai((1, 2)),
    mj.MjHai((1, 5)),
    mj.MjHai((1, 6)),
    mj.MjHai((1, 7)),
)

tehai.show()
print()

for cur_yaku_list in tehai.yaku():
    for cur_yaku in cur_yaku_list:
        print(mj.yaku_name[cur_yaku])
    print()
