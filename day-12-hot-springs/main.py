# https://adventofcode.com/2023/day/12

# Note: As I couldn't figure the if row[0] in '#?' statement and the memoization part I checked the following YouTube video for explaination:
# https://www.youtube.com/watch?v=g3Ms5e7Jdqo

# TL;DR:
# Extract the input from the file and map to the needed format:
#   - create a backtracking recursive method that for each row and lengths tuple will check the possible appearances
#   - if our current iteration of the recursive call is in the following state:
#       - finished row => check if we also finished all lengths
#       - finished lengths => check if we also finished all '#' in row
#       - cache the current (row, lengths) key in a cache dictionary for memoization (improves computation for part 2)
#       - if we found '.' or '?' recursively call function for the subarray starting with the next element
#       - if we found '#' or '?':
#           - we check if we still have enough characters in our row
#           - we check if the previous lengths[0] elements were also # or ? (so that we know we have a continuous # substring
#           - we check if it's our last element or if the next element is not '#'
#           - if all of these are true then we call recursively for the next element with the next lengths value
#           - otherwise skip
#       - if we didn't previously cache this current key (it's a new one) cache it and return appearances


# Complexities:
# Time => O(n ^ m), where n is the length of the row and m the length of the lengths array
# Space => O(n ^ m), where n is the length of the row and m the length of the lengths array


cache = {}


def find_arrangement(row, lengths):
    if not row:
        return 1 if not lengths else 0

    if not lengths:
        return 0 if '#' in row else 1

    key = (row, lengths)
    if key in cache:
        return cache[key]

    appearances = 0
    if row[0] in ".?":
        appearances += find_arrangement(row[1:], lengths)
    if row[0] in "#?":
        if (
            lengths[0] <= len(row)
            and '.' not in row[:lengths[0]]
            and (lengths[0] == len(row) or row[lengths[0]] != '#')
        ):
            appearances += find_arrangement(row[lengths[0] + 1:], lengths[1:])
        else:
            appearances += 0

    cache[key] = appearances
    return appearances


def solve(multiplier=1):
    with open("input.txt", "r") as file:
        ans = 0

        for line in file:
            line = line.replace("\n", "").split()
            row = "?".join([line[0]] * multiplier)
            lengths = tuple(map(int, line[1].split(',') * multiplier))
            ans += find_arrangement(row, lengths)

        print(ans)


# Part 1
solve(1)
# Part 2
solve(5)