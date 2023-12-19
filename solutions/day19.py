def parse_input(input: str):
    halves = input.split("\n\n")

    workflows = {}
    for line in halves[0].split("\n"):
        name = line.split("{")[0]
        rules = []
        for rule in line.split("{")[1].split("}")[0].split(","):
            parts = rule.split(":")
            if len(parts) == 1:
                rules.append((None, parts[0]))
            else:
                if ">" in parts[0]:
                    condition_parts = parts[0].split(">")
                    rules.append(
                        ([">", condition_parts[0], int(condition_parts[1])], parts[1])
                    )
                elif "<" in parts[0]:
                    condition_parts = parts[0].split("<")
                    rules.append(
                        (["<", condition_parts[0], int(condition_parts[1])], parts[1])
                    )
                else:
                    raise Exception("Unknown condition")
        workflows[name] = rules

    parts = []
    for part in halves[1].split("\n"):
        parts.append(
            {
                k: int(v)
                for k, v in [
                    part.split("=")
                    for part in part.split("{")[1].split("}")[0].split(",")
                ]
            }
        )

    return {"workflows": workflows, "parts": parts}


def process_part(workflows, part):
    cur_workflow = workflows["in"]
    while True:
        for rule in cur_workflow:
            satisfied = (
                rule[0] is None
                or (rule[0][0] == ">" and part[rule[0][1]] > rule[0][2])
                or (rule[0][0] == "<" and part[rule[0][1]] < rule[0][2])
            )
            if satisfied:
                if rule[1] == "A" or rule[1] == "R":
                    return rule[1]
                else:
                    cur_workflow = workflows[rule[1]]
                    break


def part1(input: str) -> int:
    config = parse_input(input)

    accepted = [
        part
        for part in config["parts"]
        if process_part(config["workflows"], part) == "A"
    ]

    total = 0
    for part in accepted:
        for v in part.values():
            total += v

    return total


def part2(input: str) -> int:
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
