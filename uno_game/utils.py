"""
This module contains utility functions and decorators.
It includes a function for displaying cards on the terminal, a function that creates the original deck
and a decorator used for making sure there is enough cards in the deck.

"""
import random
from card import Card
from colors import RED, YELLOW, GREEN, BLUE, RESET, PURPLE


def check_deck_size(func):
    """
    Decorator to ensure, that deck has enough cards before drawing.
    If not, more cards will be put into the deck from the discard pile and the deck will be shuffled.

    :param func: The function to be wrapped.
    :return: The wrapped function.
    """
    def wrapper(self, deck, discard_pile, amount, *args, **kwargs):
        if len(deck) < amount:
            deck.extend(discard_pile[:-1])
            del discard_pile[:-1]
            random.shuffle(deck)
        return func(self, deck, discard_pile, amount, *args, **kwargs)
    return wrapper


def read_cards(cards: list[Card], if_numbers=False) -> None:
    """
    Display a list of cards from left to right on the terminal, with or without their indexes.

    :param cards: The list of cards to be displayed.
    :param if_numbers: The parameter to check if cards should display their indexes next to them.
    """
    for i in range(1, 8):
        for j, card in enumerate(cards):
            value = card.value
            card_ascii = f"""
+-------+
|{value.ljust(3)}    |
|       |
|   {value.ljust(3)} |
|       |
|    {value.rjust(3)}|
+-------+
"""
            if if_numbers and i == 1:
                printing = f"{PURPLE}{str(j).rjust(2)}.{RESET} "
            elif if_numbers:
                printing = " " * 4
            else:
                printing = ""
            card_parts = card_ascii.split("\n")
            if card.color == "R":
                printing += f"{RED}{card_parts[i]}{RESET}"
            elif card.color == "Y":
                printing += f"{YELLOW}{card_parts[i]}{RESET}"
            elif card.color == "G":
                printing += f"{GREEN}{card_parts[i]}{RESET}"
            elif card.color == "B":
                printing += f"{BLUE}{card_parts[i]}{RESET}"
            else:
                printing += card_parts[i]
            print(printing, end="\t")
        print()


def create_deck_cards() -> list[Card]:
    """
    Create the standard "UNO" game deck
    :return: The created game deck.
    """
    colors = ['R', 'Y', 'G', 'B']
    number_values = list(map(str, range(10))) + ['S', 'R', '+2']
    wild_values = ['W', 'W+4']

    deck = []

    for color in colors:
        deck.append(Card(color, '0'))
        for value in number_values[1:]:
            deck.append(Card(color, value))
            deck.append(Card(color, value))

    for value in wild_values:
        for _ in range(4):
            deck.append(Card('W', value))

    random.shuffle(deck)

    return deck
