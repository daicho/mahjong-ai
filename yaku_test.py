import mahjong.core as mj

tehai = mj.Tehai()

tehai.append(
    mj.MjHai(0, 1),
    mj.MjHai(0, 9),
    mj.MjHai(1, 1),
    mj.MjHai(1, 9),
    mj.MjHai(2, 1),
    mj.MjHai(2, 9),
    mj.MjHai(3, 0),
    mj.MjHai(4, 0),
    mj.MjHai(5, 0),
    mj.MjHai(6, 0),
    mj.MjHai(7, 0),
    mj.MjHai(8, 0),
    mj.MjHai(9, 0),
    mj.MjHai(9, 0),
)

tehai.yaku()
