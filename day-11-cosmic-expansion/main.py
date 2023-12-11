# https://adventofcode.com/2023/day/11

# TL;DR:
# Extract the input from the file and map to the needed format:
#   - find all empty rows index and empty columns index (the ones that don't contain '#')
#   - find all galaxies ('#') and add their positions to a list
#   - iterate through the galaxies taken in pairs and find their paths (all tiles that we pass when going from one to the other)
#       - to find this path first we have to tell which direction we have to move when going from the first galaxy to the second
#       - after we find the direction (both vertical/horizontal axis) we start from the first galaxy and move to the second galaxy according to the found direction
#       -  whenever we modify the current position we append it to the path array
#   - get the length of the path array and for each element in path that went through an empty row or column we add the expansion number accordingly:
#       - 1 for the first part where the empty rows and columns double in size
#       - 1_000_000 - 1 for the second part where each empty row and column increase by 1_000_000


# Complexities:
# Time => O(n * m * p^2), where n is the number of lines, m the number of columns and p the number of galaxies
# Space => O(n * m), where n is the number of lines and m the number of columns


def find_empty_rows(grid):
    return [i for i, row in enumerate(grid) if '#' not in row]


def find_empty_columns(grid):
    empty_columns = [j for j in range(len(grid[0]))]
    for row in grid:
        for j, column in enumerate(row):
            if column == '#':
                if j in empty_columns:
                    empty_columns.remove(j)

    return empty_columns


def find_galaxies(grid):
    galaxies = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '#':
                galaxies.append((i, j))

    return galaxies


def find_direction_between_two_galaxies(this_galaxy, other_galaxy):
    direction = {
        'VERTICAL': None,
        'HORIZONTAL': None,
    }

    if this_galaxy[0] < other_galaxy[0]:
        direction['VERTICAL'] = 'DOWN'
    elif this_galaxy[0] > other_galaxy[0]:
        direction['VERTICAL'] = 'UP'
    else:
        direction['VERTICAL'] = 'EQUAL'

    if this_galaxy[1] < other_galaxy[1]:
        direction['HORIZONTAL'] = 'RIGHT'
    elif this_galaxy[1] > other_galaxy[1]:
        direction['HORIZONTAL'] = 'LEFT'
    else:
        direction['HORIZONTAL'] = 'EQUAL'

    return direction


def find_path_between_two_galaxies(this_galaxy, other_galaxy):
    direction = find_direction_between_two_galaxies(this_galaxy, other_galaxy)

    path = []
    position = this_galaxy
    while position != other_galaxy:
        while position[0] != other_galaxy[0]:
            if direction['VERTICAL'] == 'UP':
                position = (position[0] - 1, position[1])
            elif direction['VERTICAL'] == 'DOWN':
                position = (position[0] + 1, position[1])
            path.append(position)

        while position[1] != other_galaxy[1]:
            if direction['HORIZONTAL'] == 'RIGHT':
                position = (position[0], position[1] + 1)
            elif direction['HORIZONTAL'] == 'LEFT':
                position = (position[0], position[1] - 1)
            path.append(position)

    return path


def solve(expand_number = 1):
    with open("input.txt", 'r') as file:
        grid = [list(line.replace("\n", "")) for line in file]

        empty_rows = find_empty_rows(grid)
        empty_columns = find_empty_columns(grid)

        galaxies = find_galaxies(grid)
        ans = 0
        for i in range(len(galaxies) - 1):
            for j in range(i + 1, len(galaxies)):
                path = find_path_between_two_galaxies(galaxies[i], galaxies[j])
                length = len(path)
                for tile in path:
                    if tile[0] in empty_rows or tile[1] in empty_columns:
                        length += expand_number

                ans += length

        print(ans)


# Part 1
solve(expand_number=1)

# Part 2
solve(expand_number=999999)