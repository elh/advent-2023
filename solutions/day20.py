import pprint

ITERATIONS = 1000
VERBOSE = False


def parse_modules(input: str):
    lines = [line for line in input.split("\n") if not line.startswith("#")]
    modules: dict[str, dict] = {}
    for line in lines:
        parts = line.split(" -> ")

        m_str = parts[0]
        if m_str.startswith("%"):
            name = m_str[1:]
            type = "flip"
        elif m_str.startswith("&"):
            name = m_str[1:]
            type = "conj"
        elif m_str == "broadcaster":
            name = m_str
            type = "broadcaster"
        else:
            raise Exception("malformed module: {}".format(m_str))

        dests = parts[1].split(", ")
        modules[name] = {"type": type, "dests": dests}

    # init state
    for module in modules.values():
        if module["type"] == "flip":
            module["state"] = "off"
        if module["type"] == "conj":
            module["remembered"] = {}
    for name, module in modules.items():
        for dest in module["dests"]:
            if dest not in modules:
                continue
            if modules[dest]["type"] == "conj":
                modules[dest]["remembered"][name] = "low"

    return modules


def debug(args):
    if VERBOSE:
        pprint.pprint(args)


def flip(state: str) -> str:
    if state == "on":
        return "off"
    else:
        return "on"


Pulse = tuple[str, str, str]  # (from, "high"/"low", to)


# mutates the state of modules
def press_button(modules: dict) -> list[Pulse]:
    pulse_history = []

    pulses = [("button", "low", "broadcaster")]
    while len(pulses) > 0:
        pulse = pulses.pop(0)
        pulse_history.append(pulse)
        pulse_from, pulse_highlow, pulse_to = pulse
        debug(modules)
        debug((pulse_from, pulse_highlow, pulse_to))

        if pulse_to not in modules:
            continue

        pulse_to_module = modules[pulse_to]
        if pulse_to_module["type"] == "flip":
            if pulse_highlow == "high":
                continue
            pulse_to_module["state"] = flip(pulse_to_module["state"])
            new_highlow = "high" if pulse_to_module["state"] == "on" else "low"

            for dest in pulse_to_module["dests"]:
                pulses.append((pulse_to, new_highlow, dest))
        elif pulse_to_module["type"] == "conj":
            pulse_to_module["remembered"][pulse_from] = pulse_highlow
            if "low" not in pulse_to_module["remembered"].values():
                new_highlow = "low"
            else:
                new_highlow = "high"
            for dest in pulse_to_module["dests"]:
                pulses.append((pulse_to, new_highlow, dest))
        elif pulse_to_module["type"] == "broadcaster":
            for dest in pulse_to_module["dests"]:
                pulses.append((pulse_to, pulse_highlow, dest))
        else:
            raise Exception("bad module type")

    return pulse_history


def part1(input: str) -> int:
    modules = parse_modules(input)

    low_pulse_count, high_pulse_count = 0, 0
    for _ in range(ITERATIONS):
        pulses = press_button(modules)
        low_pulse_count += len([pulse for pulse in pulses if pulse[1] == "low"])
        high_pulse_count += len([pulse for pulse in pulses if pulse[1] == "high"])

    return low_pulse_count * high_pulse_count


def part2(input: str) -> int:
    raise Exception("Not implemented yet")
