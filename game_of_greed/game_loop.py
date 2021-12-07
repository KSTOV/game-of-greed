from game_of_greed.game_logic import GameLogic

welcome_message = """
**************************************************
***                                            ***
***   Welcome to Won Direction's game of Foo   ***
***                                            ***
**************************************************
We hope you Won many points today. To start yell 'START!'
"""

def start_game():
   response = input(welcome_message)
   if response == "START!":
     run_game()

def run_game():
  while True:
    # step 2: roll dice for that current player
    rolled_dice = GameLogic.roll_dice(6)

    # step 2.2: show what dice were rolled
    if GameLogic.calculate_score(rolled_dice) == 0:
        print("Farkled")
        continue
    

    # step 2.5: if no scoring dice, farkle, and switch turns


    # step 3: choose dice to put on shelf (requires user input())


# welcome message before game starts
start_game()

# want want a game loop that loops through the steps of the game. condition: continue_playing and score <= 10k
    # step 1: set the current player. skip this for now because single player game without computer/player2
    # step 2: roll dice for that current player
    # step 2.2: show what dice were rolled
    # step 2.5: if no scoring dice, farkle, and switch turns
    # step 3: choose dice to put on shelf (requires user input())
    # step 4: calculate score based on dice in shelf
    # step 5: decide to bank or reroll (requires user input()).
        # if reroll: go back to step 2, except set number of dice to 6 minus dice on shelf or set to 6 if shelf is full
        # else if bank: add to bank 
            # if score >= 10k, player wins
            # else: switch turns

# ask to play again (requires user input())
