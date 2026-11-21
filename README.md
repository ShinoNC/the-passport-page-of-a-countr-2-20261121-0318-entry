[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/ShinoNC/the-passport-page-of-a-countr-2-20261121-0318-entry/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/ShinoNC/the-passport-page-of-a-countr-2-20261121-0318-entry/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

# The High Republic of Kestra

A passport spread for a country that isn't there: the High Republic of
Kestra, a mountain republic whose passport is valid only above 2,000
metres. The spread carries three pass stamps, a data page with a
portrait, and a machine-readable zone whose check digits are computed,
not faked.

The artwork is drawn in code — `build_spread.py` (PIL) renders the
whole spread, including the MRZ with computed check digits. The entry
itself is `main.ts`, which ships `entry.png` byte-for-byte to the
output directory.

## Run

```sh
node main.ts
```

This writes `/output/entry.png`.

## License

MIT — see [LICENSE](LICENSE).
