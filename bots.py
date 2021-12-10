"""Place in root of Game of Greed Project,
at same level as pyproject.toml
"""

from abc import ABC, abstractmethod
import builtins
import re
from typing import Counter
from game_of_greed.game import Game
from game_of_greed.game_logic import GameLogic


class BaseBot(ABC):
    """Base class for Game of Greed bots"""

    def __init__(self, print_all=False):
        self.last_print = ""
        self.last_roll = []
        self.print_all = print_all
        self.dice_remaining = 0
        self.unbanked_points = 0

        self.real_print = print
        self.real_input = input
        builtins.print = self._mock_print
        builtins.input = self._mock_input
        self.total_score = 0

    def reset(self):
        """restores the real print and input builtin functions"""

        builtins.print = self.real_print
        builtins.input = self.real_input

    def report(self, text):
        """Prints out final score, and all other lines optionally"""

        if self.print_all:
            self.real_print(text)
        elif text.startswith("Thanks for playing."):
            score = re.sub("\D", "", text)
            self.total_score += int(score)

    def _mock_print(self, *args, **kwargs):
        """steps in front of the real builtin print function"""

        line = " ".join(args)

        if "unbanked points" in line:

            # parse the proper string
            # E.g. "You have 700 unbanked points and 2 dice remaining"
            unbanked_points_part, dice_remaining_part = line.split("unbanked points")

            # Hold on to unbanked points and dice remaining for determining rolling vs. banking
            self.unbanked_points = int(re.sub("\D", "", unbanked_points_part))

            self.dice_remaining = int(re.sub("\D", "", dice_remaining_part))

        elif line.startswith("*** "):

            self.last_roll = [int(ch) for ch in line if ch.isdigit()]

        else:
            self.last_print = line

        self.report(*args, **kwargs)

    def _mock_input(self, *args, **kwargs):
        """steps in front of the real builtin print function"""

        if self.last_print == "(y)es to play or (n)o to decline":

            return "y"

        elif self.last_print == "Enter dice to keep, or (q)uit:":

            return self._enter_dice()

        elif self.last_print == "(r)oll again, (b)ank your points or (q)uit:":

            return self._roll_bank_or_quit()

        raise ValueError(f"Unrecognized last print {self.last_print}")

    def _enter_dice(self):
        """simulate user entering which dice to keep.
        Defaults to all scoring dice"""

        roll = GameLogic.get_scorers(self.last_roll)

        roll_string = ""

        for value in roll:
            roll_string += str(value)

        self.report("> " + roll_string)

        return roll_string

    @abstractmethod
    def _roll_bank_or_quit(self):
        """decide whether to roll the dice, bank the points, or quit"""

        # subclass MUST implement this method
        pass

    @classmethod
    def play(cls, num_games=1):
        """Tell Bot play game a given number of times.
        Will report average score"""

        mega_total = 0

        for _ in range(num_games):
            player = cls()
            game = Game()
            try:
                game.play()
            except SystemExit:
                # in game system exit is fine
                # because that's how they quit.
                pass

            with open("log_sams.txt", "a") as file:
                file.write(str(player.total_score) + "\n")
            mega_total += player.total_score
            player.reset()

        print(
            f"{cls.__name__}: {num_games} games played with average score of {mega_total // num_games}"
        )


class NervousNellie(BaseBot):
    """NervousNellie banks the first roll always"""

    def _roll_bank_or_quit(self):
        return "b"

class Sams(BaseBot):
    def _roll_bank_or_quit(self):
        if self.unbanked_points >= 250 and self.dice_remaining >= 2:
            return "b"
        elif self.unbanked_points >= 350 and self.dice_remaining == 1:
            return "b"
        return "r"

    def _enter_dice(self):
        counts_for_dice = Counter(self.last_roll)
        total_score_of_dice = GameLogic.calculate_score(tuple(self.last_roll))
        keepers_possible = GameLogic.get_scorers(tuple(self.last_roll))
        if total_score_of_dice == 150:
            return "1"
        if counts_for_dice[2] == 3 and total_score_of_dice >= 200:
            return "".join([str(num) for num in keepers_possible if num != 2])

        return super()._enter_dice()
        
        # [str(num) for num in keepers_possible if num != 2].join("")

class Chloes_test(BaseBot):
    def _roll_bank_or_quit(self):
        
        if self.unbanked_points >= 250:
            return "b"
        else:
            return "r"
        
class Chloes(BaseBot):
    def _roll_bank_or_quit(self):
        # want to know the value of each dice when there's x number of dice.
        
        # want to know the total value of the chosen set of dice
        # want to keep only the dice that exceed the value of each dice for x number of dice.
        self.total_score += 100**1000
        return "b"

    def _enter_dice(self):
        """simulate user entering which dice to keep.
        Defaults to all scoring dice"""

        return super()._enter_dice()

class Klans(BaseBot):
    def _roll_bank_or_quit(self):
        """your logic here"""
        if self.unbanked_points >= 550 or self.dice_remaining <= 2:
            return "b"
        elif self.unbanked_points < 250 and self.dice_remaining == 3:
            return "r"
        return "r"

    def _enter_dice(self):
        """simulate user entering which dice to keep.
        Defaults to all scoring dice"""
        return super()._enter_dice()

class Kirks(BaseBot):
    def _roll_bank_or_quit(self):
        if self.unbanked_points >= 550 or self.dice_remaining <= 2:
            return "b"
        return "r"

    def _enter_dice(self):
        """simulate user entering which dice to keep.
        Defaults to all scoring dice"""

        return super()._enter_dice()

class YourBot(BaseBot):
    def _roll_bank_or_quit(self):
        """your logic here"""
        return "b"

    def _enter_dice(self):
        """simulate user entering which dice to keep.
        Defaults to all scoring dice"""

        return super()._enter_dice()


if __name__ == "__main__":
    num_games = 1000
    # NervousNellie.play(num_games)
    # YourBot.play(num_games)
    Sams.play(num_games)
    # Klans.play(num_games)
    # Chloes.play(num_games)
    #Chloes_test.play(num_games)
    # Kirks.play(num_games)