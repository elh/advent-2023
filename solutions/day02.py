def parse_game(line: str) -> dict:
    parts = line.split(": ")
    number = int(parts[0].split(" ")[1])
    rounds = []
    for round in parts[1].split("; "):
        r = {}
        for color_t in round.split(", "):
            color_parts = color_t.split(" ")
            r[color_parts[1]] = int(color_parts[0])
        rounds.append(r)

    return {
        "number": number,
        "rounds": rounds,
    }


def part1(input: str) -> int:
    cubes: dict[str, int] = {"red": 12, "green": 13, "blue": 14}

    def points(game: dict) -> int:
        if all(
            round[color] <= cubes[color] for round in game["rounds"] for color in round
        ):
            return game["number"]
        return 0

    return sum([points(parse_game(line)) for line in input.split("\n")])


def part2(input: str) -> int:
    def points(game: dict) -> int:
        cubes: dict[str, int] = {"red": 0, "green": 0, "blue": 0}
        for round in game["rounds"]:
            for color in round:
                cubes[color] = max(cubes[color], round[color])
        return cubes["red"] * cubes["green"] * cubes["blue"]

    return sum([points(parse_game(line)) for line in input.split("\n")])
