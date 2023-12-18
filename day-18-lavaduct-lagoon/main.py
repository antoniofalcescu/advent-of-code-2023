# https://adventofcode.com/2023/day/18

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For both parts of the problem we'll use the combination of Shoelace Formula with Pick's Theorem:
#   https://en.wikipedia.org/wiki/Shoelace_formula  https://en.wikipedia.org/wiki/Pick%27s_theorem
#       - for each instruction we'll update our polygon points (by appending a new point based on the previous last point and the instruction direction and steps)
#       - we'll also keep track of the number of boundary points by adding the number of steps of each instruction
#       - apply Shoelace Formula on the polygon points to get the area
#       - apply Pick's Theorem on the area and the number of boundary points to get the number of points inside the polygon
#       - sum up the boundary points and the inside points to get the total points which is the answer


# Complexities:
# Time => O(n), where n is the number of instructions (corner points of our polygon)
# Space => O(n), where n is the number of instructions (corner points of our polygon)


DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def shoelace_formula(polygon_points):
    area = 0
    for i in range(len(polygon_points)):
        aux = polygon_points[i][0] * (polygon_points[i - 1][1] - polygon_points[(i + 1) % len(polygon_points)][1])
        area += aux

    return abs(area) // 2


def pick_theorem(area, number_of_boundary_points):
    return area - number_of_boundary_points // 2 + 1


def find_number_of_cubic_metres_of_lava():
    with open("input.txt", "r") as file:
        number_of_boundary_points = 0
        polygon_points = [(0, 0)]
        for line in file:
            line = line.split()
            direction, steps = line[0], int(line[1])
            mv_i, mv_j = DIRECTIONS[direction]

            number_of_boundary_points += steps
            i, j = polygon_points[-1]
            polygon_points.append((i + mv_i * steps, j + mv_j * steps))


        area = shoelace_formula(polygon_points)
        number_of_inside_points = pick_theorem(area, number_of_boundary_points)
        ans = number_of_boundary_points + number_of_inside_points
        print(ans)


def parse_color(color):
    hex_number = color[1:len(color) - 1]
    direction_id = color[len(color) - 1]

    steps = int(hex_number, 16)
    direction = ''
    if direction_id == '0':
        direction = 'R'
    elif direction_id == '1':
        direction = 'D'
    elif direction_id == '2':
        direction = 'L'
    elif direction_id == '3':
        direction = 'U'

    return direction, steps


def find_number_of_cubic_metres_of_lava_large_numbers():
    with open("input.txt", "r") as file:
        number_of_boundary_points = 0
        polygon_points = [(0, 0)]
        for line in file:
            line = line.split()
            color = line[2][1:len(line[2]) - 1]
            direction, steps = parse_color(color)
            mv_i, mv_j = DIRECTIONS[direction]

            number_of_boundary_points += steps
            i, j = polygon_points[-1]
            polygon_points.append((i + mv_i * steps, j + mv_j * steps))

        area = shoelace_formula(polygon_points)
        number_of_inside_points = pick_theorem(area, number_of_boundary_points)
        ans = number_of_boundary_points + number_of_inside_points
        print(ans)


find_number_of_cubic_metres_of_lava()
find_number_of_cubic_metres_of_lava_large_numbers()