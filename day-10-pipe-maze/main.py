# https://adventofcode.com/2023/day/10

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For both parts:
#       - border the matrix of pipes with '.' character
#       - find the start position of S
#       - find the pipe type of S and replace it with the found type
#   For the first part of the problem where we have to find the farthest pipe in the loop from the start:
#       - use a BFS with a queue and a seen set to find the loop
#       - return the seen array with positions and print the length // 2 to find the farthest distance
#   For the second part where we have to find all points that are enclosed in our pipe loop:
#       - use the previous BFS to find the pipe loop
#       - replace unused pipes (pipes that are not part of the loop - that's why we need the pipe loop from the BFS -) with '.'
#       - find points inside our loop with Even-Odd Rule https://en.wikipedia.org/wiki/Even–odd_rule#
#           (iterate through each line and count the number of appearances of "walls" from our loop e.g. L,J,|
#       - if the number of passed walls is odd => the current character is inside the loop so we add it to our inside set
#       - return the set and print it's length to find the total number


# Complexities:
# Time => O(n * m), where n is the number of lines and m the number of columns
# Space => O(n * m), where n is the number of lines and m the number of columns

from collections import deque

DIRECTIONS = {
    'UP': [-1, 0],
    'RIGHT': [0, 1],
    'DOWN': [1, 0],
    'LEFT': [0, -1]
}

PIPE_TYPES = {
    '|': {
        'UP': ['|', '7', 'F'],
        'RIGHT': [],
        'DOWN': ['|', 'L', 'J'],
        'LEFT': [],
    },
    '-': {
        'UP': [],
        'RIGHT': ['-', '7', 'J'],
        'DOWN': [],
        'LEFT': ['-', 'L', 'F'],
    },
    'L': {
        'UP': ['|', '7', 'F'],
        'RIGHT': ['-', '7', 'J'],
        'DOWN': [],
        'LEFT': [],
    },
    'J': {
        'UP': ['|', '7', 'F'],
        'RIGHT': [],
        'DOWN': [],
        'LEFT': ['-', 'F', 'L'],
    },
    '7': {
        'UP': [],
        'RIGHT': [],
        'DOWN': ['|', 'L', 'J'],
        'LEFT': ['-', 'L', 'F'],
    },
    'F': {
        'UP': [],
        'RIGHT': ['-', 'J', '7'],
        'DOWN': ['|', 'L', 'J'],
        'LEFT': [],
    },
}


def find_start_position(pipes):
    for i in range(len(pipes)):
        if 'S' in pipes[i]:
            return [i, pipes[i].index('S')]


def border_matrix(pipes):
    pipes.insert(0, ['.'] * len(pipes[0]))
    pipes.append(['.'] * len(pipes[0]))

    for i in range(len(pipes)):
        pipes[i].insert(0, '.')
        pipes[i].append('.')


def modify_start_pipe(pipes, start_position):
    neighbors = []
    for direction in DIRECTIONS:
        position = [start_position[0] + DIRECTIONS[direction][0], start_position[1] + DIRECTIONS[direction][1]]
        neighbors.append([direction, pipes[position[0]][position[1]]])

    for pipe in PIPE_TYPES:
        for i in range(len(neighbors) - 1):
            for j in range(i + 1, len(neighbors)):
                if (neighbors[i][1] in PIPE_TYPES[pipe][neighbors[i][0]]
                        and neighbors[j][1] in PIPE_TYPES[pipe][neighbors[j][0]]):
                    pipes[start_position[0]][start_position[1]] = pipe
                    return


def find_pipe_loop(pipes, start_position):
    pipe_loop = {(start_position[0], start_position[1])}
    q = deque([(start_position[0], start_position[1])])

    while q:
        i, j = q.popleft()
        pipe = pipes[i][j]

        for direction in DIRECTIONS:
            new_position = (i + DIRECTIONS[direction][0], j + DIRECTIONS[direction][1])
            if new_position in pipe_loop:
                continue

            if pipes[new_position[0]][new_position[1]] in PIPE_TYPES[pipe][direction]:
                pipe_loop.add(new_position)
                q.append(new_position)

    return pipe_loop


def find_farthest_pipe_in_loop():
    with open("input.txt", "r") as file:
        pipes = [[*line.replace('\n', '')] for line in file]
        border_matrix(pipes)
        start_position = find_start_position(pipes)
        modify_start_pipe(pipes, start_position)
        pipe_loop = find_pipe_loop(pipes, start_position)

        print(len(pipe_loop) // 2)


def replace_unused_pipes(pipes, pipe_loop):
    for i in range(len(pipes)):
        for j in range(len(pipes[i])):
            if (i, j) not in pipe_loop:
                pipes[i][j] = '.'


def find_inside_characters(pipes):
    inside = set()

    for i in range(len(pipes)):
        count = 0
        for j in range(len(pipes[i])):
            tile = pipes[i][j]
            if tile in "|LJ":
                count += 1
            elif tile == '.':
                if count % 2 != 0:
                    inside.add((i, j))
    return inside


def find_number_of_inside_characters():
    with open("input.txt", "r") as file:
        pipes = [[*line.replace('\n', '')] for line in file]
        border_matrix(pipes)
        start_position = find_start_position(pipes)
        modify_start_pipe(pipes, start_position)
        pipe_loop = find_pipe_loop(pipes, start_position)

        replace_unused_pipes(pipes, pipe_loop)
        inside = find_inside_characters(pipes)
        print(len(inside))


find_farthest_pipe_in_loop()
find_number_of_inside_characters()
