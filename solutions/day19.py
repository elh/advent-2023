from functools import reduce
import operator


def parse_input(input: str):
    halves = input.split("\n\n")

    workflows = {}
    for line in halves[0].split("\n"):
        if line.startswith("#"):
            continue
        name = line.split("{")[0]
        rules: list[tuple] = []
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

    values: list[dict[str, int]] = []
    for part in halves[1].split("\n"):
        values.append(
            {
                k: int(v)
                for k, v in [
                    part.split("=")
                    for part in part.split("{")[1].split("}")[0].split(",")
                ]
            }
        )

    return {"workflows": workflows, "values": values}


def workflow_pointers(workflows):
    pointers = {}
    for name, rules in workflows.items():
        for i, rule in enumerate(rules):
            if rule[1] == "A" or rule[1] == "R":
                continue
            if rule[1] not in pointers:
                pointers[rule[1]] = []
            pointers[rule[1]].append((name, i))
    return pointers


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


def product(l: list) -> int:
    return reduce(operator.mul, l, 1)


default_ranges = {
    "x": (1, 4000),
    "m": (1, 4000),
    "a": (1, 4000),
    "s": (1, 4000),
}


def count_combos(workflows, workflow_ptrs, wf_name, rule_idx, ranges):
    def matches(ranges, rule):
        ranges = ranges.copy()
        if rule[0] is None:
            return ranges
        elif rule[0][0] == ">":
            var, val = rule[0][1], rule[0][2]
            ranges[var] = (max(ranges[var][0], val + 1), ranges[var][1])
            return ranges
        elif rule[0][0] == "<":
            var, val = rule[0][1], rule[0][2]
            ranges[var] = (ranges[var][0], min(ranges[var][1], val - 1))
            return ranges
        else:
            raise Exception("Unknown condition")

    def not_matches(ranges, rule):
        ranges = ranges.copy()
        if rule[0][0] == ">":
            var, val = rule[0][1], rule[0][2]
            ranges[var] = (ranges[var][0], min(ranges[var][1], val))
            return ranges
        elif rule[0][0] == "<":
            var, val = rule[0][1], rule[0][2]
            ranges[var] = (max(ranges[var][0], val), ranges[var][1])
            return ranges
        else:
            raise Exception("Unknown condition or no match")

    cur_workflow = workflows[wf_name]
    ranges = matches(ranges, cur_workflow[rule_idx])
    for i in reversed(range(rule_idx)):
        ranges = not_matches(ranges, cur_workflow[i])

    if wf_name == "in":
        counts = []
        for v in ranges.values():
            counts.append(v[1] - v[0] + 1)
        return product(counts)
    else:
        total = 0
        if wf_name in workflow_ptrs:
            for parent_wf, rule_idx in workflow_ptrs[wf_name]:
                total += count_combos(
                    workflows, workflow_ptrs, parent_wf, rule_idx, ranges
                )
        return total


def part1(input: str) -> int:
    config = parse_input(input)
    accepted = [
        part
        for part in config["values"]
        if process_part(config["workflows"], part) == "A"
    ]

    total = 0
    for part in accepted:
        for v in part.values():
            total += v

    return total


def part2(input: str) -> int:
    config = parse_input(input)
    workflows = config["workflows"]
    workflow_ptrs = workflow_pointers(workflows)

    # work backwards. find all "A"s and reverse to construct the possible ranges
    total = 0
    for name, rules in workflows.items():
        for i, rule in enumerate(rules):
            if rule[1] == "A":
                total += count_combos(workflows, workflow_ptrs, name, i, default_ranges)
    return total
