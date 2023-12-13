# https://adventofcode.com/2023/day/13

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For the first part of the problem where we have to find the sum of the mirror index for all matrices:
#       - we'll use the same function for iterating through the lines and through the columns (by transposing the matrix)
#       - this method will do the following:
#           - iterate from the second line (because the mirror can only appear after [0, 1] line
#           - split the grid into 2 pieces based on our current index i
#           - flip the first piece so that this piece's first len(bottom_piece) elements will be at the top and the comparison between the 2 pieces will be easier
#           - take only the first N elements where N = min(len(bottom), len(top)) (note that in Python if we splice an array of length 3 with the value 10 we will get the initial array in full)
#           - if both pieces are equal => the current index is a mirroring line
#   For the second part where we have to find the sum of the mirror index for all matrices with offset of 1 element (smudge):
#       - repeat the process as in part 1 with the following changes:
#           - iterate line by line through both pieces and check if the line(string) has mismatches
#           - if we have found exactly 1 mismatch (our smudge) => current index is a mirroring line so return it


# Complexities:
# Time => O(n * max(a,b) ^ 2), where n is the number of matrices and a and b the number of lines/columns of each matrix
# Space => O(n * a * b), where n is the number of matrices and a and b the number of lines/columns of each matrix

def find_mirror_without_smudge(grid):
    for i in range(1, len(grid)):
        top_mirror = grid[:i]
        bottom_mirror = grid[i:]

        # flip top_mirror
        top_mirror = top_mirror[::-1]

        top_mirror = top_mirror[:len(bottom_mirror)]
        bottom_mirror = bottom_mirror[:len(top_mirror)]

        if top_mirror == bottom_mirror:
            return i

    return 0


def find_number_of_mismatches_in_two_lines(this_line, other_line):
    num = 0

    for i in range(len(this_line)):
        if this_line[i] != other_line[i]:
            num += 1

    return num


def find_mirror_with_smudge(grid):
    for i in range(1, len(grid)):
        top_mirror = grid[:i]
        bottom_mirror = grid[i:]

        # flip top_mirror
        top_mirror = top_mirror[::-1]

        num = 0
        for top, bottom in zip(top_mirror, bottom_mirror):
            num += find_number_of_mismatches_in_two_lines(top, bottom)

        if num == 1:
            return i

    return 0


def find_sum_of_mirrors_without_smudge():
    ans = 0
    with open("input.txt", "r") as file:
        for block in file.read().split("\n\n"):
            grid = block.splitlines()

            ans += find_mirror_without_smudge(grid) * 100
            transpose_grid = list(zip(*grid))
            ans += find_mirror_without_smudge(transpose_grid)

        print(ans)


def find_sum_of_mirrors_with_smudge():
    ans = 0
    with open("input.txt", "r") as file:
        for block in file.read().split("\n\n"):
            grid = block.splitlines()

            ans += find_mirror_with_smudge(grid) * 100
            transpose_grid = list(zip(*grid))
            ans += find_mirror_with_smudge(transpose_grid)

        print(ans)


find_sum_of_mirrors_without_smudge()
find_sum_of_mirrors_with_smudge()
