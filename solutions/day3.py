# including diagonals
def neighbors(i, j):
    return [
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ]


def adjacent_to_symbol(number_str, start_idx, symbols):
    locs = set()
    for i in range(len(number_str)):
        for neighbor in neighbors(start_idx[0], start_idx[1] + i):
            locs.add(neighbor)
    return locs & symbols


def part1(input: str) -> int:
    # build set of all symbol locations
    symbols = set()
    for i, line in enumerate(input.split("\n")):
        for j, c in enumerate(line):
            if c != "." and not c.isdigit():
                symbols.add((i, j))

    # build a list of tuples of numbers and their starting locations
    numbers = []
    current_number = ""
    for i, line in enumerate(input.split("\n")):
        for j, c in enumerate(line):
            if c.isdigit():
                current_number += c
            elif current_number:
                numbers.append((current_number, (i, j - len(current_number))))
                current_number = ""
        if current_number:
            numbers.append((current_number, (i, j - len(current_number))))
            current_number = ""

    adjacent_numbers = [v for v in numbers if adjacent_to_symbol(*v, symbols)]
    return sum(int(v[0]) for v in adjacent_numbers)


def part2(input: str) -> int:
    # build set of all gear locations
    gears = set()
    for i, line in enumerate(input.split("\n")):
        for j, c in enumerate(line):
            if c == "*":
                gears.add((i, j))

    # build up a map of squares with a number on it to the number
    numbers = {}
    current_number = ""
    for i, line in enumerate(input.split("\n")):
        for j, c in enumerate(line):
            if c.isdigit():
                current_number += c
            elif current_number:
                for k in range(len(current_number)):
                    numbers[(i, j - len(current_number) + k)] = (
                        int(current_number),
                        (i, j),
                    )
                current_number = ""
        if current_number:
            for k in range(len(current_number)):
                numbers[(i, j - len(current_number) + k)] = (
                    int(current_number),
                    (i, j),
                )
            current_number = ""

    total = 0
    for gear in gears:
        neighbor_numbers = set()
        for n in neighbors(*gear):
            if n in numbers:
                neighbor_numbers.add(numbers[n])
        if len(neighbor_numbers) == 2:
            l = list(neighbor_numbers)
            total += l[0][0] * l[1][0]

    return total
