import mahjong.core as mj

tehai = mj.Tehai()

tehai.append(
    mj.MjHai(0, 2),
    mj.MjHai(0, 3),
    mj.MjHai(0, 4),
    mj.MjHai(0, 6),
    mj.MjHai(0, 7),
    mj.MjHai(0, 8),
    mj.MjHai(1, 3),
    mj.MjHai(1, 4),
    mj.MjHai(1, 5),
    mj.MjHai(1, 7),
    mj.MjHai(1, 7),
    mj.MjHai(1, 7),
    mj.MjHai(1, 8),
    mj.MjHai(1, 8)
)

tehai.yaku()
