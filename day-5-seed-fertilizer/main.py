# https://adventofcode.com/2023/day/5

# TL;DR:
# We'll iterate through the input file line by line and parse each game (line) accordingly:
#   For the first part of the problem where we have to find the minimum location from an array of seeds:
#       - parse the seeds array
#       - iterate through the file and check if the current mapping changes the values in our seeds array
#       - if so update the modified set by adding our updated seed index to the set and update the seed value
#       - return the min value from our seeds array
#   For the second part where we have to find the minimum location from a seeds array that contains ranges instead of plain numbers
#   (e.g of a range: [seeds[i], seeds[i] + seeds[i + 1] for each i % 2 == 0):
#       - parse the seeds array
#       - iterate through the file and save the current mapping to a mappings array
#       - iterate through the mappings array and while our seeds array is not empty pop an element from it
#       - with the popped element(which is a range) and the current mapping (which can also be seen as a range) we have to intersect them and create 1-3 new ranges with the common values from them
#       - if we have a modified range (from source we update it to target values) we add it to a new aux variable called ranges
#       - if we didn't modify the previous seeds_range we add it with the same values in the aux ranges array
#       - after emptying the seeds_ranges we reinitialize it with the values from the ranges array
#       - continue the iteration with the next mapping group


# Complexities:
# For part 1:
#   Time => O(n * m), where n is the number of lines in the file and m is the length of seeds array
#   Space => O(n), where n is the size of a line (could be seeds line or any other mapping line)
# For part 2:
#   Time => O(n * m * s), where n is the number of lines in the file, m is the number of the elements in a mapping and s is the number of elements in the seeds_ranges array
#   Space => O(n * m), where n is the number of mappings and m is the size of each mapping

def findMinLocationFromSeeds():
    with open("input.txt", "r") as file:
        seeds = [int(x) for x in file.readline().split(":")[1].split()]
        modified = set()

        for line in file:
            if line[0].isdigit():
                mapping = [int(x) for x in line.split()]
                for i in range(len(seeds)):
                    if i in modified:
                        continue

                    range_start = mapping[1]
                    range_end = mapping[1] + mapping[2]
                    if seeds[i] in range(range_start, range_end):
                        diff = seeds[i] - range_start
                        seeds[i] = mapping[0] + diff
                        modified.add(i)

            else:
                modified = set()

        print(min(seeds))


# Disclaimer: This solution is inspired from: https://www.youtube.com/watch?v=NmxHw_bHhGM
# My initial solution worked on the demo input but wasn't working on the test input
# and I couldn't handle debugging values like these: 3136945476 509728956
def findMinLocationFromSeedsRanges():
    with open("input.txt", "r") as file:
        seeds = [int(x) for x in file.readline().split(":")[1].split()]
        seeds_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

        mappings = []
        maps = []
        for line in file:
            if line[0].isdigit():
                maps.append([int(x) for x in line.split()])
            else:
                if maps:
                    mappings.append(maps)
                maps = []
        mappings.append(maps)

        for mapping in mappings:
            ranges = []
            while seeds_ranges:
                seed_range_start, seed_range_end = seeds_ranges.pop()
                for target, source, length in mapping:
                    new_range_start = max(seed_range_start, source)
                    new_range_end = min(seed_range_end, source + length)

                    if new_range_start < new_range_end:
                        new_range = (new_range_start - source + target, new_range_end - source + target)
                        ranges.append(new_range)

                        if seed_range_start < new_range_start:
                            seeds_ranges.append((seed_range_start, new_range_start))
                        if seed_range_end > new_range_end:
                            seeds_ranges.append((new_range_end, seed_range_end))
                        break
                else:
                    ranges.append((seed_range_start, seed_range_end))
            seeds_ranges = ranges

    print(min(seeds_ranges)[0])


findMinLocationFromSeeds()
findMinLocationFromSeedsRanges()
