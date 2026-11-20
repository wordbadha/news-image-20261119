[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/wordbadha/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/wordbadha/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# THE WORLD TODAY — Thursday, 19 November 2026

One image summing up the world's news of 19 November 2026, drawn as a newspaper front page. The APEC trilateral in Shenzhen leads the page, with the ICJ's Rohingya ruling, the record Anthropic IPO, Jeffries' historic Speaker nomination, the EU–Indonesia trade deal, Voyager 1's distance record and the Gaza aid appeal below.

## How it works

`main.ts` copies the pre-rendered `entry.png` to the output directory and validates the copy: PNG signature, IHDR chunk, 1024×1024 dimensions, IEND terminator, and a size under 1 MiB. No network, no dependencies, nothing beyond Node's standard library.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
```

The image lands at `/tmp/out/entry.png`.
