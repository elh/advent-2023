def parse_input(input: str) -> list[list[list[str]]]:
    groups = input.split("\n\n")
    out = []
    for group in groups:
        out.append([[char for char in line] for line in group.split("\n")])
    return out


# is a horizontal line of reflection (reflected vertically)
# return a tuple of (<is reflection>, <has only a single defect pair>)
def is_horizontal_line(i: int, grid: list[list[str]]) -> tuple[bool, bool]:
    seen_defect = False
    up = i - 1
    down = i
    while up >= 0 and down < len(grid):
        for j in range(len(grid[0])):
            if grid[up][j] != grid[down][j]:
                if seen_defect:
                    return False, False
                seen_defect = True
        up -= 1
        down += 1

    return not seen_defect, seen_defect


# is a vertical line of reflection (reflected horizontally)
# return a tuple of (<is reflection>, <has only a single defect pair>)
def is_vertical_line(i: int, grid: list[list[str]]) -> tuple[bool, bool]:
    seen_defect = False
    left = i - 1
    right = i
    while left >= 0 and right < len(grid[0]):
        for line in grid:
            if line[left] != line[right]:
                if seen_defect:
                    return False, False
                seen_defect = True
        left -= 1
        right += 1

    return not seen_defect, seen_defect


def score(grid: list[list[str]], with_smudge: bool = False) -> int:
    score = 0
    for i in range(1, len(grid)):
        ok, one_smudge = is_horizontal_line(i, grid)
        if (not with_smudge and ok) or (with_smudge and one_smudge):
            score += i * 100
    for i in range(1, len(grid[0])):
        ok, one_smudge = is_vertical_line(i, grid)
        if (not with_smudge and ok) or (with_smudge and one_smudge):
            score += i

    return score


def part1(input: str) -> int:
    grids = parse_input(input)
    scores = [score(grid) for grid in grids]
    return sum(scores)


def part2(input: str) -> int:
    grids = parse_input(input)
    scores = [score(grid, with_smudge=True) for grid in grids]
    return sum(scores)
