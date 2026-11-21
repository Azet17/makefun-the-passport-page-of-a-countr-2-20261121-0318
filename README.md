[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Azet17/makefun-the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Azet17/makefun-the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

Entry for the make.fun bounty: https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318

# The Passport Page of a Country That Does Not Exist

An invented passport spread for the **Republic of Kaldrin** — a small
landlocked mountain republic, capital Tarnholm, nationality KALDRINIAN.
Rendered as one open spread (1024x640): the data page on the left, the
visas/stamps page on the right.

## How to run

```sh
python3 draw.py    # renders entry.png in this directory
python3 main.py    # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

`draw.py` needs Pillow; `main.py` is stdlib only. Both are deterministic —
re-running produces the same image.

## The invented country

- **Republic of Kaldrin** — landlocked mountain republic; capital **Tarnholm**.
- Holder: **Maren Ilsa Veyn**, born 12 JUN 1988 in Tarnholm, sex F.
- Passport **KD 417 902**, issued **14 MAR 2021** in Tarnholm, expires
  **14 MAR 2031**. The machine-readable zone (TD3, two 44-character lines)
  is generated in code with ICAO 9303 check digits computed from the data
  above, so the MRZ agrees with the printed fields.
- The portrait is drawn procedurally with PIL shapes and shading
  (duotone document-photo treatment) — no pasted face.
- Neighbours stamped in the passport: **Ostravia** (Velgorod border) and
  **Meridia** (Port Salenne).

## Date-consistency rules followed

1. **No stamp predates the passport.** Every stamp is dated after the
   14 MAR 2021 issue date.
2. **Chronological order, matching entry/exit pairs:**
   Ostravia entry 08 APR 2022 / exit 21 APR 2022; Meridia entry
   17 SEP 2023 / exit 02 OCT 2023; Ostravia entry 05 JUN 2025 /
   exit 19 JUN 2025.
3. **Place of issue agrees everywhere:** Tarnholm is the place of birth,
   place of issue, and issuing authority.
4. **Expiry is 10 years after issue** (14 MAR 2021 → 14 MAR 2031) and the
   MRZ expiry field (310314) matches.
5. **Telling paperwork detail:** a stamped condition —
   "HIGH VALLEYS PERMIT K-7 REQUIRED BEYOND 2,400 M" — with a fee stamp
   (40 krona, paid 03 JUN 2025, Tarnholm), plus a bilingual column
   (English / Kaldrin: "REISEPASS · KALDRIN TORVA LÆND"), showing what
   kind of place Kaldrin is: a high mountain republic where the valleys
   keep their own road.
