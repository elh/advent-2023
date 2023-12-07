word_ints = [
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
]


def get_first_int(line: str, as_word: bool = False, reverse: bool = False) -> int:
    line = line[::-1] if reverse else line
    for i in range(len(line)):
        if line[i].isdigit():
            return int(line[i])
        if as_word:
            for word, value in word_ints:
                if line[i:].startswith(word if not reverse else word[::-1]):
                    return value
    raise ValueError("No int found")


def part1(input: str) -> int:
    return sum(
        int(str(get_first_int(line)) + str(get_first_int(line, reverse=True)))
        for line in input.split("\n")
    )


def part2(input: str) -> int:
    return sum(
        int(
            str(get_first_int(line, as_word=True))
            + str(get_first_int(line, as_word=True, reverse=True))
        )
        for line in input.split("\n")
    )
