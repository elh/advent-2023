from typing import Any


def parse_input(input: str) -> list[list[int]]:
    return [[int(char) for char in line] for line in input.split("\n")]


def print_grid(grid: list[list[Any]]) -> None:
    for row in grid:
        print(" ".join(["∞" if char == float("inf") else str(char) for char in row]))


Loc = tuple[int, int]  # (y, x)
Dir = tuple[int, int]  # (dy, dx) where dy, dx ∈ {-1, 0, 1}
Pos = tuple[Dir, int]  # (dir, steps) where steps is # of steps in current dir
State = tuple[Loc, Pos]


def print_distances(distances: list[list[dict[Pos, int | float]]]) -> None:
    for row in distances:
        for d in row:
            m = min(d.values()) if len(d) > 0 else float("inf")
            print(m if m != float("inf") else "∞", end=" ")
        print()


def shortest_path(
    grid: list[list[int]],
    min_steps_in_dir: int | None,
    max_steps_in_dir: int | None,
) -> int:
    # seed 2 starting squares. this avoids complications with turning from (0,0)
    # 2d grid of dicts from Pos to dijkstra distance
    distances: list[list[dict[Pos, int | float]]] = [
        [{} for _ in range(len(grid[0]))] for _ in range(len(grid))
    ]
    distances[0][1] = {((0, 1), 1): grid[0][1]}
    distances[1][0] = {((1, 0), 1): grid[1][0]}
    # pprint.pprint(distances)

    # visited: set[State] = set()
    fringe: list[State] = [
        ((0, 1), ((0, 1), 1)),
        ((1, 0), ((1, 0), 1)),
    ]
    while fringe:
        # pop from the front for BFS. conservative
        # TODO: A*?
        cur_state = fringe.pop(0)
        # print("popped:", cur_state)
        # print_distances(distances)
        (y, x), cur_pos = cur_state
        (prev_dy, prev_dx), step_count = cur_pos

        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_y, new_x = y + dy, x + dx
            next_step_count = step_count + 1 if (dy, dx) == (prev_dy, prev_dx) else 1
            next_pos = (
                (dy, dx),
                next_step_count,
            )
            next_state = ((new_y, new_x), next_pos)

            # disallow walking off the grid
            if not (0 <= new_y < len(grid)) or not 0 <= new_x < len(grid[0]):
                continue
            # disallow reversal
            if (dy, dx) == (-prev_dy, -prev_dx):
                continue
            # disallow current dir if greater than max_steps_in_dir
            if max_steps_in_dir is not None:
                if (dy, dx) == (
                    prev_dy,
                    prev_dx,
                ) and next_step_count > max_steps_in_dir:
                    continue
            # disallow changing dir if less than min_steps_in_dir
            if min_steps_in_dir is not None:
                if (dy, dx) != (
                    prev_dy,
                    prev_dx,
                ) and step_count < min_steps_in_dir:
                    continue

            # do not add to fringe if child distance did not improve distances
            prior = (
                distances[new_y][new_x][next_pos]
                if next_pos in distances[new_y][new_x]
                else float("inf")
            )
            distances[new_y][new_x][next_pos] = min(
                prior,
                distances[y][x][cur_pos] + grid[new_y][new_x],
            )
            if distances[new_y][new_x][next_pos] == prior:
                continue

            # TODO: not sure when to skip in this bastardized dijkstra's
            # dedupe
            # if next_state in visited:
            #     continue
            # visited.add(next_state)
            fringe.append(next_state)

    return int(min(distances[-1][-1].values()))


def part1(input: str) -> int:
    grid = parse_input(input)
    return shortest_path(grid, None, 3)


def part2(input: str) -> int:
    grid = parse_input(input)
    return shortest_path(grid, 4, 10)
