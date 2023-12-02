import importlib
import json


# Usage: python all.py
#
# Runs all solutions in the stype of `main.py` and checks with answers present
# in `answers.json`.
def main():
    for day in range(1, 26):
        print("Day " + str(day) + ":\t", end="")
        for part in range(1, 3):
            try:
                module = importlib.import_module("solutions.day" + str(day))
                fn = getattr(module, "part" + str(part))
                input_file = "inputs/" + str(day) + ".txt"
                input = open(input_file, "r").read().rstrip("\n")
                got = fn(input)
            except Exception:
                print("-", end=" ")
                continue

            try:
                answers = json.load(open("answers.json", "r"))
                expected = answers[str(day) + "." + str(part)]
                if str(got) == str(expected):
                    print("✓", end=" ")
                else:
                    print("x", end=" ")
            except Exception:
                print("?", end=" ")

        print()


if __name__ == "__main__":
    main()
