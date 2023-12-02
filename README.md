# advent-2023 🎄

![AoC Stars](https://img.shields.io/badge/4-%F0%9F%8C%9F-yellow)

Refamiliarizing myself with Python. I completed [last year's in Clojure](https://github.com/elh/advent-2022).<br>
Inputs and answers are not checked in but can be provided in `inputs/` and `answers.json` respectively.

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
```

## Development

```bash
make lint       # mypy, ruff
make pretty     # black
```
