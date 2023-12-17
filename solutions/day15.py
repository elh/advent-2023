def parse_input(input: str) -> list[dict[str, str]]:
    out = []
    for step in input.split(","):
        if step.endswith("-"):
            out.append(
                {
                    "raw": step,
                    "op": "-",
                    "label": step[:-1],
                }
            )
        else:
            parts = step.split("=")
            out.append(
                {
                    "raw": step,
                    "op": "=",
                    "label": parts[0],
                    "value": parts[1],
                }
            )
    return out


def holiday_hash(s: str) -> int:
    cur = 0
    for char in s:
        cur += ord(char)
        cur *= 17
        cur %= 256
    return cur


class HolidayHashMap:
    def __init__(self) -> None:
        self.dict: dict[int, list[tuple[str, int]]] = {}

    def add(self, k: str, v: int) -> None:
        h = holiday_hash(k)
        if h not in self.dict:
            self.dict[h] = []

        key_exists = k in [t[0] for t in self.dict[h]]
        if key_exists:
            self.dict[h] = [(k, v) if t[0] == k else t for t in self.dict[h]]
        else:
            self.dict[h].append((k, v))

    def remove(self, k: str) -> None:
        h = holiday_hash(k)
        if h in self.dict:
            self.dict[h] = [t for t in self.dict[h] if t[0] != k]


def focusing_power(lens_boxes: dict[int, list[tuple[str, int]]]) -> int:
    total = 0
    for box_num, lenses in lens_boxes.items():
        for i, lens in enumerate(lenses):
            total += (box_num + 1) * (i + 1) * lens[1]

    return total


def part1(input: str) -> int:
    steps = parse_input(input)
    values = [holiday_hash(step["raw"]) for step in steps]
    return sum(values)


def part2(input: str) -> int:
    steps = parse_input(input)

    hm = HolidayHashMap()
    for step in steps:
        if step["op"] == "=":
            hm.add(step["label"], int(step["value"]))
        elif step["op"] == "-":
            hm.remove(step["label"])
        else:
            raise Exception("unsupported op")

    return focusing_power(hm.dict)
