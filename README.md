# advent-2023 🎄

![AoC Stars](https://img.shields.io/badge/32-%F0%9F%8C%9F-yellow)

Refamiliarizing myself with Python. I completed [last year's in Clojure](https://github.com/elh/advent-2022).<br>
Inputs and answers are not checked in but can be provided in `inputs/` and `answers.json` respectively.

## Progress

`make` result:
```
Day 1:	✓ ✓ 	 [0.0012, 0.008]
Day 2:	✓ ✓ 	 [0.0005, 0.0006]
Day 3:	✓ ✓ 	 [0.0056, 0.003]
Day 4:	✓ ✓ 	 [0.0012, 0.0012]
Day 5:	✓ ✓ 	 [0.0002, 0.0013]
Day 6:	✓ ✓ 	 [0.0, 0.0]
Day 7:	✓ ✓ 	 [0.0176, 0.0243]
Day 8:	✓ ✓ 	 [0.0034, 0.0205]
Day 9:	✓ ✓ 	 [0.0033, 0.0033]
Day 10:	✓ ✓ 	 [0.0156, 0.1614]
Day 11:	✓ ✓ 	 [0.0099, 0.0769]
Day 12:	✓ ✓ 	 [0.0273, 0.6667]
Day 13:	✓ ✓ 	 [0.0016, 0.0015]
Day 14:	✓ ✓ 	 [0.0014, 0.6438]
Day 15:	✓ ✓ 	 [0.0029, 0.0042]
Day 16:	✓ ✓ 	 [0.0119, 0.8791]
Day 17:	- - 	 [None, None]
Day 18:	- - 	 [None, None]
Day 19:	- - 	 [None, None]
Day 20:	- - 	 [None, None]
Day 21:	- - 	 [None, None]
Day 22:	- - 	 [None, None]
Day 23:	- - 	 [None, None]
Day 24:	- - 	 [None, None]
Day 25:	- - 	 [None, None]

Results: 32 ✓, 0 x, 0 ?, 18 -, 0 s
Total time (s): 2.5994
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
  * Added an all.py script.
* 12/3
  * Day 4: Clean single-pass iterative solution.
* 12/4
  * Day 5: Pleased with how fast I solved part 2 by coming up with a well bounded brute force solution. Performance is quite poor though taking 5s and I get a little confused thinking through the ranges. Done shortly after takeoff from Taiwan back to SF 🌉.
* 12/5
  * Day 6: Heh... I solved it quickly with a janky binary search before looking up the quadratic equation.
* 12/6
  * Day 7: Finished 396th! This was the first night that I was at my computer at 9pm and prioritized speed so I'm quite pleased with this. My approach treating hands as a dict of card -> count was amenable to handling jokers 🃏.
* 12/7
  * Day 8: I was surprised that this math was needed as early as day 8 so I waited for my naive solution to complete a little too long.
  * At this point heading into travel next week 🇬🇧🇮🇳, I am leading 11 coworkers in my private leaderboard. I'm having a ton of fun chatting with the non-engineers doing it for the first time - 2 of them occupying 2nd and 3rd place.
* 12/9
  * Day 9: Done before bed in London after a 10 hour flight next to toddlers and 14K steps around xmas markets 🎅...
* 12/10
  * Day 10: Part 2 is the first puzzle to defeat me on the initial sitting at 6am jet lagged in the citizenM Bankside lobby. I'm familiar with winding numbers but have difficulty adapting the idea to the ascii grid after horribly fumbling the set up in Part 1.
* 12/11
  * Day 11: Part 1 completed in a taxi on the way to Heathrow airport.
  * Day 10: Part 2 revisited and solved using the even-odd rule for winding numbers and checking on cardinal directions from a given point. Great puzzle! We handle corners by treating them as connecting on one side. The next seen corner either connects on the opposite side completing the wall or on the same side which cancels it out. Some fun corner cases like handling "S" and handling unconnected pipes are done as preprocessing. Done before falling asleep the flight from London to Delhi on the way to a coworker's wedding.
* 12/16
  * Wrapped up an incredible wedding in Jaipur 🎊!
  * Day 12: Part 2 solved with DP by treating `s[1:]` as the subproblem and using the `@cache` decorator.
  * Quickly got through Days 13-16 part 1's so I have access to part 2's for the flight back in case I'm not too sleepy 😪.
  * Day 14: Part 2 solved by detecting loops and finding equivalent position via modulo.
  * Day 16: Performance improved reusing previous results. `cast_light` returns a graph of lights and downstream lights which we can optionally take as an argument as well and build upon.
