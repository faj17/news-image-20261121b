# The World Today — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/faj17/news-image-20261121b/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/faj17/news-image-20261121b/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up Saturday, 21 November 2026: a classic newspaper front page under the masthead **THE WORLD TODAY**, leading with the day's biggest story and carrying the rest of the front page in columns below it. `main.py` is a small, dependency-free Python script that validates the image and copies it byte-for-byte into the output directory.

## Stories on the front page

- **World court finds Myanmar guilty of genocide** — the International Court of Justice rules against Myanmar over the Rohingya, the first time an international court has ever found a state guilty of genocide.
- **Russia's huge overnight barrage on Ukraine** — around 400 drones and 110 missiles in one of the war's largest attacks, with Russian missiles crashing in south-eastern Poland.
- **US Senate rejects Iran war-powers resolution** — the measure fails 51–48.
- **COP31 enters its final stage** — climate talks in Turkey reach their crucial last round, with fossil fuels and climate finance at the centre.
- **Cyclone Akvan crosses the Odisha coast** — the storm makes landfall near Gopalpur with strong winds and heavy rain.
- **Banks hit by vendor cyberattacks** — JPMorgan Chase, Visa and Mastercard report incidents involving third-party providers; core payment networks are unaffected.
- **Fresh aid for Ukraine** — the EU adopts €1 billion in military aid and the UK pledges over 1,000 drones in a £260 million package.
- **Bolsonaro taken to hospital** — Brazil's imprisoned former president is hospitalised with severe abdominal pain.

## How to run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Or pass the output directory directly:

```sh
python3 main.py --output out --verbose
```

Pass `--quiet` to suppress all output except errors:

```sh
python3 main.py --output out --quiet
```

The script checks that `entry.png` is a 1024×1024 PNG no larger than 1 MiB, copies it to the output directory, and verifies the copy's SHA-256 digest matches the original before printing the output path, byte size, dimensions and digest. Python 3.13, standard library only — no network access.

## Verification

Ran `python3 main.py --output out --verbose` twice into `out/`; both runs printed the same SHA-256 (`ac9e3502e794b88e59e27201ddbc14f0f92708bc9f13c6d6ab94bdbd6a7e65f0`), identical to `entry.png` itself — the output is byte-identical across runs. The image is 1024×1024 PNG, 713122 bytes.

## License

MIT — see [LICENSE](LICENSE).

<sub>Entered on [make.fun](https://make.fun/?ref=tzsn25v9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
