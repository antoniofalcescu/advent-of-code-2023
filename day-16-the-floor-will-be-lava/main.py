# https://adventofcode.com/2023/day/16

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For both parts of the problem we'll use an algorithm based on BFS:
#       - given a starting position and a direction we'll move accordingly with an array of directions
#       - if we encounter any special character (mirror or split characters) we'll change directions as the problem's requirements specify
#       -  we'll store in our seen/queue data structures the current position and direction in the following format:
#           - (row_index, column_index, direction) =>  this allows us to easily check if the same beam passes through a visited tile by checking if both the position and direction are the same
#       - at last return a new energized set that contains all uniquely visited elements not taking in account the direction
#   For the second part where we have to find the maximum possible number of energized tiles:
#       - starting from each tile on the first/last row and the first/last column:
#           - brute force with the same algorithm and store inside a max_energized variable the maximum value


# Complexities:
# For part 1:
#   Time => O(n * m), where n * m is the size of the matrix
#   Space => O(n * m * 4) = O(n * m), where n * m is the size of the matrix and 4 is the 4 possible direction
# For part 2:
#   Time => O(n * m * max(n, m)), where n * m is the size of the matrix
#   Space => O(n * m * 4) = O(n * m), where n * m is the size of the matrix and 4 is the 4 possible direction


from collections import deque

DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}


def find_energized_tiles(grid, start):
    start = [start]
    seen = set()
    q = deque(start)

    while q:
        (i, j, direction) = q.popleft()
        i, j = (i + DIRECTIONS[direction][0], j + DIRECTIONS[direction][1])

        if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
            ch = grid[i][j]

            if ch == '.' or (ch == '-' and direction in ['LEFT', 'RIGHT']) or (ch == '|' and direction in ['UP', 'DOWN']):
                if (i, j, direction) not in seen:
                    seen.add((i, j, direction))
                    q.append((i, j, direction))
            elif ch == '/':
                if direction == 'UP':
                    direction = 'RIGHT'
                elif direction == 'DOWN':
                    direction = 'LEFT'
                elif direction == 'RIGHT':
                    direction = 'UP'
                elif direction == 'LEFT':
                    direction = 'DOWN'

                if (i, j, direction) not in seen:
                    seen.add((i, j, direction))
                    q.append((i, j, direction))
            elif ch == '\\':
                if direction == 'UP':
                    direction = 'LEFT'
                elif direction == 'DOWN':
                    direction = 'RIGHT'
                elif direction == 'RIGHT':
                    direction = 'DOWN'
                elif direction == 'LEFT':
                    direction = 'UP'

                if (i, j, direction) not in seen:
                    seen.add((i, j, direction))
                    q.append((i, j, direction))
            elif ch == '|' and direction in ['LEFT', 'RIGHT']:
                for direction in ['UP', 'DOWN']:
                    if (i, j, direction) not in seen:
                        seen.add((i, j, direction))
                        q.append((i, j, direction))
            elif ch == '-' and direction in ['UP', 'DOWN']:
                for direction in ['LEFT', 'RIGHT']:
                    if (i, j, direction) not in seen:
                        seen.add((i, j, direction))
                        q.append((i, j, direction))

    energized = {(i, j) for (i, j, _) in seen}
    return energized


def find_number_of_energized_tiles():
    with open("input.txt", "r") as file:
        grid = file.read().splitlines()
        energized = find_energized_tiles(grid, (0, -1, 'RIGHT'))

        print(len(energized))


def find_max_number_of_energized_tiles():
    with open("input.txt", "r") as file:
        grid = file.read().splitlines()

        max_energized = 0
        for i in range(len(grid)):
            energized_from_left = len(find_energized_tiles(grid, (i, -1, 'RIGHT')))
            energized_from_right = len(find_energized_tiles(grid, (i, len(grid[i]), 'LEFT')))
            max_energized = max(max_energized, energized_from_left, energized_from_right)

        for j in range(len(grid[0])):
            energized_from_top = len(find_energized_tiles(grid, (-1, j, 'DOWN')))
            energized_from_bottom = len(find_energized_tiles(grid, (len(grid), j, 'UP')))
            max_energized = max(max_energized, energized_from_top, energized_from_bottom)

        print(max_energized)


find_number_of_energized_tiles()
find_max_number_of_energized_tiles()
