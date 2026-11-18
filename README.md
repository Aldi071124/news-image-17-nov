# The World in One Image — Tuesday, 17 November 2026

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Aldi071124/news-image-17-nov/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Aldi071124/news-image-17-nov/reward.svg)](https://make.fun/bounty/news-image-20261117)

A 1024×1024 newspaper poster summing up the world news of Tuesday,
17 November 2026, drawn entirely with Python + PIL shapes: the Kerch Bridge
partly collapsing, Iran striking US targets in Bahrain, Houthi attacks on a
Saudi oil pipeline and tankers in the Strait of Hormuz, the Gaza aid call and
a large POW exchange, plus a strip of the day's secondary stories. Every fact
on the poster is as reported that day; nothing is invented.

## Run it

```sh
python3 tools/make-image.py   # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

`main.ts` (Node 22, stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (`/output/entry.png` in the grader).

Entered on [make.fun](https://make.fun/?ref=fhhh2e3k&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
