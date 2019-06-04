import mahjong.core as mj

tehai = mj.Tehai()

tehai.append(
    mj.MjHai(0, 1),
    mj.MjHai(0, 2),
    mj.MjHai(0, 3),
    mj.MjHai(1, 1),
    mj.MjHai(1, 2),
    mj.MjHai(1, 3),
    mj.MjHai(2, 1),
    mj.MjHai(2, 2),
    mj.MjHai(2, 3),
    mj.MjHai(0, 9),
    mj.MjHai(0, 9),
    mj.MjHai(0, 9),
    mj.MjHai(4, 0),
    mj.MjHai(4, 0),
)

tehai.yaku()
