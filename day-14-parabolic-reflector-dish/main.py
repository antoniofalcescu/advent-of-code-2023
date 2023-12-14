# https://adventofcode.com/2023/day/14

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For the first part of the problem where we have to find the total load of the stones rolled to the north:
#       - will zip the matrix so that we transpose our grid for ease of use when iterating
#       - iterate through each element of matrix and check if it's a O' stone:
#           - if that is the case => move the stone to the left until we reach an obstacle (another 'O' or '#' stone)
#       - after finishing moving all 'O' stones calculate the load of each (rows - row of stone)
#   For the second part where we have to find all winning possibilities the total load of the stones rolled to each direction after 1_000_000_000 iterations:
#       - use the same logic as in step 1 but for each direction not only north
#       - we'll keep a cache with already seen grid and an array of grids
#       - use this cache set to check if the current grid cycle was already seen
#       - get the offset of the first N different grids and the cycle_length of the grids
#       - use these values to get from our array the [(1_000_000_000 - offset) % cycle_length + offset] element
#       - calculate the total load for this grid


# Complexities:
# For part 1:
#   Time => O(n * m * max(log N, log M)), where n is the number of rows and m the number of columns
#   Space => O(n * m), where n is the number of rows and m the number of columns
# For part 2:
#   Time => O(n * m * max(log N, log M)), where n is the number of rows and m the number of columns
#   Space => O(n * m * x), where n is the number of rows, m the number of columns and x the length of the cycle in our array

def roll_stones(grid):
    for row in grid:
        for j in range(1, len(row)):
            if row[j] == 'O':
                k = j - 1
                j_aux = j
                while k >= 0 and row[k] == '.':
                    row[j_aux] = '.'
                    row[k] = 'O'
                    k -= 1
                    j_aux -= 1

    return grid


def tilt_grid_north(grid):
    transpose_grid = [list(g) for g in zip(*grid)]

    transpose_grid = roll_stones(transpose_grid)

    grid = [list(g) for g in zip(*transpose_grid)]
    return grid


def tilt_grid_south(grid):
    transpose_grid = [list(g)[::-1] for g in zip(*grid)]

    transpose_grid = roll_stones(transpose_grid)

    grid = [list(g) for g in zip(*transpose_grid)][::-1]
    return grid


def tilt_grid_west(grid):
    grid = roll_stones(grid)
    return grid


def tilt_grid_east(grid):
    grid = [g[::-1] for g in grid]

    grid = roll_stones(grid)

    grid = [g[::-1] for g in grid]
    return grid


def count_load(grid):
    total_load = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'O':
                total_load += len(grid) - i

    return total_load


def get_hashable_grid(grid):
    hashable_grid = tuple(tuple(g) for g in grid)
    return hashable_grid


def find_total_load_north():
    with open("input.txt", "r") as file:
        grid = file.read().splitlines()
        grid = [list(g) for g in grid]

        grid = tilt_grid_north(grid)

        load = count_load(grid)
        print(load)


def find_total_load_cycles():
    with open("input.txt", "r") as file:
        grid = file.read().splitlines()
        grid = [list(g) for g in grid]

        seen = set(get_hashable_grid(grid))
        grids = [get_hashable_grid(grid)]

        i = 0
        while True:
            i += 1

            grid = tilt_grid_north(grid)
            grid = tilt_grid_west(grid)
            grid = tilt_grid_south(grid)
            grid = tilt_grid_east(grid)

            hashable_grid = get_hashable_grid(grid)
            if hashable_grid in seen:
                break
            seen.add(hashable_grid)
            grids.append(hashable_grid)

        offset = grids.index(hashable_grid)
        cycle_length = i - offset
        grid = grids[(1000000000 - offset) % cycle_length + offset]

        load = count_load(grid)
        print(load)

find_total_load_north()
find_total_load_cycles()