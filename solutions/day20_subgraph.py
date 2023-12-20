import day20
import argparse

MAX_ITERATIONS = 100000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input file")
    parser.add_argument(
        "parent", help='only "broadcaster", parent, and its children will be kept'
    )
    args = parser.parse_args()

    input = open(args.input_file, "r").read().rstrip("\n")
    modules = day20.parse_modules(input)

    # cut out this subgraph
    keepers = {"broadcaster", args.parent}
    fringe = [args.parent]
    while fringe:
        name = fringe.pop()
        if name not in modules:
            continue
        for dest in modules[name]["dests"]:
            if dest not in keepers:
                keepers.add(dest)
                fringe.append(dest)

    for name in list(modules.keys()):
        if name not in keepers:
            del modules[name]

    for module in modules.values():
        module["dests"] = [dest for dest in module["dests"] if dest in keepers]
        if "remembered" in module:
            module["remembered"] = {
                k: v for k, v in module["remembered"].items() if k in keepers
            }

    count = 0
    while True:
        count += 1
        if count > MAX_ITERATIONS:
            print("too many iterations", MAX_ITERATIONS)
            break
        pulses = day20.press_button(modules)
        for pulse in pulses:
            if pulse[1] == "low" and pulse[2] == "rx":
                print("rx for a low pulse!", count)
                break


if __name__ == "__main__":
    main()
