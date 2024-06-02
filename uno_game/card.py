"""
This module defines a Card class, that holds a color and a value.
It includes methods for checking if the card can be placed on another and checking if it's an action card.
"""

import re


class Card:
    """
    A class that represents a single card in an uno game.
    It holds a color and a value.
    """
    def __init__(self, color: str, value: str):
        """
        Initialize a new Card instance.

        :param color: The color of the card.
        :param value: The value of the card.
        """
        self.color = color
        self.value = value

    def __str__(self) -> str:
        """
        Return a string representation of the card.

        :return: The color and value of the card separated by ";" as a string.
        """
        return f"{self.color};{self.value}"

    def can_be_placed_on(self, card_to_place_on: 'Card', previous_color: str) -> bool:
        """
        Check if card can be placed on another card.

        :param card_to_place_on: The card that this card will be placed on.
        :param previous_color: Color of the previous card (needed when previous card was a "Wild" card)
        :return: True if this card can be placed on the specified card, False otherwise.
        """
        return (
            (card_to_place_on.color == "W" and self.color == previous_color) or
            card_to_place_on.color == self.color or
            card_to_place_on.value == self.value or
            self.color == "W"
        )

    def check_if_action(self):
        """
        Check if card is an "action" card.

        :return: True if card is classified as an action card, False otherwise.
        """
        pattern = r'^[0-9]$'
        return not (re.match(pattern, self.value))
