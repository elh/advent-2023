def parse_game(line: str) -> dict:
    parts = line.split(": ")
    out = {
        "number": int(parts[0].split(" ")[1]),
        "rounds": [],
    }

    for round in parts[1].split("; "):
        r = {}
        for color_t in round.split(", "):
            color_parts = color_t.split(" ")
            r[color_parts[1]] = int(color_parts[0])
        out["rounds"].append(r)

    return out

def p1(input: str) -> bool:
    cubes = {"red": 12, "green": 13, "blue": 14}
    total = 0
    for line in input.split("\n"):
        game = parse_game(line)
        valid = True
        for round in game["rounds"]:
            for color in round:
                if round[color] > cubes[color]:
                    valid = False
                    break
        if valid:
            total += game["number"]
    return total

def p2(input: str) -> bool:
    total = 0
    for line in input.split("\n"):
        game = parse_game(line)
        cubes = {"red": 0, "green": 0, "blue": 0}
        for round in game["rounds"]:
            for color in round:
                if round[color] > cubes[color]:
                    cubes[color] = round[color]
        total += cubes["red"] * cubes["green"] * cubes["blue"]
    return total
