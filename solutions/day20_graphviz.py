import day20
import argparse
import graphviz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input file")
    args = parser.parse_args()

    input = open(args.input_file, "r").read().rstrip("\n")
    modules = day20.parse_modules(input)

    dot = graphviz.Digraph(comment="Modules")
    for name, module in modules.items():
        # flip is red, conj is blue
        color = "black"
        if module["type"] == "flip":
            color = "red"
        elif module["type"] == "conj":
            color = "blue"
        dot.node(name, name, color=color)
        for dest in module["dests"]:
            dot.edge(name, dest)
    print(dot.source)


if __name__ == "__main__":
    main()
