import argparse

def main(input):
    total = 0
    lines = input.split("\n")
    for line in lines:
        first, last = None, None
        for i in range(len(line)):
            if not line[i].isdigit():
                continue
            if first is None:
                first = i
            last = i
        value = int(line[first] + line[last])
        total += value
    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    f = open(args.input_file, "r")
    input = f.read().rstrip("\n")
    main(input)
