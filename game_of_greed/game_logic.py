import random
from collections import Counter

class GameLogic:
  
  @staticmethod
  def calculate_score(tuple_of_dice):
      
    score = 0
    counts = Counter(tuple_of_dice)

    if tuple_of_dice and set(tuple_of_dice) == set((1, 2, 3, 4, 5, 6)):
        score += 1500
    elif len(counts) == 3 and set(counts.values()) == set((2,)):
        score += 1500
    else:
        for key, count in counts.items():
            if count >= 3:
                if key == 1:
                    score += (count - 2) * 1000
                else:
                    score += (count - 2) * key * 100
            else:
                if key == 5:
                    score += 50 * count
                if key == 1:
                    score += 100 * count

    return score

  @staticmethod
  def roll_dice(amount_of_dice_1_to_6):

    temporary_list = []
    
    for _ in range(amount_of_dice_1_to_6):
        temporary_list.append(random.randint(1, 6))

    return tuple(temporary_list)
    

GameLogic.calculate_score((1, 6, 3, 2, 5, 4))