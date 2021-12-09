from game_of_greed.game_logic import GameLogic
from game_of_greed.banker import Banker
import sys

class Game:
    def __init__(self):
        self.round_counter = 0
        self.dice_qty = 6
        self.banker = Banker()

    def welcome(self):
        print("Welcome to Game of Greed")

    def play(self, roller = GameLogic.roll_dice):
        self.welcome()
        print("(y)es to play or (n)o to decline")
        response = input("> ")
        if response == "y":
            self.run_game(roller)
        elif response == "n":
            print("OK. Maybe another time")
            self.quit()
        else:
            return self.play(roller)

    def run_game(self, roller):
        self.start_round(roller)

    def roll_loop(self, roller):
        rolled_dice = self.roll(roller)
        selected_dice = self.select_dice_and_validate(rolled_dice, roller)
        self.calculate_score(selected_dice)
        self.show_score_and_dice_qty()
        self.prompt_and_handle_bank_reroll_or_quit(roller)

    def start_round(self, roller):
        self.round_counter += 1
        self.dice_qty = 6
        self.banker.clear_shelf()
        print(f"Starting round {self.round_counter}")
        self.roll_loop(roller)

    def roll(self, roller):
        print(f"Rolling {self.dice_qty} dice...")
        rolled_dice = roller(self.dice_qty)
        self.show_rolled_dice(rolled_dice)
        return rolled_dice

    def show_rolled_dice(self, rolled_dice):
        formatted_dice = str(rolled_dice).strip("([])").replace(", ", " ")  # (4, 4, 5, 2, 3, 1) -> *** 4 4 5 2 3 1 ***
        print("*** " + formatted_dice + " ***")

    def select_dice_and_validate(self, rolled_dice, roller):

        if GameLogic.calculate_score(rolled_dice) == 0:
            print("****************************************")
            print("**        Zilch!!! Round over         **")
            print("****************************************")
            self.banker.clear_shelf()
            self.bank_points(roller)

        else:
            print("Enter dice to keep, or (q)uit:")
            response = input("> ")
            if response:
                response = response.replace(" ", "")
            else:
                self.select_dice_and_validate(rolled_dice, roller)

            if response == "q":
                print(f"Thanks for playing. You earned {self.banker.balance} points")
                self.quit()

            response_to_tuple = tuple([int(char) for char in response])
            isValid = GameLogic.validate_input(rolled_dice, response_to_tuple)
            if isValid:
                return response_to_tuple
            else:
                print("Cheater!!! Or possibly made a typo...")
                self.show_rolled_dice(rolled_dice)
                return self.select_dice_and_validate(rolled_dice, roller)

    def calculate_score(self, selected_dice):
        score = GameLogic.calculate_score(selected_dice) ## response = "1234" --> [1, 2, 3, 4] --> (1, 2, 3, 4)
        self.banker.shelf(score)
        self.dice_qty -= len(selected_dice)
        return score

    def show_score_and_dice_qty(self):
        print(f"You have {self.banker.shelved} unbanked points and {self.dice_qty} dice remaining")

    def prompt_and_handle_bank_reroll_or_quit(self, roller):
        print("(r)oll again, (b)ank your points or (q)uit:")
        bank_reroll_or_quit = input("> ").replace(" ", "")

        if bank_reroll_or_quit == "q":
            print(f"Thanks for playing. You earned {self.banker.balance} points")
            self.quit()
        elif bank_reroll_or_quit == "r":
            if self.dice_qty == 0:
                self.dice_qty = 6
                self.roll_loop(roller)
            else:
                self.roll_loop(roller)
        elif bank_reroll_or_quit == "b":
            self.bank_points(roller)

    def bank_points(self, roller):
        print(f"You banked {self.banker.shelved} points in round {self.round_counter}")
        self.banker.bank()
        print(f"Total score is {self.banker.balance} points")
        
        if self.banker.balance >= 10000:
            print("WINNER")
        else:
            self.start_round(roller)

    def quit(self):
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.play()