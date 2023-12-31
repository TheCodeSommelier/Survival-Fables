import random
from enums import *



MATERIAL_REQUIREMENTS = {
  "Infirmary": {"wood": 50, "stone": 50},
  "Armoury": {"wood": 150, "stone": 150, "iron": 100},
  "Library": {"wood": 100, "stone": 100},
  "Spear": {"wood": 20, "stone": 20},
  "Bow": {"wood": 30, "stone": 30},
  "Knife": {"iron": 50},
  "Gun": {"iron": 80, "chemicals": 50},
  "Upgrade defenses": {"wood": 30, "stone": 30, "iron": 50},
  "Bomb": {"minerals": 150, "chemicals": 120},
  "Armour": {"stone": 20, "iron": 30},
  "Heal": {"medicine": 15},
  "Revive": {"medicine": 60}
}

MATERIAL_MULTIPLIER = {
  "wood": 1,
  "stone": 1,
  "iron": 0.8,
  "medicine": 1,
  "minerals": 0.5,
  "chemicals": 0.4
}


def subtract_materials(base, building_name, material_requirements):
  if building_name in material_requirements:
    requirements = material_requirements[building_name]
    for material, amount in requirements.items():
        if material in base.storage and base.storage[material] >= amount:
            base.storage[material] -= amount


def gather_materials(base):
  numbers = [1, 3, 5, 6, 7, 8, 10, 13, 15, 17, 20, 22, 25, 27, 30]
  picked_number = random.randint(0, 30)
  if picked_number in numbers:
    for material in base.storage.keys():
      multiplier = MATERIAL_MULTIPLIER[material]
      base.storage[material] += int(picked_number * multiplier)

# This class are essentially the players
class Survivors:
  def __init__(self, name, bomb=[], armour=0, health=100, damage=40, end=False):
    self.name = name # String for the survivors name
    self.bomb = bomb # A list of bombs. Bombs can be crafted in an armoury!
    self.armour = armour # Integer symbolising armour
    self.health = health # Integer symbolising health
    self.damage = damage # Integer symbolising the damage the person can deal
    self.end = end # Yes or No value based on player input
    self.equipped_melee_weapon = None # This determines if a melee weapon is equipped or not
    self.equipped_ranged_weapon = None # This determines if a ranged weapon is equipped or not
    self.combat_skill = None
    self.tracking_skill = None
    self.update_alive_status()


  def update_alive_status(self):
    self.alive = self.health > 0


  def explore(self, hive, aliens, base):
    hive.spawn_aliens(aliens)
    aliens.merge()
    gather_materials(base)


  def fight_aliens(self, aliens, player):
    aliens.defend(player)
    self.update_alive_status()
    if not self.alive:
      print(f"\n{self.name} has died! Revive them! ")
    else:
      print(f"\n{self.name} you have survived your HP is at a {self.health}! ")


  def build(self, base, aliens, hive):
    while True:

      for material, amount in base.storage.items():
        print(f"\nYou have {amount} of {material}. ")

      player_input = input(f"""
      What do you want to build {self.name}? Type either:
      - Infirmary (50 wood and 50 stone)
      - Armoury (200 wood, 200 stone and 100 iron)
      - Library (100 wood and 100 stone)
      - Nothing
      """).capitalize()

      if player_input== "Infirmary":
        if base.infirmary == True:
          print(f"You already have an Infirmary! ")
          break
        elif base.storage["wood"] >= 50 and base.storage["stone"] >= 50:
          base.infirmary = True
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          for i in range(0, 3):
            hive.spawn_aliens(aliens)
          print(f"\nCongrats you have built an Infirmary now you can heal and revive players! ")
          break
        else:
          print("You don't have enough materials to build an Infirmary...")
          break
      elif player_input == "Armoury":
        if base.armoury == True:
          print(f"You already have an Armoury! ")
          break
        elif base.storage["stone"] >= 150 and base.storage["wood"] >= 150 and base.storage["iron"] >= 100:
          base.armoury = True
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          for i in range(0, 3):
            hive.spawn_aliens(aliens)
          print(f"\nCongrats you have built an Armoury you can now craft weapons and a bomb! ")
          break
        else:
          print("You don't have enough materials to build an Armoury...")
          break
      elif player_input == "Library":
        if base.library == True:
          print(f"You already have a Library! ")
          break
        elif base.storage["wood"] >= 100 and base.storage["stone"] >= 100:
          base.library = True
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          for i in range(0, 3):
            hive.spawn_aliens(aliens)
          print(f"\nCongrats you have built a Library you can learn new skills now! ")
          break
        else:
          print("You don't have enough materials to build a Library... ")
          break
      elif player_input == "Nothing":
        print(f"\n{self.name} you chose to build nothing! ")
        break
      else:
        print("\nInvalid input... Please type a valid input 'Infirmary', 'Armoury', 'Library or 'Nothing'. ")


  def craft_gear(self, base, armoury, player):
    player_input = input("""\nWhat do you want to craft?
    Type either:
    - Spear (adds 20 damage to the player. Costs 20 of wood and stone)
    - Bow (adds 30 damage to the player. Costs 30 of wood and stone)
    - Knife (adds 50 damage to the player. Costs 50 iron.)
    - Gun (adds 80 damage to the player. Costs 80 iron and 30 chemicals)
    - Upgrade defenses (adds 30 to the base defenses. Costs 30 wood and stone and 50 iron)
    - Bomb (adds a bomb to your 'Bomb list' and you can then attack the hive. Costs 150 minerals and 120 chemicals)
    - Armour (adds 100 armor to the player. Costs 20 stone and 30 iron)
    - Nothing
    """).capitalize()

    if base.armoury:
      if player_input == "Spear":
        if base.storage["wood"] >= 20 and base.storage["stone"] >= 20:
          armoury.craft_weapon(player, "Spear", 20, base)
        else:
          print("You don't have enough materials to craft a Spear...")
      elif player_input == "Bow":
        if base.storage["wood"] >= 30 and base.storage["stone"] >= 30:
          armoury.craft_weapon(player, "Bow", 30, base)
        else:
          print("You don't have enough materials to craft a Bow... ")
      elif player_input == "Knife":
        if base.storage["iron"] >= 50:
          armoury.craft_weapon(player, "Knife", 50, base)
      elif player_input == "Gun":
        if base.storage["iron"] >= 80 and base.storage["chemicals"] >= 30:
          armoury.craft_weapon(player, "Gun", 80, base)
      elif player_input == "Upgrade defenses":
        if base.storage["wood"] >= 30 and base.storage["stone"] >= 30 and base.storage["iron"] >= 40:
          armoury.upgrade_defenses(base)
        else:
          print("You don't have enough materials to Upgrade defenses...")
      elif player_input == "Bomb":
        if base.storage["minerals"] >= 150 and base.storage["chemicals"] >= 120:
          armoury.craft_weapon(player, "Bomb", 0, base)
        else:
          print("You don't have enough materials to craft a Bomb... ")
      elif player_input == "Armour":
        if base.storage["stone"] >= 20 and base.storage["iron"] >= 30:
          armoury.craft_armour(player, 100, base)
        else:
          print("You don't have enough materials to craft Armour...")
      elif player_input == "Nothing":
        print(f"{player.name} chose to craft nothing! ")
      else:
        print(f"Invalid input... Please input 'Spear', 'Bow', 'Upgrade defenses', 'Bomb', 'Armour', or 'Nothing'. ")
    else:
      print("\nYou don't have an Armoury. You can build it for 150 wood, 150 stone, and 100 iron. ")


  def attack_the_hive(self, aliens, hive, player):
    if "Bomb" not in self.bomb:
      print(f"{player.name}, you can't attack the hive because you don't have a bomb...")
      return

    aliens.attack(self)
    self.update_alive_status()
    if not self.alive:
        success = [1, 3, 5, 7, 8, 9, 10]
        rand_num = random.randint(1, 10)
        if rand_num in success and self.bomb.count("bomb") == 2:
            while "Bomb" in self.bomb:
                self.bomb.remove("Bomb")
            hive.hp -= 1000
            print(f"\nYou have destroyed the Hive {self.name}, but you have died trying! The survivors have won!! The remaining aliens die with horrifying screams and you can finally breathe. It's over...")
        elif rand_num in success and self.bomb.count("bomb") == 1 and hive.hp == 1000:
            self.bomb.remove("Bomb")
            hive.hp -= 500
            print(f"\nYou have dealt some damage to the hive, but you died trying {self.name}. One more attack like this and the Hive will fall!")
        elif rand_num in success and self.bomb.count("bomb") == 1 and hive.hp == 500:
            self.bomb.remove("Bomb")
            hive.hp -= 500
            print(f"\nYou have destroyed the Hive {self.name}, but you have died trying! The survivors have won!! The remaining aliens die with horrifying screams. It's over...")
        elif rand_num not in success:
            self.bomb.remove("Bomb")
            print(f"\nYour attack failed... You didn't do any damage to the hive... And you died...")
    else:
        success = [1, 5, 10, 15, 20]
        rand_num = random.randint(1, 20)
        if rand_num in success and self.bomb.count("Bomb") == 2:
          while "Bomb" in self.bomb:
            self.bomb.remove("Bomb")
          hive.hp -= 1000
          print(f"\nYou have destroyed the Hive {self.name}! You win!! The remaining aliens die with horrifying screams and you can finally breathe. It's over... ")
        elif rand_num in success and self.bomb.count("Bomb") == 1 and hive.hp == 1000:
          self.bomb.remove("Bomb")
          hive.hp -= 500
          print(f"\nYou have dealt some damage to the hive {self.name}. One more attack like this and the Hive will fall! Your HP is {self.health}")
        elif rand_num in success and self.bomb.count("Bomb") == 1 and hive.hp == 500:
            self.bomb.remove("Bomb")
            hive.hp -= 500
            print(f"\nYou have destroyed the Hive {self.name}! You win!! The remaining aliens die with horrifying screams and you can finally breathe. It's over... ")
        elif rand_num not in success:
            self.bomb.remove("Bomb")
            print(f"\nYour attack failed... You didn't do any damage to the hive... Your HP is {self.health}")


  def save_a_player(self, base, other_player, infirmary):
    if base.infirmary:
      if base.infirmary == True and base.storage["medicine"] >= 60:
        base.storage["medicine"] -= 60
        infirmary.revive(other_player, players)
        self.update_alive_status()
      elif base.infirmary == True and base.storage["medicine"] < 60:
        print("\nYou don't have enough medicine!!")
    else:
      print("\nTo heal or save players you need to first build an Infirmary!")


  def heal_player(self, base, infirmary):
    if base.infirmary:
      if base.storage["medicine"] >= 15:
        base.storage["medicine"] -= 15
        infirmary.heal(self)
        self.update_alive_status()
        print(f"\nYour HP is {self.health}!")
      elif base.storage["medicine"] < 15:
        print("\nYou don't have enough medicine...")
    else:
      print("\nTo heal or save players you need to first build an Infirmary!")


  def learn(self, base, library):
    if base.library:
      input_p = input("""\nWhat do you want to learn?
                      1. Combat (Adds 30 damage to your overall damage)
                      2. Tracking (Increases the probability of you finding materials)
                      """)
      if input_p == "1":
        library.learn_combat(self)
      elif input_p == "2":
        library.learn_tracking(self)
    else:
      print("\nTo learn new skills build a Library first! ")

# This is where the instances of Survivors (players) are stored.
players = {}
