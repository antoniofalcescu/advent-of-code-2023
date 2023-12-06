# https://adventofcode.com/2023/day/6

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For the first part of the problem where we have to find all winning possibilities of multiple small races:
#       - create a list with the times and record_distances from the parsed input
#       - iterate through all races and check for all possible holding time values in range of [0, time_of_race]
#       - if our hold_time * remaining_time > record_distance increase the counter by 1
#       - after finishing checking for all holding time values multiply the total ans with our current counter
#       - after finishing iterating through all races return the ans
#   For the second part where we have to find all winning possibilities of one big race:
#       - parse the input and merge all numbers into one value each for time, respectively record_distance
#       - use the Quadratic Formula (explained inside the function body) to get our win_lower_bound and win_upper_bound
#       - use these two bounds to get the final result by calculating win_upper_bound - win_lower_bound


# Complexities:
# For part 1:
#   Time => O(r * t), where r is the number of races and t the time of each race
#   Space => O(r), where r is the number of races
# For part 2:
#   Time => O(1)
#   Space => O(1)


import math


# Inefficient O(r * t)
def findAllWinningPossibilites():
    ans = 1
    with open("input.txt", "r") as file:
        time = list(map(int, file.readline().split(":")[1].strip().split()))
        record_distance = list(map(int, file.readline().split(":")[1].strip().split()))
        number_of_races = len(time)

        for i in range(number_of_races):
            win_count = 0

            for holding_time in range(time[i] + 1):
                remaining_time = time[i] - holding_time
                if holding_time * remaining_time > record_distance[i]:
                    win_count += 1

            ans *= win_count

        print(ans)


# Quadratic formula O(1)
def findAllWinningPossibilitiesForBigRace():
    with open("input.txt", "r") as file:
        time = int(file.readline().split(":")[1].strip().replace(' ', ''))
        record_distance = int(file.readline().split(":")[1].strip().replace(' ', ''))

        # t = time, d = record_distance
        # x(t - x) > d <=> -x^2 + xt > d <=> -x^2 + xt - d > 0
        # x1, x2 = (-b +- sqrt(b^2 - 4ac)) / 2a
        # <=> x1 = (-t + sqrt(t^2 - 4d)) / (-2) <=> (t - sqrt(t^2 - 4d)) / 2
        # <=> x2 = (-t - sqrt(t^2 - 4d)) / (-2) <=> (t + sqrt(t^2 - 4d)) / 2
        # solution for >= 0 = (x1, x2)

        win_lower_bound = math.ceil((time - math.sqrt(pow(time, 2) - 4 * record_distance)) / 2)
        win_upper_bound = math.ceil((time + math.sqrt(pow(time, 2) - 4 * record_distance)) / 2)

        print(win_upper_bound - win_lower_bound)


findAllWinningPossibilites()
findAllWinningPossibilitiesForBigRace()
