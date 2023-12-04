# https://adventofcode.com/2023/day/4

# TL;DR:
# We'll iterate through the input file line by line and parse each game (line) accordingly:
#   For the first part of the problem where we have to sum all scratchcards:
#       - make a set with the winning numbers
#       - save our numbers in a list
#       - iterate through that list and check if it's a winning number => increment multiplier by 1
#       - calculate 2 to the power of that multiplier and add it to our final answer
#   For the second part where we have to duplicate the following lines and calculate the number of new total lines:
#       - store winning numbers and our numbers in 2 separate arrays
#       - make a copies array that has 1 for each element
#       - check for our nums if they are winning and increment our won variable by 1
#       - iterate through our number of next won games and add the value of the prev scratchcards to the next


# Complexities:
# Time => O(n * m), where n is the number of lines in the file and m is the length of each line
# Space => O(1)


# The value of a strachcard is given by calculating how many winning numbers we have
# and calculate 2 to the power of that number of winning numbers
def findSumOfScratchcards():
    ans = 0

    with open("input.txt", "r") as file:
        for line in file:
            line = line.split(':')[1].strip()

            winning_nums_aux = line.split('|')[0].split(' ')
            winning_nums = set()
            for num in winning_nums_aux:
                if num.isdigit():
                    winning_nums.add(int(num))

            multiplier = -1

            nums = line.split('|')[1].split(' ')
            for num in nums:
                if num.isdigit():
                    if int(num) in winning_nums:
                        multiplier += 1

            if multiplier > -1:
                ans += pow(2, multiplier)

        print(ans)


def findSumOfCopies():
    winning_nums = []
    nums = []

    with open("input.txt", "r") as file:
        for line in file:
            card = int(line.split(':')[0].strip().split(' ')[-1])
            line = line.split(':')[1].strip()

            winning_nums_parsed = line.split('|')[0].split(' ')
            winning_nums_aux = set()
            for num in winning_nums_parsed:
                if num.isdigit():
                    winning_nums_aux.add(int(num))

            winning_nums.append(winning_nums_aux)

            nums_parsed = line.split('|')[1].split(' ')
            nums.append(nums_parsed)

        copies = [1] * len(nums)

        for (i, list_nums) in enumerate(nums):
            won = 0
            for num in list_nums:
                if num.isdigit():
                    if int(num) in winning_nums[i]:
                        won += 1

            for j in range(i + 1, i + 1 + won):
                copies[j] += copies[i]

        print(sum(copies))


part1()
part2()