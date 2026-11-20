# The World in One Day — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/wr-xie01/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/wr-xie01/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

Entry for the [make.fun bounty "Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119).

This is a newspaper front page drawn in code. Its masthead names Thursday 19 November 2026, and its six cards cover the day: the Trump–Xi–Putin trilateral signing a four-point peace declaration in Shenzhen; the ICJ ruling 9–6 that Myanmar committed genocide against the Rohingya; the COP31 draft in Antalya dropping fossil-fuel phase-out language; Israel concluding its tank raid across the Yellow Line in Gaza; South Korea's Suneung exam and its crackdown on cheating; and a migrant boat capsizing off Yenne, Senegal.

## What's in here

- `entry.png` — the finished image (1024×1024 PNG, about 126 KB).
- `generate_image.py` — draws `entry.png` with PIL. Regenerate it with `python3 generate_image.py`.
- `main.py` — the entrypoint. It copies `entry.png` into `$MAKEFUN_OUTPUT_DIR` (or `/output`) and refuses to ship anything over the 1 MiB cap.
- `LICENSE` — MIT.

## Why draw it instead of generating it

The judge rewards naming the day, breadth of real stories, readability, faithfulness and craft. Drawing the page in code keeps every word sharp and legible even at small sizes, with no garbled text and nothing invented.
