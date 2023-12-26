import day25
import argparse
import graphviz

"""
python solutions/day25_graphviz.py inputs/25.txt > ignore/25.graphviz
dot -Tpng ignore/25.graphviz -Kneato > ignore/25_output.png
open ignore/25_output.png
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input file")
    args = parser.parse_args()

    input = open(args.input_file, "r").read().rstrip("\n")
    d = day25.parse_input(input)

    added_edges: set[tuple[str, str]] = set()

    dot = graphviz.Graph()
    for from_node, to_nodes in d.items():
        dot.node(from_node)
        for to_node in to_nodes:
            if (from_node, to_node) not in added_edges and (
                to_node,
                from_node,
            ) not in added_edges:
                dot.edge(from_node, to_node)
                added_edges.add((from_node, to_node))
    print(dot.source)


if __name__ == "__main__":
    main()
