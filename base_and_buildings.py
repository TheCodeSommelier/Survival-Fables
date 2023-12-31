
from players import *


class Base:
  def __init__(self, storage={}, defenses=50, main_building=True):
    self.storage = storage # A dictionary contianing type of materials as keys and values as how much
    self.defenses = defenses
    self.main_building = main_building
    self.infirmary = False
    self.armoury = False
    self.library = False


class Building:
  def craft_weapon(self, player, weapon_name, damage_bonus, base):
    if weapon_name not in player.bomb and weapon_name not in [player.equipped_melee_weapon, player.equipped_ranged_weapon]:
      if weapon_name in MATERIAL_REQUIREMENTS and all(material in base.storage and base.storage[material] >= amount for material, amount in MATERIAL_REQUIREMENTS[weapon_name].items()):
        for material, amount in MATERIAL_REQUIREMENTS[weapon_name].items():
          base.storage[material] -= amount

        if weapon_name in {"Spear", "Knife", "Bow", "Gun"}:
          if player.equipped_melee_weapon == "Spear":
            damage_bonus -= 20
          elif player.equipped_ranged_weapon == "Bow":
            damage_bonus -= 30

          if weapon_name in {"Spear", "Knife"}:
            player.equipped_melee_weapon = weapon_name
          elif weapon_name in {"Bow", "Gun"}:
            player.equipped_ranged_weapon = weapon_name

          if weapon_name:
            player.damage += damage_bonus

          print(f"{player.name} has crafted a {weapon_name}. Their damage is {player.damage}.")
        else:
          player.bomb.append(weapon_name)
          print(f"{player.name} has crafted a {weapon_name}. There are {len(player.bomb)} {weapon_name}s in the Armoury! ")
      else:
        print(f"You don't have enough materials to craft {weapon_name}...")
    else:
      print(f"{player.name} already has a {weapon_name}...")

  def craft_armour(self, player, armour_value, base):
    if player.armour < armour_value:
      if "Armour" in MATERIAL_REQUIREMENTS and all(material in base.storage and base.storage[material] >= amount for material, amount in MATERIAL_REQUIREMENTS["Armour"].items()):
        for material, amount in MATERIAL_REQUIREMENTS["Armour"].items():
          base.storage[material] -= amount

        player.armour = armour_value
        print(f"{player.name} has crafted an Armour! {player.name} has {player.armour} of Armour! ")
      else:
        print(f"You didn't have enough materials to craft Armour! ")
    else:
      print(f"{player.name} already has a full metal jacket...")

  def upgrade_defenses(self, base):
    if all(material in base.strage and base.storage[material] >= amount for material, amount in MATERIAL_REQUIREMENTS["Upgrade defenses"].items()):
      for material, amount in MATERIAL_REQUIREMENTS["Upgrade defenses"].items():
        base.storage[material] -= amount
      base.defenses += 30
      print(f"Congrats! You have upgraded your defenses! Base defenses: {base.defenses}")
    else:
      print(f"You don't have enough materials to upgrade your defenses... ")

class Infirmary(Building):
  def revive(self, other_player, players):
    for player in players.values():
      if player.name == other_player:
        if player.health == 0:
          player.health = 20
          players[other_player].alive = True
          print(f"You have revived {other_player}! Well done! ")
        else:
          print("\nTo revive a player they need to be dead first... ")

  def heal(self, player):
    if player.health in range(80, 101):
      player.health = 100
    else:
      player.health += 20

class Armoury(Building):
  pass

class Library(Building):
  def learn_combat(self, player):
    if player.combat_skill == None:
      player.combat_skill = "Combat expert"
      player.damage += 30
      print(f"\n{player.name} is now a combat expert. They have {player.damage} of damage. ")
    else:
      print("\nThis player already is a combat expert...")

  def learn_tracking(self, player):
    if player.tracking_skill == None:
      player.tracking_skill = "Tracking expert"
      print(f"\n{player.name} is now a tracker. {player.name} has a higher probability of getting more materials! ")
    else:
      print(f"\n{player.name} is already a tracker... ")
