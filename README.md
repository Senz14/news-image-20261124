# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Senz14/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Senz14/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

**The world in one day — Tuesday, 24 November 2026.** One original front page summing up the day's world news in six panels: the stories that happened, or were first reported, on 24 November 2026.

## The six stories

1. **Huawei found guilty** — A US jury convicts the tech giant of stealing trade secrets and bank fraud, but clears it of racketeering (United States · China).
2. **Four tankers hit by mines** — Iran says four tankers struck naval mines in the Strait of Hormuz; its Revolutionary Guard says it hit a container ship.
3. **Hamas security chief killed** — Israeli airstrikes kill Naeem Abu Nahel, head of Hamas' internal security, and six others in Gaza.
4. **Kyiv strikes Russian ships** — Ukraine says its drones hit the Russian cargo ship Sparta II in the Gulf of Finland and another off Libya.
5. **Military helicopter crash** — A Turkish Air Force helicopter comes down after take-off from Eskisehir; all five crew members are killed.
6. **Senegal take the Cup back** — Senegal regain the Africa Cup of Nations title after a sports court appeal overturns the final result.

Plus, in the footer: Nvidia brings back Jensen Huang, Oregon and Virginia sue SpaceX, and Germany is first into Ukraine's Delta battlefield system.

## The image

`entry.png` (1024×1024) is an original illustration drawn for this bounty by `draw.py` — no news-agency photographs, no copied artwork. Each panel pairs a pictogram with a short headline and summary, so a viewer who missed the day can tell what happened from the image alone.

## Run it

No build step, no network. `main.ts` (Node 22, standard library only) copies `entry.png` to the output directory, then verifies the copy byte-for-byte (SHA-256) and reports the image's dimensions from its PNG header:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png
```

To redraw the image from scratch: `python3 draw.py` (needs Pillow).

## Files

- `entry.png` — the entry image (1024×1024 PNG).
- `draw.py` — the program that draws `entry.png` (Pillow, standard fonts).
- `main.ts` — the entry program: copies `entry.png` to `/output/entry.png` and verifies the copy.

<sub>Entered on [make.fun](https://make.fun/?ref=jkmc4mts&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
