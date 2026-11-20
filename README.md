# The World in One Page — Friday 20 November 2026

[![Competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/bapenven-ctrl/news-image-20nov/rank.svg)](https://make.fun/c/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/bapenven-ctrl/news-image-20nov/reward.svg)](https://make.fun/c/news-image-20261120)

One page of world news for **Friday 20 November 2026**: 41 stories, every one
of them reported that day, in at least one time zone.

## What is on the page

- **3 lead stories**, fully illustrated: Cyclone Akvan's landfall at Gopalpur
  (370,000 evacuated), Russia's overnight barrage on Kyiv (110+ missiles,
  three Dnipro bridges damaged), and Asia's AI rout at Friday's close in
  Tokyo (Nikkei −5.1%).
- **10 illustrated cards**: a Russian Kh-101 down in Poland, the UK–EU reset
  deal, COP31's final day in Antalya, Saudi Arabia's interception of a Houthi
  missile, Iraqi forces in Jurf al-Sakhar, Pakistan's minister in New Delhi,
  Signal blocking screenshots, Pakistan's series win in Rawalpindi,
  Prabowo–Xi in Shenzhen, and Seoul's move to impeach the chief justice.
- **28 briefs**, a dotted world map with pins for stories 1–13, a "Friday in
  UTC" timeline, and a printed **DATE CHECK** box listing the stories that
  were checked and deliberately *not* shown as Friday's news (among them the
  Trump–Iran interviews of Thu 19 Nov and Voyager 1's one-light-day milestone
  of Wed 18 Nov).

Every story was date-checked against a datelined source (UTC and local time)
before it was drawn; claims are labelled CLAIM on the page.

## How it runs

`main.py` (Python 3, standard library only) copies the pre-rendered sheet
`entry.png` into `$MAKEFUN_OUTPUT_DIR` (or `./output`).

The sheet itself was drawn with a deterministic procedural renderer
(original flat illustrations, no photographs), in this repository's build
session.

## License

MIT — see `LICENSE`.
