import importlib
import json
import time

GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"


def rounded(v: float) -> float:
    return int(v * 10000) / 10000


# Usage: python all.py
#
# Runs all solutions in the stype of `main.py` and checks with answers present
# in `answers.json`.
def main():
    total_dur = 0
    counts = {
        "✓": 0,  # Correct
        "x": 0,  # Incorrect
        "?": 0,  # No answer provided
        "-": 0,  # Unimplemented
    }
    for day in range(1, 26):
        print("Day " + str(day) + ":\t", end="")
        durs = []
        for part in range(1, 3):
            try:
                module = importlib.import_module("solutions.day" + str(day))
                fn = getattr(module, "part" + str(part))
                input_file = "inputs/" + str(day) + ".txt"
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
        for dur in durs:
            if dur is not None:
                total_dur += dur
        print("\t", durs, end="")
        print()
    print("\nResults:", ", ".join([str(v) + " " + k for k, v in counts.items()]))
    print("Total time (s):", rounded(total_dur))


if __name__ == "__main__":
    main()
