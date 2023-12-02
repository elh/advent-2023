import argparse
import importlib


# Usage: python main.py <day> <part> <input_file>
# Example: python main.py 25 2 input.txt
#
# Expects files named `solutions/day<day>.py` with functions `part1` and `part2`
# that take the input as a string and return the answer.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", help="1 to 25")
    parser.add_argument("part", help="1 or 2")
    parser.add_argument("input_file", help="path to input file")
    args = parser.parse_args()

    input = open(args.input_file, "r").read().rstrip("\n")
    module = importlib.import_module("solutions.day" + args.day)
    fn = getattr(module, "part" + args.part)
    print(fn(input))


if __name__ == "__main__":
    main()
