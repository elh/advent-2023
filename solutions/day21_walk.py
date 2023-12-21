import day21
import argparse

"""
shape   command for an example
-----------------------------------------------------------------------------------
square  time python solutions/day21_walk.py inputs/21.txt --steps 131
corner  python solutions/day21_walk.py inputs/21.txt --steps 65 --start_loc="0,130"
house   python solutions/day21_walk.py inputs/21.txt --steps 131 --start_loc="0,65"
chipped python solutions/day21_walk.py inputs/21.txt --steps 196 --start_loc="0,0"

walking for 1.5 grid lengths, crossing over 9 original grids
python solutions/day21_walk.py inputs/21.txt --steps 196 --print_grid --width 3 --start_loc="196,196"
"""


def expand_grid(grid, n):
    new_rows = []
    for row in grid:
        new_rows.append(row * n)
    return new_rows * n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input file")
    parser.add_argument("--steps", type=int, default=65, help="number of steps to take")
    parser.add_argument("--start_loc", help="start point")
    parser.add_argument(
        "--print_grid",
        type=bool,
        default=False,
        help="if true, print grid",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--width", type=int, default=1, help="how many original grids wide"
    )
    args = parser.parse_args()

    input = open(args.input_file, "r").read().rstrip("\n")
    grid, start_loc = day21.parse_input(input)
    if args.start_loc:
        start_loc = tuple(map(int, args.start_loc.split(",")))
    if args.width > 1:
        grid = expand_grid(grid, args.width)

    count = day21.walk(grid, start_loc, args.steps, print_final_grid=args.print_grid)
    print(count)


if __name__ == "__main__":
    main()
