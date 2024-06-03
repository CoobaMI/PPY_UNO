"""
This module defines the Game class, that holds a deck, discard pile, a list of players,
the previous color, the player index and direction of play.
It includes methods for game setup, initialization and the game loop.
"""

import random
from player import Player, Bot
from card import Card
from utils import read_cards, create_deck_cards, check_deck_size
from colors import RED, YELLOW, GREEN, BLUE, RESET, PURPLE, BRIGHT_WHITE, DARK_RED


class Game:
    """
    A class that represents the UNO game
    """
    def __init__(self):
        """
        Initialize a new Game instance.
        Sets up the deck, discard pile, players, previous color, current player, and game direction.
        """
        self.deck = create_deck_cards()
        self.discard_pile = []
        self.players = []
        self.previous_color = ""
        self.player = 0
        self.direction = 1

    def start_game(self) -> None:
        """
        Start the UNO game.
        """
        self.setup_game()
        self.distribute_initial_cards()
        self.prepare_discard_pile()
        self.play_game()

    def setup_game(self) -> None:
        """
        Set up the uno game by getting the player count initializing specified number of players.
        """
        player_count = Game.get_player_count()
        self.initialize_players(player_count)

    @staticmethod
    def get_player_count() -> int:
        """
        Allow user to input the player count and validate if it's between 2 and 4.

        :return: The inputted player count.
        """
        while True:
            print("How many players? (2 - 4)")
            try:
                player_count = int(input(": "))
                if 2 <= player_count <= 4:
                    return player_count
                else:
                    print(f"{DARK_RED}Please enter a valid number of players{RESET}")
            except ValueError:
                print(f"{DARK_RED}Please enter a valid number.{RESET}")

    def initialize_players(self, player_count: int) -> None:
        """
        Initialize a certain amount of players.

        :param player_count: The amount of players.
        """
        existing_names = set()
        bot_count = 0
        for i in range(player_count):
            is_bot = Game.get_bot_status(i)
            while True:
                if is_bot == 'y':
                    bot_count += 1
                    bot_name = f"Bot_{bot_count}"
                    if bot_name in existing_names:
                        print(f"{DARK_RED}This bot name has already been taken. Generating a new name.{RESET}")
                        continue
                    print(bot_name)
                    existing_names.add(bot_name)
                    self.players.append(Bot(bot_name))
                    break
                else:
                    player_name = Game.get_player_name(i, existing_names)
                    existing_names.add(player_name)
                    self.players.append(Player(player_name))
                    break

    @staticmethod
    def get_bot_status(player_index: int) -> str:
        """
        Allow the user to pick if a player of a certain index should be a bot.

        :param player_index: The player index.
        :return: 'y' if the player is a bot, 'n' otherwise.
        """
        while True:
            is_bot = input(f"Is player {player_index + 1} a bot? (y/n): ")
            if is_bot in ['y', 'n']:
                return is_bot
            print(f"{DARK_RED}Please enter 'y' for yes or 'n' for no.{RESET}")

    @staticmethod
    def get_player_name(player_index: int, existing_names: set[str]) -> str:
        """
        Allow user to input a player name for player of specified index.

        :param player_index: The player index.
        :param existing_names: The list of existing names.
        :return: The inputted player name.
        """
        while True:
            print(f"Enter player {player_index + 1} name")
            player_name = input(": ").strip()
            if player_name in existing_names:
                print(f"{DARK_RED}This name has already been taken. Please choose a different name.{RESET}")
            else:
                return player_name

    def distribute_initial_cards(self) -> None:
        """
        Distribute the initial 7 cards to each player in the game.
        """
        for player in self.players:
            player.draw(self.deck, self.discard_pile, 7)

    def prepare_discard_pile(self) -> None:
        """
        Prepare discard pile for play, by placing new cards on it until card on top is not an action card.
        """
        while True:
            new_card = self.deck.pop()
            self.discard_pile.append(new_card)
            if not new_card.check_if_action():
                break
        self.previous_color = self.discard_pile[-1].color

    def play_game(self) -> None:
        """
        Start the main game loop.
        """
        finish_game = False
        current_player = None
        while not finish_game:
            current_player = self.players[self.player]
            print("=" * 100)
            print(f"player: {PURPLE}{current_player.name}{RESET}")

            placeable_card_exists = self.check_placeable_card(current_player)
            while not placeable_card_exists:
                print("Card has to be drawn!")
                current_player.draw(self.deck, self.discard_pile, 1)
                print("new card:")
                read_cards([current_player.hand[-1]])
                if current_player.hand[-1].can_be_placed_on(self.discard_pile[-1], self.previous_color):
                    placeable_card_exists = True

            self.show_top_card()
            print("available cards: ")
            read_cards(current_player.hand, True)

            finish_game = self.play_turn(current_player)
            self.player = (self.player + self.direction) % len(self.players)

        print(f"{BRIGHT_WHITE}Player: {current_player.name} won!!!{RESET}")

    def check_placeable_card(self, player: Player) -> bool:
        """
        Check if player has a placeable card.

        :param player: The player.
        :return: True if player has a placeable card and False otherwise.
        """
        for card in player.hand:
            if card.can_be_placed_on(self.discard_pile[-1], self.previous_color):
                return True
        return False

    def show_top_card(self) -> None:
        """
        Show top card in the discard pile on terminal.
        """
        print("Top card in discard Pile:")
        if self.discard_pile[-1].color == "W":
            read_cards([self.discard_pile[-1]])
            color = Game.get_color_code(self.previous_color)
            print(f"(colour: {color}{self.previous_color}{RESET})")
        else:
            read_cards([self.discard_pile[-1]])

    @staticmethod
    def get_color_code(color: str) -> str:
        """
        Get color code for card color.

        :param color: The card color.
        :return: The correct ANSI color code.
        """
        if color == "R":
            return RED
        elif color == "Y":
            return YELLOW
        elif color == "G":
            return GREEN
        else:
            return BLUE

    def play_turn(self, current_player: Player) -> bool:
        """
        Play a players turn.

        :param current_player: The currently participating player.
        :return: If player has no cards left after turn True otherwise False.
        """
        while True:
            print("enter card number")
            try:
                user_input = current_player.pick_card(self.discard_pile[-1], self.previous_color)
                if not (0 <= user_input < len(current_player.hand)):
                    print(f"{DARK_RED}Invalid input, please enter a valid number.{RESET}")
                    continue
            except ValueError:
                print(f"{DARK_RED}Invalid input, please enter a number.{RESET}")
                continue

            if current_player.hand[user_input].can_be_placed_on(self.discard_pile[-1], self.previous_color):
                new_card = current_player.hand.pop(user_input)
                print("Placed card:")
                read_cards([new_card])
                self.discard_pile.append(new_card)

                if len(current_player.hand) == 0:
                    return True

                if new_card.color == "W":
                    self.previous_color = Game.pick_new_color(current_player)
                else:
                    self.previous_color = new_card.color

                if len(current_player.hand) == 1:
                    self.call_uno(current_player)

                self.handle_action_card(new_card)
                break
            else:
                print(f"{DARK_RED}Card cannot be placed.{RESET}")
        return False

    @staticmethod
    def pick_new_color(current_player: Player) -> str:
        """
        Allow player to pick the index of a color for the "Wild" card.

        :param current_player: The currently participating player.
        :return: The color corresponding to the index.
        """
        while True:
            print(f"Pick a color! ({PURPLE}0{RESET}: {RED}R{RESET}, {PURPLE}1{RESET}: {YELLOW}Y{RESET},"
                  f" {PURPLE}2{RESET}: {GREEN}G{RESET}, {PURPLE}3{RESET}: {BLUE}B{RESET})")
            try:
                user_input = current_player.pick_color()
            except ValueError:
                print(f"{DARK_RED}Invalid input, please enter a number.{RESET}")
                continue

            if user_input == 0:
                return "R"
            elif user_input == 1:
                return "Y"
            elif user_input == 2:
                return "G"
            elif user_input == 3:
                return "B"
            else:
                print(f"{DARK_RED}Invalid input, please try again.{RESET}")

    def call_uno(self, current_player: Player) -> None:
        """
        Allow player to call UNO or stop it.

        :param current_player: The currently participating player.
        """
        while True:
            user_input = current_player.uno_interact()
            if user_input == "UNO":
                break
            elif user_input == "STOP UNO":
                current_player.draw(self.deck, self.discard_pile, 2)
                break
            else:
                print(f"{DARK_RED}Invalid input, please try again.{RESET}")

    def handle_action_card(self, new_card: Card) -> None:
        """
        Handle action card correctly, according to the value.

        :param new_card: The card being played by the current player.
        """
        if new_card.value == "W+4":
            self.player = (self.player + self.direction) % len(self.players)
            self.players[self.player].draw(self.deck, self.discard_pile, 4)
        elif new_card.value == "+2":
            self.player = (self.player + self.direction) % len(self.players)
            self.players[self.player].draw(self.deck, self.discard_pile, 2)
        elif new_card.value == "S":
            self.player = (self.player + self.direction) % len(self.players)
        elif new_card.value == "R":
            self.direction *= -1
