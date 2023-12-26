import json


def parse_input(input: str) -> dict[str, list[str]]:
    lines = input.split("\n")
    d = {}
    for line in lines:
        parts = line.split(": ")
        d[parts[0]] = parts[1].split(" ")

    # populate all missing to_nodes and back pointers
    out: dict[str, list[str]] = {}
    for from_node, to_nodes in d.items():
        if from_node not in out:
            out[from_node] = []
        for to_node in to_nodes:
            if to_node not in out:
                out[to_node] = []
            if to_node not in out[from_node]:
                out[from_node].append(to_node)
            if from_node not in out[to_node]:
                out[to_node].append(from_node)

    return out


def graph_size(edges: dict[str, list[str]], member: str) -> int:
    s = {member}
    fringe = [member]
    while fringe:
        node = fringe.pop()
        for neighbor in edges[node]:
            if neighbor not in s:
                s.add(neighbor)
                fringe.append(neighbor)
    return len(s)


# use day25_graphviz.py to find the 3 edges that connect the subgraphs via graph viz.
# the 3 edges should be described in a file called ignore/25_three_wires.json and
# identify the edges in this format:
# [
#     ["aaa", "bbb"],
#     ["ccc", "ddd"],
#     ["eee", "fff"],
# ]
def part1(input: str) -> int:
    # read remove_edges from the json file
    FILE_NAME = "ignore/25_three_wires.json"
    with open(FILE_NAME) as f:
        remove_edges = json.load(f)

    edges = parse_input(input)
    for remove_edge in remove_edges:
        edges[remove_edge[0]].remove(remove_edge[1])
        edges[remove_edge[1]].remove(remove_edge[0])

    return graph_size(edges, remove_edges[0][0]) * graph_size(edges, remove_edges[0][1])


def part2(input: str) -> int:
    raise Exception("Not implemented yet")
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
