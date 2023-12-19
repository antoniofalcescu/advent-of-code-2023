# https://adventofcode.com/2023/day/19

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For the first part of the problem where we have to find the sum of all accepted parts:
#       - parse the input (both workflows and parts)
#       - for each part check it by looping through the workflows to find if the part matches that workflow and send it to the next workflow until we reach 'A' or 'R'
#   For the second part where we have to find the sum of all lenses from the 256 boxes:
#       - parse the input (only the workflows)
#       - create a recursive function similar to the one from part 1 but:
#           - instead of iterating through each aprt we take a part_ranges ([1, 4000] inclusive on both ends)
#           - iterate through all the workflows starting from 'in' and split for each of those the current part_ranges into 2 halves (the one that matches the current workflow and the other that doesn't)
#           - recursively call the same method with the new part_ranges for the true half
#           - if we didn't find a valid true half the we recursively call for our last element from this workflow (the fallback)


# Complexities:
# For part 1:
#   Time => O(n * m), where n is the number of parts and m the number of workflows
#   Space => O(n * m), where n is the number of parts and m the number of workflows
# For part 2:
#   Time => O(4000 * 4 * n) = O(n), where n is the number of workflows and 4000 * 4 the possible combinations of all 4 part symbols
#   Space => O(4000 * 4 * n) = O(n), where n is the number of workflows and 4000 * 4 the possible combinations of all 4 part symbols

def parse_workflow(workflow):
    workflow = workflow[:len(workflow) - 1].split("{")

    name = workflow[0]
    parsed_workflow = []

    conditions = workflow[1].split(",")
    for condition in conditions:
        if ':' in condition:
            condition = condition.split(":")

            part_symbol = condition[0][0]
            criteria = condition[0][1]
            number = int(condition[0][2:])
            new_workflow = condition[1]

            parsed_workflow.append({
                part_symbol: {
                    'criteria': criteria,
                    'number': number,
                    'new_workflow': new_workflow
                }
            })
        else:
            parsed_workflow.append(condition)

    return name, parsed_workflow


def parse_part(part):
    part = part[1: len(part) - 1]
    parsed_part = {}
    part = part.split(",")
    for p in part:
        p = p.split("=")
        parsed_part[p[0]] = int(p[1])

    return parsed_part


def check_part(part, workflows):
    current_workflow_name = 'in'

    while True:
        if current_workflow_name in "AR":
            return current_workflow_name == 'A'

        workflow = workflows[current_workflow_name]
        for w in workflow:
            if isinstance(w, dict):
                ch = list(w)[0]
                criteria = w[ch]['criteria']
                number = w[ch]['number']
                new_workflow = w[ch]['new_workflow']

                if criteria == '<':
                    if part[ch] < number:
                        current_workflow_name = new_workflow
                        break
                elif criteria == '>':
                    if part[ch] > number:
                        current_workflow_name = new_workflow
                        break
            elif isinstance(w, str):
                current_workflow_name = w
                break


def calculate_part_sum(part):
    part_sum = sum(part.values())

    return part_sum


def find_sum_of_accepted_parts():
    with open("input.txt", "r") as file:
        aux = file.read().split("\n\n")
        workflows = aux[0].split("\n")
        parts = aux[1].split("\n")

        parsed_workflows = dict()
        for i in range(len(workflows)):
            name, parsed_workflow = parse_workflow(workflows[i])
            parsed_workflows[name] = parsed_workflow

        for i in range(len(parts)):
            parts[i] = parse_part(parts[i])

        ans = 0
        for part in parts:
            is_part_accepted = check_part(part, parsed_workflows)
            if is_part_accepted:
                ans += calculate_part_sum(part)

        print(ans)


def find_number_of_possible_combinations(part_ranges, workflows, current_workflow_name='in'):
    if current_workflow_name == "R":
        return 0

    if current_workflow_name == "A":
        product = 1
        for low, high in part_ranges.values():
            product *= high - low + 1
        return product

    workflow = workflows[current_workflow_name]
    total = 0
    for w in workflow:
        if isinstance(w, dict):
            ch = list(w)[0]
            criteria = w[ch]['criteria']
            number = w[ch]['number']
            new_workflow = w[ch]['new_workflow']
            low, high = part_ranges[ch]

            if criteria == '<':
                true_half = (low, number - 1)
                false_half = (number, high)
            elif criteria == '>':
                true_half = (number + 1, high)
                false_half = (low, number)
            else:
                return 0

            if true_half[0] <= true_half[1]:
                part_ranges_copy = dict(part_ranges)
                part_ranges_copy[ch] = true_half
                total += find_number_of_possible_combinations(part_ranges_copy, workflows, new_workflow)

            if false_half[0] <= false_half[1]:
                part_ranges = dict(part_ranges)
                part_ranges[ch] = false_half
            else:
                break
        elif isinstance(w, str):
            total += find_number_of_possible_combinations(part_ranges, workflows, w)
            break

    return total


def find_number_of_possibly_accepted_parts():
    with open("input.txt", "r") as file:
        aux = file.read().split("\n\n")
        workflows = aux[0].split("\n")

        parsed_workflows = dict()
        for i in range(len(workflows)):
            name, parsed_workflow = parse_workflow(workflows[i])
            parsed_workflows[name] = parsed_workflow

        part_ranges = {key: (1, 4000) for key in "xmas"}
        ans = find_number_of_possible_combinations(part_ranges, parsed_workflows)
        print(ans)


find_sum_of_accepted_parts()
find_number_of_possibly_accepted_parts()
