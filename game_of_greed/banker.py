class Banker:

  def __init__(self):
    self.balance = 0
    self.shelved = 0

  def shelf(self, points_to_add_to_shelf):
    # want to instead set shelf equal to what we pass in
    self.shelved = points_to_add_to_shelf

  def clear_shelf(self):
    self.shelved = 0

  def bank(self):
    # want to see whats shelved, and set it equal to the balance
    self.balance = self.shelved

    # want to reset shelved to 0
    self.clear_shelf()
