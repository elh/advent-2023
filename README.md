# advent-2023 🎄

![AoC Stars](https://img.shields.io/badge/18-%F0%9F%8C%9F-yellow)

Refamiliarizing myself with Python. I completed [last year's in Clojure](https://github.com/elh/advent-2022).<br>
Inputs and answers are not checked in but can be provided in `inputs/` and `answers.json` respectively.

## Progress

`make` result:
```
Day 1:	✓ ✓ 	 [0.001, 0.0066]
Day 2:	✓ ✓ 	 [0.0004, 0.0005]
Day 3:	✓ ✓ 	 [0.0046, 0.0024]
Day 4:	✓ ✓ 	 [0.0009, 0.0009]
Day 5:	✓ ✓ 	 [0.0002, 0.001]
Day 6:	✓ ✓ 	 [0.0, 0.0]
Day 7:	✓ ✓ 	 [0.0134, 0.0181]
Day 8:	✓ ✓ 	 [0.0024, 0.0144]
Day 9:	✓ ✓ 	 [0.0024, 0.0023]
Day 10:	- - 	 [None, None]
Day 11:	- - 	 [None, None]
Day 12:	- - 	 [None, None]
Day 13:	- - 	 [None, None]
Day 14:	- - 	 [None, None]
Day 15:	- - 	 [None, None]
Day 16:	- - 	 [None, None]
Day 17:	- - 	 [None, None]
Day 18:	- - 	 [None, None]
Day 19:	- - 	 [None, None]
Day 20:	- - 	 [None, None]
Day 21:	- - 	 [None, None]
Day 22:	- - 	 [None, None]
Day 23:	- - 	 [None, None]
Day 24:	- - 	 [None, None]
Day 25:	- - 	 [None, None]

Results: 18 ✓, 0 x, 0 ?, 32 -, 0 s
Total time (s): 0.0714
```

✓ = Correct, x = Incorrect, ? = No answer provided, - = Unimplemented, s = Skipped

## Usage

I have a nice harness that dynamically imports solution files and functions to run them. We can check all of them against saved answers to prevent regressions.

```bash
# Usage: python main.py <day> <part> <input_file>
# Example: python main.py 25 2 input.txt
#
# Expects files named `solutions/day<day>.py` with functions `part1` and `part2`
# that take the input as a string and return the answer. The file name <day> is
# 0-padded to 2 digits.
python main.py 2 2 input.txt

# Usage: python all.py [--skip <skip>]
#
# Runs all solutions in the stype of `main.py` and checks with answers present
# in `answers.json`. --skip is an optional csv of parts to skip. parts are
# represented as <day>.<part>, e.g. 1.1, 25.2
python all.py

# or just run `make`. `SKIP=5.2 make` to skip specified parts
```

## Development

```bash
make lint       # mypy, ruff
make pretty     # black

make good       # runs lint, pretty
```

## Log

* 12/1
  * Wasn't sure if I would do it this year but I can't resist challenging friends to do it. Starting a private leaderboard with a bounty. I don't think I will have as much time as I did last year learning Clojure so opting for Python 🐍. Started on a flight to Taiwan for family 🇹🇼.
  * Day 1: Pleased with this idea of reversing the entire text and the words I am searching for to generalize the search.
  * Implemented a common main.py that can dynamically import solutions functions via importlib.
* 12/2
  * Played around with some Python tooling: ruff, black, mypy.
  * Added a all.py script.
* 12/3
  * Day 4: Nice clean single-pass iterative solution.
* 12/4
  * Day 5: Pleased with how fast I solved part 2 by coming up with a well bounded brute force solution. Performance is quite poor though taking 5s and I get a little confused thinking through the ranges. Done shortly after takeoff from Taiwan back to SF 🌉.
* 12/5
  * Day 6: Heh... I solved it quickly with a janky binary search before looking up the quadratic equation.
* 12/6
  * Day 7: Finished 396th! This was the first night that I was at my computer at 9pm and prioritized speed so I'm quite pleased with this. My approach treating hands as a dict of card -> count was amenable to handling jokers 🃏.
* 12/7
  * Day 8: I was surprised that this math was needed as early as day 8 so I waited for my naive solution to complete a little too long. Finished 1021st. Won't be able to care about that anymore as I'm about to be traveling for the next week 🇬🇧🇮🇳.
  * At this point, I am leading 11 coworkers in my private leaderboard. I'm having the most fun chatting with the non-engineers doing it for the first time - 2 of them occupying 2nd and 3rd place.
* 12/9
  * Day 9: Done before bed in London after a 10 hour flight next to toddlers and 14K steps around xmas markets 🎅...
