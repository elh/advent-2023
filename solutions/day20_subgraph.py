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
    subgraph = day20.extract_subgraph(modules, args.parent)

    count = 0
    while True:
        count += 1
        if count > MAX_ITERATIONS:
            print("too many iterations", MAX_ITERATIONS)
            break
        pulses = day20.press_button(subgraph)
        for pulse in pulses:
            if pulse[1] == "low" and pulse[2] == "rx":
                print("rx for a low pulse!", count)
                break


if __name__ == "__main__":
    main()
