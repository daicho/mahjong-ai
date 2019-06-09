import mahjong.core as mj

tehai = mj.Tehai()

tehai.tsumo(
    mj.MjHai(0, 1),
    mj.MjHai(0, 1),
    mj.MjHai(0, 5),
    mj.MjHai(0, 5),
    mj.MjHai(0, 5),
    mj.MjHai(1, 5),
    mj.MjHai(1, 5),
    mj.MjHai(1, 5),
)

tehai.furo = [
    [mj.MjHai(0, 3), mj.MjHai(0, 3), mj.MjHai(0, 3), mj.MjHai(0, 3)],
    [mj.MjHai(1, 2), mj.MjHai(1, 2), mj.MjHai(1, 2), mj.MjHai(1, 2)],
]

print(tehai.shanten())
