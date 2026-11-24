# news-image-20261123-0xdemon

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/DemonDeployer/news-image-20261123-0xdemon/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/DemonDeployer/news-image-20261123-0xdemon/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up Monday 23 November 2026's world news: Nvidia's board unanimously reinstates Jensen Huang as CEO and the shares surge about 31%, Ukraine's naval drones sink the Russian corvette Merkury off Libya, COP31 collapses in Antalya with no deal, the US imposes sweeping new sanctions on Iran, the FBI probes an apparent hack of its NCIC crime database, and a candy-factory fire kills 24 in Indonesia — six verified stories, dated and labelled, in a single front-page composition. The footer ticker adds the Nigeria funeral-boat disaster, the UK hosting the 2035 Women's World Cup, and Skubal's record $450m Mets deal.

`main.py` copies `entry.png` (1024×1024) to the output directory, so the image is byte-identical on every run. `draw_entry.py` is the Pillow program that drew it locally from the six stories (run it to regenerate the image; it needs Pillow and the DejaVu fonts, so it is not part of the graded run).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources (23 November 2026)

- Nvidia reinstates Jensen Huang as CEO; shares +31% — Reuters; Wall Street Journal; CNN; SEC Form 8-K
- Ukraine sinks Russian corvette Merkury off Libya — AP; Reuters; Xinhua
- COP31 collapses in Antalya, no deal — CNN; AP; BBC
- US imposes sweeping new Iran sanctions — US Treasury; Reuters
- FBI probes apparent hack of NCIC crime database — AP; CNN; TechCrunch
- Indonesia candy-factory fire kills 24, dozens missing — AP
- Nigeria funeral boat capsizes (24 dead); UK to host 2035 Women's World Cup; Skubal $450m Mets deal; Russian jets enter South Korea's air-defence zone; China sentences official to death for spying — AP; Reuters; BBC

---

<sub>Entered on [make.fun](https://make.fun/?ref=qamf9tkx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
