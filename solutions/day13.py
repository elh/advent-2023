def parse_input(input: str) -> list[list[list[str]]]:
    groups = input.split("\n\n")
    out = []
    for group in groups:
        out.append([[char for char in line] for line in group.split("\n")])
    return out


# is a horizontal line of reflection (reflected vertically)
def is_horizontal_line(i: int, grid: list[list[str]]) -> bool:
    up = i - 1
    down = i
    while up >= 0 and down < len(grid):
        if grid[up] != grid[down]:
            return False
        up -= 1
        down += 1

    return True


def is_vertical_line(i: int, grid: list[list[str]]) -> bool:
    left = i - 1
    right = i
    while left >= 0 and right < len(grid[0]):
        for line in grid:
            if line[left] != line[right]:
                return False
        left -= 1
        right += 1

    return True


def part1(input: str) -> int:
    grids = parse_input(input)

    score = 0
    for grid in grids:
        for i in range(1, len(grid)):
            if is_horizontal_line(i, grid):
                score += i * 100
        for i in range(1, len(grid[0])):
            if is_vertical_line(i, grid):
                score += i

    return score


def part2(input: str) -> int:
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
