import argparse
import importlib
import json
import time

GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"


# prec determines the decimal place precision
def rounded(v: float, prec: int = 10000) -> float:
    return int(v * prec) / prec


def parse_skips(skip: str) -> set:
    skips = set()
    for part in skip.split(","):
        day, part = part.split(".")
        skips.add((int(day), int(part)))
    return skips


# Usage: python all.py [--skip <skip>]
#
# Runs all solutions in the stype of `main.py` and checks with answers present
# in `answers.json`. --skip is an optional csv of parts to skip. parts are
# represented as <day>.<part>, e.g. 1.1, 25.2
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip",
        help="csv of parts to skip. parts are represented as <day>.<part>, e.g. 1.1",
    )
    parser.add_argument("--stats", help="if enabed, emit summary statistics")
    args = parser.parse_args()

    skips = parse_skips(args.skip) if args.skip else set()

    total_dur = 0
    all_durs = {}
    counts = {
        "✓": 0,  # Correct
        "x": 0,  # Incorrect
        "?": 0,  # No answer provided
        "-": 0,  # Unimplemented
        "s": 0,  # Skipped
    }
    for day in range(1, 26):
        print("Day " + str(day) + ":\t", end="")
        durs = []
        for part in range(1, 3):
            if (day, part) in skips:
                print("s", end=" ")
                counts["s"] += 1
                durs.append(None)
                continue

            try:
                module = importlib.import_module("solutions.day" + str(day).zfill(2))
                fn = getattr(module, "part" + str(part))
                input_file = "inputs/" + str(day).zfill(2) + ".txt"
                input = open(input_file, "r").read().rstrip("\n")
            except Exception:
                print("-", end=" ")
                counts["-"] += 1
                durs.append(None)
                continue

            try:
                start_t = time.time()
                got = fn(input)
                durs.append(rounded(time.time() - start_t))
            except Exception:
                print(RED + "x" + ENDC, end=" ")
                counts["x"] += 1
                durs.append(rounded(time.time() - start_t))
                continue

            try:
                answers = json.load(open("answers.json", "r"))
                expected = answers[str(day) + "." + str(part)]
                if str(got) == str(expected):
                    print(GREEN + "✓" + ENDC, end=" ")
                    counts["✓"] += 1
                else:
                    print(RED + "x" + ENDC, end=" ")
                    counts["x"] += 1
            except Exception:
                print("?", end=" ")
                counts["?"] += 1
        all_durs[day] = {}
        for i, dur in enumerate(durs):
            if dur is not None:
                total_dur += dur
                all_durs[day][i + 1] = dur
        print("\t", durs, end="")
        print()
    print("\nResults:", ", ".join([str(v) + " " + k for k, v in counts.items()]))
    print("Total time (s):", rounded(total_dur))

    if args.stats:
        print()
        for day in range(1, 26):
            print("Day " + str(day), end="")
            for part in range(1, 3):
                if part in all_durs[day]:
                    print(
                        "\t",
                        rounded((all_durs[day][part] / total_dur) * 100, prec=100),
                        end="",
                    )
            print()


if __name__ == "__main__":
    main()
