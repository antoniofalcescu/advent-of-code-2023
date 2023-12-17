# https://adventofcode.com/2023/day/17

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For both parts we need to use a modified Djikstra's Algorithm:
#       - use a priority queue which has the push/pop value set as the heat_loss of each tile
#       - when moving forward (not changing the current direction) we need to check to not move too far (3 steps for p1, 10 for p2)
#       - when trying to change direction we need to check to move the direction only left or right (and for p2 if only we moved at least 4 steps)
#       - when we reach the element from the bottom right corner we print it and break from the while loop


# Complexities:
# Time => O(n * m * log(n * m)), where n * m is the size of the matrix
# Space => O(n * m), where n * m is the size of the matrix


from heapq import heappush, heappop

DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1),
    'STAND': (0, 0),
}


def find_min_heat_loss_for_crucible():
    with open("input.txt", "r") as file:
        grid = [list(map(int, line.strip())) for line in file]
        GRID_WIDTH = len(grid[0])
        GRID_HEIGHT = len(grid)

        seen = set()

        # heat_loss, i, j, direction, steps_in_direction
        pq = [(0, 0, 0, "STAND", 0)]
        while pq:
            heat_loss, i, j, direction, steps = heappop(pq)

            if i == GRID_HEIGHT - 1 and j == GRID_WIDTH - 1:
                print(heat_loss)
                break

            if i < 0 or i >= GRID_HEIGHT or j < 0 or j >= GRID_WIDTH:
                continue

            if (i, j, direction, steps) in seen:
                continue
            seen.add((i, j, direction, steps))

            if steps < 3 and direction != "STAND":
                new_i = i + DIRECTIONS[direction][0]
                new_j = j + DIRECTIONS[direction][1]

                if 0 <= new_i < GRID_HEIGHT and 0 <= new_j < GRID_WIDTH:
                    heappush(pq, (heat_loss + grid[new_i][new_j], new_i, new_j, direction, steps + 1))

            for possible_direction in DIRECTIONS:
                if direction == possible_direction or possible_direction == "STAND":
                    continue

                mv_i, mv_j = DIRECTIONS[direction]
                new_mv_i, new_mv_j = DIRECTIONS[possible_direction]

                if (new_mv_i, new_mv_j) != (-mv_i, -mv_j):
                    new_i = i + new_mv_i
                    new_j = j + new_mv_j

                    if 0 <= new_i < GRID_HEIGHT and 0 <= new_j < GRID_WIDTH:
                        heappush(pq, (heat_loss + grid[new_i][new_j], new_i, new_j, possible_direction, 1))


def find_min_heat_loss_for_ultra_crucible():
    with open("input.txt", "r") as file:
        grid = [list(map(int, line.strip())) for line in file]
        GRID_WIDTH = len(grid[0])
        GRID_HEIGHT = len(grid)

        seen = set()

        # heat_loss, i, j, direction, steps_in_direction
        pq = [(0, 0, 0, "STAND", 0)]
        while pq:
            heat_loss, i, j, direction, steps = heappop(pq)

            if i == GRID_HEIGHT - 1 and j == GRID_WIDTH - 1 and steps >= 4:
                print(heat_loss)
                break

            if i < 0 or i >= GRID_HEIGHT or j < 0 or j >= GRID_WIDTH:
                continue

            if (i, j, direction, steps) in seen:
                continue
            seen.add((i, j, direction, steps))

            if steps < 10 and direction != "STAND":
                new_i = i + DIRECTIONS[direction][0]
                new_j = j + DIRECTIONS[direction][1]

                if 0 <= new_i < GRID_HEIGHT and 0 <= new_j < GRID_WIDTH:
                    heappush(pq, (heat_loss + grid[new_i][new_j], new_i, new_j, direction, steps + 1))

            if steps >= 4 or direction == "STAND":
                for possible_direction in DIRECTIONS:
                    if direction == possible_direction or possible_direction == "STAND":
                        continue

                    mv_i, mv_j = DIRECTIONS[direction]
                    new_mv_i, new_mv_j = DIRECTIONS[possible_direction]

                    if (new_mv_i, new_mv_j) != (-mv_i, -mv_j):
                        new_i = i + new_mv_i
                        new_j = j + new_mv_j

                        if 0 <= new_i < GRID_HEIGHT and 0 <= new_j < GRID_WIDTH:
                            heappush(pq, (heat_loss + grid[new_i][new_j], new_i, new_j, possible_direction, 1))


find_min_heat_loss_for_crucible()
find_min_heat_loss_for_ultra_crucible()