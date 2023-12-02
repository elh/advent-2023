import argparse


# Usage: python input.py <day>
# Utility to print the input URL for terminal Cmd+click convenience.
def main():
    year = 2023
    parser = argparse.ArgumentParser()
    parser.add_argument("day", help="1 to 25")
    args = parser.parse_args()

    print("https://adventofcode.com/{}/day/{}/input".format(year, args.day))


if __name__ == "__main__":
    main()
