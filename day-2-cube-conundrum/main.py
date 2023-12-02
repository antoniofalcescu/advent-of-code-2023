# https://adventofcode.com/2023/day/2

# TL;DR:
# We'll iterate through the input file line by line and parse each game (line) accordingly:
#   For the first part of the problem where we have to sum all possible games:
#       - get the game number (we'll use this number to add it to the final answer if the game is valid)
#       - iterate through each extraction (cubes picked) and then through each type of cubes
#       - for each type of cube check if it's number is less than the MAX_CUBES value
#       - if it's grater than the MAX_CUBES value then we skip this line and move on to the next
#       - at last we add the game number to our answer if we didn't find any number of cube larger than MAX_CUBES
#   For the second part where we have to sum the product of the minimum values for each type of cube for each game:
#       - for each game store a MIN_CUBES variable which we'll use to update our min values
#       - iterate through each extraction (cubes picked) and then through each type of cubes
#       - for each type of cube check if it's number is greater than our MIN_CUBES (and if so update our MIN_CUBES)
#       - after finishing the current game add to answer the product of each value for 'red', 'green' and 'blue' cubes


# Complexities:
# Time => O(n * m), where n is the number of lines in the file and m is the length of each line
# Space => O(1)

# A possible game is one in which the number of extracted cubes for each extraction
# is less ethan the number of cubes in the MAX_CUBES variable
def findSumOfPossibleGames():
    MAX_CUBES = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    ans = 0

    with open("input.txt", "r") as file:
        for line in file:
            parsedLine = line.split(':')
            gameNumber = int(parsedLine[0].split(' ')[1])
            extractions = parsedLine[1].split(';')
            isValidExtraction = True

            for extraction in extractions:
                cubes = extraction.split(',')

                for cube in cubes:
                    cube = cube.strip()
                    num = int(cube.split(' ')[0])
                    type = cube.split(' ')[1]

                    if num > MAX_CUBES[type]:
                        isValidExtraction = False
                        break

                if not isValidExtraction:
                    break

            if isValidExtraction:
                ans += gameNumber

    print(ans)

# The product of a game is the value resulted from multiplying the minimum number of cubes for each color
# so that the game is possible
def findSumOfProductsOfGames():
    ans = 0

    with open("input.txt", "r") as file:
        for line in file:
            MIN_CUBES = {
                "red": 0,
                "green": 0,
                "blue": 0
            }

            parsedLine = line.split(':')
            extractions = parsedLine[1].split(';')

            for extraction in extractions:
                cubes = extraction.split(',')

                for cube in cubes:
                    cube = cube.strip()
                    num = int(cube.split(' ')[0])
                    type = cube.split(' ')[1]

                    MIN_CUBES[type] = max(MIN_CUBES[type], num)

            ans += MIN_CUBES["red"] * MIN_CUBES["green"] * MIN_CUBES["blue"]

    print(ans)

findSumOfPossibleGames()
findSumOfProductsOfGames()