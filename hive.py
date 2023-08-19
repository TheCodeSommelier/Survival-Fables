# The alien hive 🧠

from aliens import AlienType
class Hive:
  def __init__(self):
    self.number_of = 1
    self.hp = 1000

  def spawn_aliens(self, aliens):
    aliens.aliens[AlienType.BASIC].how_many += 1
    print(f"1 Basic alien was spawned!")