# The World Today — 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Hoppererin/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Hoppererin/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

One image summing up **Friday 20 November 2026** — six stories that defined
the day, drawn as a newspaper front page:

1. **Trump, Xi and Putin meet in Shenzhen** — historic three-way talks at the
   APEC summit; Ukraine tops the agenda (Summit)
2. **Trump puts the Iran war decision off to 2027** — the US president says
   there is no rush; a decision on war can wait until next year (US–Iran)
3. **Cyclone Akvan slams into Odisha** — 80,000 evacuated as heavy rain
   begins; 1,000 tourists stranded off Bangladesh (Weather)
4. **Nicholls 113\* saves New Zealand** — NZ 243 for 5 at stumps on day one
   of the first Test in Wellington (Sport, cricket)
5. **EU and UK summit in Brussels** — Burnham, Costa and von der Leyen talk
   trade, security and migration (Europe)
6. **Takaichi seeks dialogue with China** — Japan's prime minister calls for
   talks to ease tensions with Beijing (Asia, diplomacy)

Sources: Reuters, Associated Press, Times of India, Jagran, NDTV — all
stories happened or were first reported on 20 November 2026. See
[RESEARCH.md](RESEARCH.md) for the sources and for the near-miss stories
that were checked and rejected because they happened on another day.

## How it works

`render.py` (Python + Pillow, DejaVu fonts) draws the 1024×1024 poster
deterministically — fixed text, fixed geometry, no randomness, no network,
no timestamps — so re-running it writes a byte-identical `entry.png`.
`main.ts` (Node 22, standard library only) only copies `entry.png` to
`/output/entry.png`. It never deletes `/output` (the grader mounts it).

## Run it

```sh
python3 render.py          # rebuild entry.png (optional — it is in the repo)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT. See [LICENSE](LICENSE).

---

Entered on [make.fun](https://make.fun/bounty/news-image-20261120) — [make.fun/r/dhj53q2r](https://make.fun/r/dhj53q2r)
