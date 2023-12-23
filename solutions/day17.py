from typing import Any
import heapq

Loc = tuple[int, int]  # (y, x)
Dir = tuple[int, int]  # (dy, dx) where dy, dx ∈ {-1, 0, 1}
Pos = tuple[Dir, int]  # (dir, steps) where steps is # of steps in current dir
State = tuple[Loc, Pos]


def parse_input(input: str) -> list[list[int]]:
    return [[int(char) for char in line] for line in input.split("\n")]


def print_distances(distances: list[list[dict[Pos, int | float]]]) -> None:
    for row in distances:
        for d in row:
            m = min(d.values()) if len(d) > 0 else float("inf")
            print(m if m != float("inf") else "∞", end=" ")
        print()


def manhattan(loc1: Loc, loc2: Loc) -> int:
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


def shortest_path(
    grid: list[list[int]],
    min_steps_in_dir: int | None,
    max_steps_in_dir: int | None,
) -> int:
    end_loc = (len(grid) - 1, len(grid[0]) - 1)

    # seed 2 starting squares. this avoids complications with turning from (0,0)
    # 2d grid of dicts from Pos to dijkstra distance
    distances: list[list[dict[Pos, int | float]]] = [
        [{} for _ in range(len(grid[0]))] for _ in range(len(grid))
    ]
    distances[0][1] = {((0, 1), 1): grid[0][1]}
    distances[1][0] = {((1, 0), 1): grid[1][0]}

    # TODO: perf: skip visited states. unclear if states can be skipped
    fringe: list[Any] = []  # a list of State. mypy not happy with heapq
    heapq.heappush(
        fringe,
        (grid[0][1] + manhattan((0, 1), end_loc), ((0, 1), ((0, 1), 1))),
    )
    heapq.heappush(
        fringe,
        (grid[1][0] + manhattan((1, 0), end_loc), ((1, 0), ((1, 0), 1))),
    )

    while fringe:
        _, cur_state = heapq.heappop(fringe)
        # print("popped:", cur_state)
        # print_distances(distances)
        (y, x), cur_pos = cur_state
        (prev_dy, prev_dx), step_count = cur_pos

        # reached end
        if y == len(grid) - 1 and x == len(grid[0]) - 1:
            break

        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_y, new_x = y + dy, x + dx
            next_step_count = step_count + 1 if (dy, dx) == (prev_dy, prev_dx) else 1
            next_pos = ((dy, dx), next_step_count)
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
            new_distance = distances[y][x][cur_pos] + grid[new_y][new_x]
            prior_distance = (
                distances[new_y][new_x][next_pos]
                if next_pos in distances[new_y][new_x]
                else float("inf")
            )
            distances[new_y][new_x][next_pos] = min(prior_distance, new_distance)
            if distances[new_y][new_x][next_pos] == prior_distance:
                continue

            heapq.heappush(
                fringe, (new_distance + manhattan((new_y, new_x), end_loc), next_state)
            )

    # print_distances(distances)
    return int(min(distances[end_loc[0]][end_loc[1]].values()))


def part1(input: str) -> int:
    grid = parse_input(input)
    return shortest_path(grid, None, 3)


def part2(input: str) -> int:
    grid = parse_input(input)
    return shortest_path(grid, 4, 10)
