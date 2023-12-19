# https://adventofcode.com/2023/day/15

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For the first part of the problem where we have to find the sum of all hash values:
#       - get the has value according to the formula from the requirements
#       - iterate through all words from the input file and sum upp all calculated hashes
#   For the second part where we have to find the sum of all lenses from the 256 boxes:
#       - we'll use a dict to store the boxes values (it's more space and time efficient than an array because we only keep track of the boxes that are not empty)
#       - for each word we calculate its hash and create a box with this hash value (if it doesn't exist already)
#       - afterward, we check to see if our current word has '=' or '-':
#           - in case of '=' => then we expect a format of 'label'='numeric_value'
#               - we look in the current box to see if this label already exists and if so => update the existing label's value with the new one
#               - if the label doesn't exist => append it at the end of the list
#           - in case of '-' => we expect the format 'label'-
#               - we remove (if it exists) the label from the current box and shift all of the following elements by one (Python's builtin remove does this for us)
#               - we also check if the current box is empty (after the removal) => if so we delete the box altogether
#       - after we finished all words => iterate through our boxes and calculate the lens_value with the given formula
#       - add the lens_value to a total_sum for each lens in all boxes and return this as the final answer


# Complexities:
# For part 1:
#   Time => O(w * c), where w is the number of words and c the number of characters for each word
#   Space => O(1)
# For part 2:
#   Time => O(w * len(box[i])), where w is the number of words and len(box[i]) represents the length of the current box
#   Space => O(256 * w) = O(w), where 256 is the maximum possible number of our boxes and w is the number of words that are inside those boxes

def calculate_hash(word):
    hash = 0

    for c in word:
        hash = (hash + ord(c)) * 17 % 256

    return hash


def find_total_hash():
    with open("input.txt", "r") as file:
        init_sequence = file.readline().replace("\n", "").split(",")

        total_hash = 0
        for word in init_sequence:
            total_hash += calculate_hash(word)

        print(total_hash)


def get_label_and_focal_length(word):
    if '=' in word:
        label = word.split("=")[0]
        focal_length = int(word.split("=")[1])
        return label, focal_length
    elif '-' in word:
        label = word.replace("-", "")
        return label, None
    else:
        return None, None


def find_sum_of_all_lenses():
    with open("input.txt", "r") as file:
        init_sequence = file.readline().replace("\n", "").split(",")
        boxes = {}

        for word in init_sequence:
            label, focal_length = get_label_and_focal_length(word)

            hash = calculate_hash(label)
            if hash not in boxes:
                boxes[hash] = []
            box = boxes[hash]

            if '=' in word:
                already_exists = False

                for i in range(len(box)):
                    if label == box[i][0]:
                        box[i] = (label, focal_length)
                        already_exists = True
                        break
                if not already_exists:
                    box.append((label, focal_length))

            elif '-' in word:
                for i in range(len(box)):
                    if label == box[i][0]:
                        box.remove(box[i])
                        break
                if not box:
                    boxes.pop(hash)

        ans = 0
        for key, value in boxes.items():
            for i in range(len(value)):
                lens = (key + 1) * (i + 1) * value[i][1]
                ans += lens

        print(ans)


find_total_hash()
find_sum_of_all_lenses()