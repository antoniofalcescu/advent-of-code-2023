# https://adventofcode.com/2023/day/9

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For both parts:
#       - will use an utility method that calculates the sequences for each line
#   For the first part of the problem where we have to find all winning possibilities of multiple small races:
#       - after calculating the sequences iterate bottom-up and append as the last element of the current sequence
#               a new element representing the prediction for this sequence
#       - at last add to our final answer the last element of sequence[0] (which is the input line)
#   For the second part where we have to find all winning possibilities of one big race:
#       - after calculating the sequences iterate bottom-up and insert as the first element of the current sequence
#               a new element representing the history for this sequence
#       - at last add to our final answer the first element of sequence[0] (which is the input line)


# Complexities:
# Time => O(n * m), where n is the number of lines and m the number of values of each line
# Space => O(m^2), where m is number of values of each line

def calculate_sequences(line):
    sequnces = [line]
    while not all(v == 0 for v in line):
        new_sequence = []

        for i in range(1, len(line)):
            new_sequence.append(line[i] - line[i - 1])
        sequnces.append(new_sequence)
        line = new_sequence

    return sequnces


def find_prediction():
    ans = 0
    with open("input.txt", "r") as file:
        for line in file:
            line = list(map(int, line.split()))

            sequences = calculate_sequences(line)
            for i in range(len(sequences) - 2, -1, -1):
                prediction_for_sequence = sequences[i + 1][-1] + sequences[i][-1]
                sequences[i].append(prediction_for_sequence)

            ans += sequences[0][-1]
        print(ans)


def find_history():
    ans = 0
    with open("input.txt", "r") as file:
        for line in file:
            line = list(map(int, line.split()))

            sequences = calculate_sequences(line)
            for i in range(len(sequences) - 2, -1, -1):
                prediction_for_sequence = sequences[i][0] - sequences[i + 1][0]
                sequences[i].insert(0, prediction_for_sequence)

            ans += sequences[0][0]
        print(ans)

find_prediction()
find_history()