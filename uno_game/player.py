"""
This module defines Player and Bot classes, that both hold a name and a hand of cards.
The Bot class inherits from Player and overrides some of the methods to make the input automatic.
It includes methods for drawing a new card, picking a card,
picking a color of a card and interacting with a "UNO" situation.
"""
import random

from card import Card
from utils import check_deck_size


class Player:
    """
    A class that represents a single player in an uno game.
    It holds a name and a hand of cards.
    """
    def __init__(self, name: str):
        """
        Initialize a new Player instance.

        :param name: The name of the player.
        """
        self.name = name
        self.hand = []

    @check_deck_size
    def draw(self, deck: list[Card], discard_pile: list[Card], amount: int) -> None:
        """
        Draw a specified number of cards from the deck to the player's hand.

        :param deck: The deck of cards to draw from.
        :param discard_pile: The discard pile to replenish the deck.
        :param amount: The number of cards to draw.
        """
        self.hand.extend(deck[:amount])
        del deck[:amount]

    def pick_card(self, previous_card: Card, previous_color: str) -> int:
        """
        Allow the player to pick a card index

        :param previous_card: The last placed card.
        :param previous_color: The last placed cards color (important when last card was a "Wild" card).
        :return: The selected card index.
        """
        return int(input(": "))

    def pick_color(self) -> int:
        """
        Allow the player to pick a color index

        :return: The selected color index
        """
        return int(input(": "))

    def uno_interact(self) -> str:
        """
        Allow players to interact with UNO calls

        :return: The users input.
        """
        print("(UNO / STOP UNO)")
        user_input = input(": ").upper()
        return user_input


class Bot(Player):
    """
    A class that represents a Bot player in an uno game, inheriting from Player.
    """

    def __init__(self, name):
        """
        Initialize a new Bot instance.

        :param name: The name of the bot.
        """
        super().__init__(name)

    def pick_card(self, previous_card: Card, previous_color: str) -> int:
        """
        Automatically pick a random card index out of the bots hand, that can be placed on the previous card.

        :param previous_card: The last placed card.
        :param previous_color: The last placed cards color (important when last card was a "Wild" card).
        :return: The random card index.
        """
        selectable = [i for i, card in enumerate(self.hand) if card.can_be_placed_on(previous_card, previous_color)]
        random_card_index = random.choice(selectable)
        return random_card_index

    def pick_color(self) -> int:
        """
        Automatically pick a random color index.

        :return: The random color index
        """
        value = random.randint(0, 3)
        print(value)
        return value

    def uno_interact(self) -> str:
        """
        Automatically call UNO.

        :return: The bots reaction to an uno call ("UNO")
        """
        print("UNO")
        return "UNO"
