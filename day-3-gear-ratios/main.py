# https://adventofcode.com/2023/day/3

# TL;DR:
# We'll iterate through the input file line by line and add it to a new 2D array which we also border with '.'.
#   For the first part of the problem where we have to sum all numbers next to a symbol:
#       - iterate through the 2D array and check if the current char is a symbol (except '.').
#       - if that's the case we check in all 8 directions (minus the ones we have already visited) for a digit
#       - if we find a digit that was not already visited we move to the left until we find a char that is not a digit (to find the first digit of the number)
#       - after finding the first digit of the number we move all the way to the right to build the full number and add each visited index to the visited_indices
#       - add the built number to the final answer and continue the iteration
#   For the second part where we have to sum the product of the exactly 2 numbers next to a '*' character:
#       - iterate through the 2D array and check if the current char is '*'
#       - if that's the case we check in all 8 directions (minus the ones we have already visited) for a digit
#       - if we find a digit that was not already visited we move to the left until we find a char that is not a digit (to find the first digit of the number)
#       - after finding the first digit of the number we move all the way to the right to build the full number and add each visited index to the visited_indices
#       - add the built number to a list of numbers
#       - after finishing checking for all 8 directions, if we have exactly 2 numbers in that list => multiply them and add the result to the final answer


# Complexities:
# Time => O(n * m * k), where n is the number of lines in the file, m is the length of each line and k is the median length of the numbers
# Space => O(n * m), where n is the number of lines in the file and m is the length of each line

DIRECTIONS = [
    [-1, 0],
    [-1, 1],
    [0, 1],
    [1, 1],
    [1, 0],
    [1, -1],
    [0, -1],
    [-1, -1]
]

# Part 1: The visual representation of an engine is represented by the sum of all numbers next to a symbol (except '.')
def findVisualRepresentationOfEngine():
    ans = 0
    aux = []

    with open("input.txt", "r") as file:
        for line in file:
            aux.append(['.'] + [*line[:-1]] + ['.'])

    border = ['.' for _ in range(len(aux[0]))]
    aux = [border] + aux + [border]

    for i in range(1, len(aux) - 1):
        for j in range(1, len(aux[i]) - 1):
            if not aux[i][j].isdigit() and aux[i][j] != '.':
                visited_indices = set()

                for dir in DIRECTIONS:
                    new_i = i + dir[0]
                    new_j = j + dir[1]

                    if str(new_i) + ':' + str(new_j) in visited_indices:
                        continue

                    if aux[new_i][new_j].isdigit():
                        while aux[new_i][new_j - 1].isdigit():
                            new_j -= 1

                        num = 0
                        while aux[new_i][new_j].isdigit():
                            visited_indices.add(str(new_i) + ':' + str(new_j))
                            num = num * 10 + int(aux[new_i][new_j])
                            new_j += 1

                        ans += num

    print(ans)

# To find the gear ratio we have to find all '*' symbols that have exactly 2 numbers next to it,
# calculate the product of these 2 numbers and add it to the final sum
def findGearRatio():
    ans = 0
    aux = []

    with open("input.txt", "r") as file:
        for line in file:
            aux.append(['.'] + [*line[:-1]] + ['.'])

    border = ['.' for _ in range(len(aux[0]))]
    aux = [border] + aux + [border]

    for i in range(1, len(aux) - 1):
        for j in range(1, len(aux[i]) - 1):
            if aux[i][j] == '*':
                visited_indices = set()
                nums = []
                for dir in DIRECTIONS:
                    new_i = i + dir[0]
                    new_j = j + dir[1]

                    if str(new_i) + ':' + str(new_j) in visited_indices:
                        continue

                    if aux[new_i][new_j].isdigit():
                        while aux[new_i][new_j - 1].isdigit():
                            new_j -= 1

                        num = 0
                        while aux[new_i][new_j].isdigit():
                            visited_indices.add(str(new_i) + ':' + str(new_j))
                            num = num * 10 + int(aux[new_i][new_j])
                            new_j += 1

                        nums.append(num)

                if len(nums) == 2:
                    ans += nums[0] * nums[1]

    print(ans)

findVisualRepresentationOfEngine()
findGearRatio()