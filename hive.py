# The alien hive 🧠
class Hive:
  def __init__(self):
    self.number_of = 1
    self.hp = 1000

  def spawn_aliens(self, aliens):
    aliens.specs["basic"]["how_many"] += 1