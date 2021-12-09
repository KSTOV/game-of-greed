from game_of_greed.game_logic import GameLogic
from game_of_greed.banker import Banker
import sys

welcome_message = " "

# **************************************************
# ***                                            ***
# ***   Welcome to Won Direction's game of Foo   ***
# ***                                            ***
# **************************************************
# We hope you Won many points today. To start yell 'START!'

class Game:

  def __init__(self):
    self.round_counter = 1
    self.dice_qty = 6
    self.banker = Banker()

  def default_roller(self):
    GameLogic.roll_dice(self.dice_qty)

  def play(self, roller = GameLogic.roll_dice):
    print("Welcome to Game of Greed")
    print("(y)es to play or (n)o to decline")
    response = input("> ")

    if response == "n":
      print("OK. Maybe another time")
    elif response == "y":
      self.run_game(roller)

  def run_game(self, roller):

    print(f"Starting round {self.round_counter}")
    while True:

      print(f"Rolling {self.dice_qty} dice...")

      # step 2: roll dice for that current player
      rolled_dice = roller(self.dice_qty)
      formatted_dice = str(rolled_dice).strip("([])").replace(", ", " ")  # (4, 4, 5, 2, 3, 1) -> *** 4 4 5 2 3 1 ***
      print("*** " + formatted_dice + " ***") 
      
      # step 2.2: show what dice were rolled
      if GameLogic.calculate_score(rolled_dice) == 0:
          print("Farkled")
          self.round_counter += 1
          print(f"Starting round {self.round_counter}")
          continue
      
      print("Enter dice to keep, or (q)uit:")
      response_unclean = input("> ")

      response = response_unclean.replace(" ","")

      
      if response == "q":
        print(f"Thanks for playing. You earned {self.banker.balance} points")
        sys.exit()

      response_to_tuple = tuple([int(char) for char in response])

      GameLogic.validate_keepers(rolled_dice,response_to_tuple)
    
      # tally score and then bank, reroll, or quit
      response_list = tuple(map(int, list(response)))
      score = GameLogic.calculate_score(response_list) ## response = "1234" --> [1, 2, 3, 4] --> (1, 2, 3, 4)
      self.banker.shelf(score)
      self.dice_qty -= len(response_list)
      print(f"You have {self.banker.shelved} unbanked points and {self.dice_qty} dice remaining")
      print("(r)oll again, (b)ank your points or (q)uit:")
      response = input("> ")

      # bank points
      if response == "b":
        print(f"You banked {self.banker.shelved} points in round {self.round_counter}")
        self.banker.bank()
        self.dice_qty = 6
        print(f"Total score is {self.banker.balance} points")
        self.round_counter += 1
        print(f"Starting round {self.round_counter}")

      # reroll                
      elif response == "r":
        if self.dice_qty == 0:
          self.dice_qty = 6
        continue # reroll with the remaining dice on the board
      
      # quit
      elif response == "q":
        print(f"Thanks for playing. You earned {self.banker.balance} points")
        sys.exit()


if __name__ == "__main__":
  game = Game()
  game.play()