import copy


def parse_input(input: str):
    grid = [[c for c in line] for line in input.split("\n")]
    start_loc = None
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c == "S":
                start_loc = (i, j)
                grid[i][j] = "."
    if start_loc is None:
        raise Exception("No start location found")
    return grid, start_loc


State = tuple[tuple[int, int], int]  # ((y, x), step_count)

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def print_grid(grid, locs):
    grid = copy.deepcopy(grid)
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if (i, j) in locs:
                print("O", end="")
            else:
                print(c, end="")
        print()


# The following layer functions all use the optimized new_layer_locs to allow
# for deduplication of locations to evaluate in the walk fringe. To actually get
# the full set of locations at a layer we check that layer and all same parity
# layers preceeding it in new_layer_locs
def get_all_locs(
    new_layer_locs: dict[int, set[tuple[int, int]]], layer: int
) -> set[tuple[int, int]]:
    locs = set()

    # union all sets iterating from layer backwards by step size 2
    for i in range(layer, -1, -2):
        locs |= new_layer_locs[i]
    return locs


def count_layer_locs(
    new_layer_locs: dict[int, set[tuple[int, int]]], layer: int
) -> int:
    # pprint.pprint({k: len(v) for k, v in new_layer_locs.items()})
    return sum([len(new_layer_locs[i]) for i in range(layer, -1, -2)])


def is_in_layer(
    new_layer_locs: dict[int, set[tuple[int, int]]], layer: int, loc: tuple[int, int]
) -> bool:
    for i in range(layer, -1, -2):
        if loc in new_layer_locs[i]:
            return True
    return False


def walk(
    grid: list[list[str]],
    start_loc: tuple[int, int],
    limit: int,
    print_final_grid: bool = False,
    print_all_grids: bool = False,
) -> int:
    seen_states: set[State] = set()
    # from layer number to newly seen locations in that layer
    # note: this will not include locations seen as previous layers of the same parity
    new_layer_locs: dict[int, set[tuple[int, int]]] = {}

    fringe: list[State] = [(start_loc, 0)]
    cur_layer = 0
    while fringe:
        cur = fringe.pop(0)
        if cur[1] > cur_layer:
            if print_all_grids:
                print_grid(grid, get_all_locs(new_layer_locs, cur_layer))
            cur_layer += 1
        new_layer_locs[cur_layer] = new_layer_locs.get(cur_layer, set()) | {cur[0]}

        if cur[1] >= limit:  # final layer
            continue

        for dir in dirs:
            new = (cur[0][0] + dir[0], cur[0][1] + dir[1])
            if (
                new[0] < 0
                or new[0] >= len(grid)
                or new[1] < 0
                or new[1] >= len(grid[0])
            ):
                continue
            if grid[new[0]][new[1]] == "#":
                continue

            if (new, cur[1] + 1) in seen_states:
                continue
            seen_states.add((new, cur[1] + 1))

            if is_in_layer(new_layer_locs, cur_layer - 1, new):
                continue

            fringe.append((new, cur[1] + 1))

    if print_final_grid:
        print_grid(grid, get_all_locs(new_layer_locs, cur_layer))

    return count_layer_locs(new_layer_locs, cur_layer)


def part1(input: str) -> int:
    grid, start_loc = parse_input(input)
    return walk(grid, start_loc, 64)


# see day21_notes.txt for rationale and terms
def part2(input: str) -> int:
    TARGET_STEPS = 26501365

    grid, _ = parse_input(input)
    grid_len = len(grid)
    if grid_len % 2 == 0:
        raise Exception("Grid length must be odd")
    # also the distance of center from edge of the first grid
    # if grid_len is 131, center_idx is 65
    center_idx = (grid_len - 1) // 2

    if (TARGET_STEPS - center_idx) % grid_len != 0:
        raise Exception("Target steps not a multiple of grid length minus half a grid")
    # not including the center square
    n_grid_units = (TARGET_STEPS - center_idx) // grid_len
    if n_grid_units % 2 != 0:
        # Could be supported but not bothering
        raise Exception("Number of grid units must be odd")

    # equation for even "grid unit" walks, the number of grid shapes covered:
    # n^2 odd-stepped "squares"
    # n * set of 4 odd-stepped "corners"
    # (n-1)^2 even-stepped "squares"
    # (n-1) * set of 4 even-stepped "chipped"
    # set of 4 even-stepped "houses"
    #
    # see day21_notes.txt
    odd_squares = pow(n_grid_units, 2) * walk(
        grid, (center_idx, center_idx), len(grid) - 1
    )
    odd_corners = n_grid_units * sum(
        [
            walk(grid, (0, 0), center_idx - 1),
            walk(grid, (0, grid_len - 1), center_idx - 1),
            walk(grid, (grid_len - 1, 0), center_idx - 1),
            walk(grid, (grid_len - 1, grid_len - 1), center_idx - 1),
        ]
    )
    even_squares = pow(n_grid_units - 1, 2) * walk(
        grid, (center_idx, center_idx), len(grid) - 2
    )
    even_chipped = (n_grid_units - 1) * sum(
        [
            walk(grid, (0, 0), grid_len + center_idx - 1),
            walk(grid, (0, grid_len - 1), grid_len + center_idx - 1),
            walk(grid, (grid_len - 1, 0), grid_len + center_idx - 1),
            walk(grid, (grid_len - 1, grid_len - 1), grid_len + center_idx - 1),
        ]
    )
    even_houses = sum(
        [
            walk(grid, (0, center_idx), grid_len - 1),
            walk(grid, (center_idx, grid_len - 1), grid_len - 1),
            walk(grid, (grid_len - 1, center_idx), grid_len - 1),
            walk(grid, (center_idx, 0), grid_len - 1),
        ]
    )

    return odd_squares + odd_corners + even_squares + even_chipped + even_houses
