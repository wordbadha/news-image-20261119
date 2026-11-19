[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/wordbadha/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/wordbadha/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# THE WORLD TODAY — Thursday, 19 November 2026

One image that sums up the world's news of 19 November 2026, drawn as a
newspaper front page: the APEC trilateral in Shenzhen leads, with the ICJ's
Rohingya ruling, the record Anthropic IPO, Jeffries' historic Speaker
nomination, the EU–Indonesia trade deal, Voyager 1's distance record and
the Gaza aid appeal below.

## How it works

`main.ts` (Node 22) runs `build/gen_image.py` (Python 3 + Pillow, no
network). The script draws the whole page — masthead, lead story with a
hand-drawn globe, six story cards, an "also today" strip — and writes
`entry.png` (1024×1024 PNG, under 1 MiB) to the output directory.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
# or: python3 build/gen_image.py /tmp/out
```

The render is deterministic: two runs write byte-identical files.

## License

MIT — see LICENSE.
