
class Base:
  def __init__(self, storage={}, defenses=50, main_building=True):
    self.storage = storage # A dictionary contianing type of materials as keys and values as how much
    self.defenses = defenses
    self.main_building = main_building
    self.infirmary = False
    self.armoury = False
    self.library = False


class Infirmary:
  def revive(self, other_player, players):
    for player in players.values():
      if player.name == other_player:
        if player.health == 0:
          player.health = 20
          print(f"{other_player} has been revived! well done {player.name}! ")
        else:
          print("\nTo revive a player they need to be dead first... ")
    
  def heal(self, player):
    if player.health in range(80, 101):
      player.health = 100
    else:
      player.health += 20


class Armoury:
  def craft_spear(self, player):
    if player.equipped_melee_weapon is None:
      player.equipped_melee_weapon = "Spear"
      player.damage += 20
      print(f"{player.name} has crafted a Spear. {player.name} has {player.damage} damage! ")
    else:
      print(f"\n{player.name} already has a spear.")
  
  def craft_bow(self, player):
    if player.equipped_ranged_weapon is None:
      player.equipped_ranged_weapon = "Bow"
      player.damage += 30
      print(f"{player.name} has crafted a Bow. {player.name} has {player.damage} damage! ")
    else:
      print(f"\n{player.name} already has a bow!")

  def upgrade_def(self, base):
    base.defenses += 30
    print(f"\nCongrats you have upgraded your defenses! {base.defenses}!")
  
  def craft_bomb(self, player):
    player.bomb.append("bomb")
    print(f"{player.name} has crafted a Bomb. There are {len(player.bomb)} in the Armoury")
  
  def craft_armour(self, player):
    if player.armour < 100:
      player.armour = 100
      print(f"\n{player.name} has crafted an armour. Armour:{player.armour}")
    else:
      print(f"{player.name} already has a full metal jacket...")
    


class Library:
  def learn_combat(self, player):
    if player.combat_skill is None:
      player.combat_skill = "Combat expert"
      player.damage += 30
      print(f"\n{player.name} is now a combat expert. They have {player.damage} of damage. ")
    else:        
      print("\nThis player already is a combat expert...")

  def learn_tracking(self, player):
    if player.tracking_skill is None:
      player.tracking_skill = "Tracking expert"
      print(f"\n{player.name} is now a tracker. {player.name} has a higher probability of getting more materials! ")
    else:
      print(f"\n{player.name} is already a tracker... ")
  