# https://adventofcode.com/2023/day/8

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For both parts:
#       - parse the input lines into a map with key and value as object with 2 keys: 'L' and 'R'
#   For the first part where we have to find number of steps from 'AAA' to 'ZZZ':
#       - start from 'AAA' and iterate through or instructions until we reach 'ZZZ'
#       - use the maps object with 'L' and 'R' properties
#       - infinitely loop through our instructions with modulo
#       - after we reach 'ZZZ' (always will) return the number of steps
#   For the second part where we have to find number of steps from all locations ending with 'A' to any location ending with 'Z':
#       - store all locations ending with 'A' in a list
#       - iterate through that list and for each position find the number of steps it takes to reach a 'Z' location (same as in part1)
#           (note that we check individually if they reach 'Z', they don't have to reach it at the same time for now)
#       - when we reach a location ending with 'Z' store our steps number in a new array all_steps
#       - calculate the LCM (Least Common Multiple) for all of our numbers in the all_steps array
#       - return that LCM as that is the first time all locations 'A' will reach any location ending in 'Z' at the same time


# Complexities:
# Time => O(n), where n is the number of paths(lines)
# Space => O(n), where n is the number of paths(lines)


def find_steps_from_AAA_to_ZZZ():
    with open("input.txt", "r") as file:
        instructions = list(file.readline().replace('\n', ''))
        file.readline()
        maps = {line.split(' = ')[0]: {
            'L': line.split(' = ')[1].split(', ')[0].replace('(', ''),
            'R': line.split(' = ')[1].split(', ')[1].replace(')\n', ''),
        } for line in file}

        position = 'AAA'
        instruction_index = 0
        steps = 0

        while position != 'ZZZ':
            position = maps[position][instructions[instruction_index]]
            instruction_index = (instruction_index + 1) % len(instructions)
            steps += 1

        print(steps)

def find_steps_from_each_A_to_any_Z():
    def gcd(a, b):
        if a == 0:
            return b
        return gcd(b % a, a)

    with open("input.txt", "r") as file:
        instructions = list(file.readline().replace('\n', ''))
        file.readline()
        maps = {line.split(' = ')[0]: {
            'L': line.split(' = ')[1].split(', ')[0].replace('(', ''),
            'R': line.split(' = ')[1].split(', ')[1].replace(')\n', ''),
        } for line in file}

        positions = list(filter(lambda x: x.endswith('A'), maps.keys()))
        all_steps = []
        instruction_index = 0

        for position in positions:
            steps = 0
            while not position.endswith('Z'):
                position = maps[position][instructions[instruction_index]]
                instruction_index = (instruction_index + 1) % len(instructions)
                steps += 1
            all_steps.append(steps)

        lcm = 1
        for step in all_steps:
            lcm = lcm * step // gcd(lcm, step)

        print(lcm)



find_steps_from_AAA_to_ZZZ()
find_steps_from_each_A_to_any_Z()

