import argparse

word_ints = [
    ("one", 1), ("two", 2), ("three", 3),
    ("four", 4), ("five", 5), ("six", 6),
    ("seven", 7), ("eight", 8), ("nine", 9)
]

def get_first_int(line: str, reverse: bool = False) -> int:
    line = line[::-1] if reverse else line
    for i in range(len(line)):
        if line[i].isdigit():
            return int(line[i])
        for word, value in word_ints:
            if line[i:].startswith(word if not reverse else word[::-1]):
                return value

def main(input: str) -> int:
    total = 0
    for line in input.split("\n"):
        total += int(str(get_first_int(line)) + str(get_first_int(line, reverse=True)))
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    f = open(args.input_file, "r")
    input = f.read().rstrip("\n")
    print(main(input))
