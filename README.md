# advent-2023 🎄

![AoC Stars](https://img.shields.io/badge/10-%F0%9F%8C%9F-yellow)

Refamiliarizing myself with Python. I completed [last year's in Clojure](https://github.com/elh/advent-2022).<br>
Inputs and answers are not checked in but can be provided in `inputs/` and `answers.json` respectively.

## Progress

```
Day 1:	✓ ✓ 	 [0.001, 0.0062]
Day 2:	✓ ✓ 	 [0.0004, 0.0004]
Day 3:	✓ ✓ 	 [0.0044, 0.0024]
Day 4:	✓ ✓ 	 [0.0009, 0.0009]
Day 5:	✓ ✓ 	 [0.0002, 5.4009]
Day 6:	- - 	 [None, None]
Day 7:	- - 	 [None, None]
Day 8:	- - 	 [None, None]
Day 9:	- - 	 [None, None]
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

Results: 10 ✓, 0 x, 0 ?, 40 -
Total time (s): 5.4177
```

✓ = Correct, x = Incorrect, ? = No answer provided, - = Unimplemented

## Usage

```bash
# Usage: python main.py <day> <part> <input_file>
# Example: python main.py 25 2 input.txt
#
# Expects files named `solutions/day<day>.py` with functions `part1` and `part2`
# that take the input as a string and return the answer.
python main.py 2 2 input.txt

# Usage: python all.py
#
# Runs all solutions in the stype of `main.py` and checks with answers present
# in `answers.json`. Expects inputs to be named `inputs/<day>.txt`.
python all.py

# or just run `make`
```

## Development

```bash
make lint       # mypy, ruff
make pretty     # black
```
