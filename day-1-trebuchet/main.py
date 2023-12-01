# https://adventofcode.com/2023/day/1

# TL;DR:
# We'll iterate through the input file line by line and check for each line with 2 pointers (left and right)
# for the first and the last digit (number or word).
# We iterate from left to right until we find the first number while checking:
#   - if the current char is a digit => store that number as the first digit
#   - if the current word (range [0, currentIndex] is a word that represents a digit
#       => store the equivalent of that word
# We repeat the process from right to left to find the last number
# After finding both values we build our 2-digit number and add it to our total sum
# Lastly, we return the final sum


# Complexities:
# Time => O(n * m), where n is the number of lines in the file and m is the length of each line
# Space => O(1)


VALID_DIGITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

sum = 0

with open("input.txt", "r") as file:
    for line in file:
        l, firstDigit = 0, -1
        r, lastDigit = len(line) - 1, -1

        while firstDigit == -1:
            if line[l].isdigit():
                firstDigit = int(line[l])
            else:
                for key in VALID_DIGITS:
                    if key in line[: (l + 1)]:
                        firstDigit = VALID_DIGITS[key]
                        break
            l += 1

        while lastDigit == -1:
            if line[r].isdigit():
                lastDigit = int(line[r])
            else:
                for key in VALID_DIGITS:
                    if key in line[r:]:
                        lastDigit = VALID_DIGITS[key]
                        break
            r -= 1

        num = firstDigit * 10 + lastDigit
        sum += num

print(sum)
