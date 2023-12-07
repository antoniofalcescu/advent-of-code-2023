# https://adventofcode.com/2023/day/7

# TL;DR:
# Extract the input from the file and map to the needed format:
#   For both parts we will use these utils methods:
#       - getHandType  => iterates through a card hand and returns the type of hand while also taking account of joker wildcards
#                      => if we have jokers (for part2) we will add the number of jokers to the highest card
#       - compareHands => util method that takes 2 hands and compares them for the sorted() built-in method
#                      => we store a dict to map the card character to a number value
#                      => we use the previous getHandType for both hands to see if they are of different types
#                      => if they are of equal types we iterate through both hands to see the bigger character out of the two from left to right
#   For the first part of the problem where we have to find sum of all winnings from the poker game:
#       - we sort the hands with the built-in sorted method and passing a custom comparator that uses our compareHands with an isJoker argument set to False
#       - we iterate through the sorted hands to multiply the bid with the according number in ascending order
#       - add the multiplied bid to the final answer and after iterating through all hands return that answer
#   For the second part where we have to find sum of all winnings from the poker game that allows joker wildcards:
#       - we sort the hands with the built-in sorted method and passing a custom comparator that uses our compareHands with an isJoker argument set to True
#       - we iterate through the sorted hands to multiply the bid with the according number in ascending order
#       - add the multiplied bid to the final answer and after iterating through all hands return that answer


# Complexities:
# Time => O(n log n), where n is the number of hands(lines) (actually it's (m * (n log n)) but m is always 5 (number of cards in a poker hand)
# Space => O(n), where n is the size of the list of hands



from enum import Enum
from functools import cmp_to_key


def getHandType(hand, isJoker):
    class HandType(Enum):
        HIGH_CARD = 1
        ONE_PAIR = 2
        TWO_PAIR = 3
        THREE_OF_A_KIND = 4
        FULL_HOUSE = 5
        FOUR_OF_A_KIND = 6
        FIVE_OF_A_KIND = 7

    cards = dict()
    jokers = 0

    for card in hand:
        if isJoker and card == 'J':
            jokers += 1
            continue

        if card in cards:
            cards[card] += 1
        else:
            cards[card] = 1

    if isJoker:
        if jokers == 5:
            cards['J'] = 5
        else:
            keyOfMaxValue = max(cards, key=cards.get)
            cards[keyOfMaxValue] += jokers
        keyOfMaxValue = max(cards, key=cards.get)
    else:
        keyOfMaxValue = max(cards, key=cards.get)

    numberOfUniqueCards = len(cards)


    if numberOfUniqueCards == 5:
        return HandType.HIGH_CARD
    elif numberOfUniqueCards == 4:
        return HandType.ONE_PAIR
    elif numberOfUniqueCards == 3:
        if cards[keyOfMaxValue] == 2:
            return HandType.TWO_PAIR
        elif cards[keyOfMaxValue] == 3:
            return HandType.THREE_OF_A_KIND
    elif numberOfUniqueCards == 2:
        if cards[keyOfMaxValue] == 3:
            return HandType.FULL_HOUSE
        elif cards[keyOfMaxValue] == 4:
            return HandType.FOUR_OF_A_KIND
    elif numberOfUniqueCards == 1:
        return HandType.FIVE_OF_A_KIND


def compareHands(thisHand, otherHand, isJoker):
    CARD_VALUES = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'Q': 13,
        'K': 14,
        'A': 99,
    }

    if isJoker:
        CARD_VALUES['J'] = 1
    else:
        CARD_VALUES['J'] = 12


    thisHandType = getHandType(thisHand, isJoker)
    otherHandType = getHandType(otherHand, isJoker)

    if thisHandType.value > otherHandType.value:
        return 1
    elif thisHandType.value < otherHandType.value:
        return -1
    else:
        for i in range(len(thisHand)):
            if CARD_VALUES[thisHand[i]] > CARD_VALUES[otherHand[i]]:
                return 1
            elif CARD_VALUES[thisHand[i]] < CARD_VALUES[otherHand[i]]:
                return -1


def getPokerWinningsWithoutJoker():
    def compare(thisHand, otherHand):
        return compareHands(thisHand, otherHand, False)

    ans = 0
    with open("input.txt", "r") as file:
        handsWithBids = {line.split()[0]: int(line.split()[1]) for line in file}
        hands = list(handsWithBids)

        hands = sorted(hands, key=cmp_to_key(compare))

        for i in range(len(hands)):
            multiplier = i + 1
            amountWon = handsWithBids[hands[i]]

            ans += amountWon * multiplier

        print(ans)


def getPokerWinningsWithJoker():
    def compare(thisHand, otherHand):
        return compareHands(thisHand, otherHand, True)

    ans = 0
    with open("input.txt", "r") as file:
        handsWithBids = {line.split()[0]: int(line.split()[1]) for line in file}
        hands = list(handsWithBids)

        hands = sorted(hands, key=cmp_to_key(compare))

        for i in range(len(hands)):
            multiplier = i + 1
            amountWon = handsWithBids[hands[i]]

            ans += amountWon * multiplier

        print(ans)


getPokerWinningsWithoutJoker()
getPokerWinningsWithJoker()