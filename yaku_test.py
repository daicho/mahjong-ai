import mahjong.core as mj

tehai = mj.Tehai()

tehai.append(
    mj.MjHai(1, 1),
    mj.MjHai(1, 1),
    mj.MjHai(1, 1),
    mj.MjHai(1, 2),
    mj.MjHai(1, 2),
    mj.MjHai(1, 2),
    mj.MjHai(1, 3),
    mj.MjHai(1, 3),
    mj.MjHai(1, 4),
    mj.MjHai(1, 4),
    mj.MjHai(1, 4),
    mj.MjHai(1, 5),
    mj.MjHai(1, 5),
    mj.MjHai(1, 5),
)

yaku_agari = tehai.yaku()
for yakus in yaku_agari:
    for yaku in yakus:
        print(mj.yaku_list[yaku].fan[0], mj.yaku_list[yaku].name)
    print()
