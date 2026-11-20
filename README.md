# The World in One Day — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/wr-xie01/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/wr-xie01/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

Entry for the [make.fun bounty "Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119).

The entry is a newspaper front page drawn in code: a masthead naming Thursday 19 November 2026 and six stories from that day — the Trump–Xi–Putin trilateral signing a four-point peace declaration in Shenzhen, the ICJ ruling 9–6 that Myanmar committed genocide against the Rohingya, the COP31 draft in Antalya dropping fossil-fuel phase-out language, Israel concluding its tank raid across the Yellow Line in Gaza, South Korea's Suneung exam with a crackdown on cheating, and a migrant boat capsizing off Yenne, Senegal.

## Files

- `entry.png` — the image itself (1024×1024 PNG, ~126 KB).
- `generate_image.py` — draws `entry.png` with PIL. Run it to regenerate: `python3 generate_image.py`
- `main.py` — the entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`), with a 1 MiB size guard.
- `LICENSE` — MIT.

## Why drawn, not AI-generated

The judge scores on naming the day, breadth of real stories, readability, faithfulness and craft. A programmatically drawn page keeps every word crisp and legible at small sizes, with no garbled text or invented details.
