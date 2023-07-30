import random

MATERIAL_REQUIREMENTS = {
  "Infirmary": {"wood": 50, "stone": 50},
  "Armoury": {"wood": 150, "stone": 150, "iron": 100},
  "Library": {"wood": 100, "stone": 100},
  "Spear": {"wood": 20, "stone": 20},
  "Bow": {"wood": 30, "stone": 30},
  "Upgrade defenses": {"wood": 30, "stone": 30, "iron": 50},
  "Bomb": {"minerals": 150, "chemicals": 120},
  "Armour": {"stone": 20, "iron": 30},
  "Heal": {"medicine": 15},
  "Revive": {"medicine": 60}
}

def subtract_materials(base, building_name, material_requirements):
  if building_name in material_requirements:
    requirements = material_requirements[building_name]
    for material, amount in requirements.items():
        if material in base.storage and base.storage[material] >= amount:
            base.storage[material] -= amount

# This class are essentially the players
class Survivors:

  def __init__(self, name, bomb=[], armour=0, health=100, alive=True, damage=40, end=False):
    self.name = name # String for the survivors name
    self.bomb = bomb # A list of bombs. Bombs can be crafted in an armoury!
    self.armour = armour # Integer symbolising armour
    self.health = health # Integer symbolising health
    self.alive = alive # Boolean value symbolising if the person is alive
    self.damage = damage # Integer symbolising the damage the person can deal
    self.end = end # Yes or No value based on player input
    self.equipped_melee_weapon = None # This determines if a melee weapon is equipped or not
    self.equipped_ranged_weapon = None # This determines if a ranged weapon is equipped or not
    self.combat_skill = None
    self.tracking_skill = None

  # When called lets players "explore". 
  def explore(self, hive, aliens, base):

    # Next two lines randomise the materials gathering
    rand_materials = [1, 3, 5, 6, 7, 8, 10, 13, 15, 17, 20, 22, 25, 27, 30]
    random_num_m = random.randint(0, 30)

    # This logic spawns a new alien everytime the player goes out to explore and also merges everytime there are enough aliens to merge into a bigger alien!
    hive.spawn_aliens(aliens)
    aliens.merge(aliens)
    
    # This combination of coditionals and for loops allow for the materials to be gathered and also check if a player has learned tracking and if so, it lets them collect more materials
    if random_num_m in rand_materials:
      for material in base.storage.keys():
        if material == "wood" or material == "stone":
          base.storage[material] += int(random_num_m)
        elif material == "iron" or material == "medicine":
          base.storage[material] += int(random_num_m / 2)
        elif material == "minerals" or material == "chemicals":
          base.storage[material] += int(random_num_m / 3)
      if self.tracking_skill is not None:
        for material in base.storage.keys():
          if material == "wood" or material == "stone":
            base.storage[material] += int(random_num_m) + 20
          elif material == "iron" or material == "medicine":
            base.storage[material] += int(random_num_m / 2) + 15
          elif material == "minerals" or material == "chemicals":
            base.storage[material] += int(random_num_m / 3) + 10


  # This function allows players to fight with aliens and checks if a player is dead.
  def fight_aliens(self, aliens, player):
    #total_player_damage = self.damage
    aliens.attack(player)
    if not self.alive:
      print(f"\n{self.name} has died! Revive them! ")
    else:
      print(f"\n{self.name} you have survived your HP is at a {self.health}! ")
    



  # This function lets players build buildings.
  def build(self, base, hive, aliens):

    # The while loop ensures that players can pick what to build
    while True:

      # This for loop prints how much do you have of each material!
      for material, amount in base.storage.items():
        print(f"\nYou have {amount} of {material}. ")

      # Here it will promt the player for an input on what do they want to build
      player_input = input(f"""
      What do you want to build {self.name}? Type either:
      - Infirmary (50 wood and 50 stone)
      - Armoury (200 wood ,200 stone and 100 iron)
      - Library (100 wood and 100 stone)
      - Nothing 
      """).capitalize()

      # This conditional statement check the player input, based on that it subtracts the materials, swithces the building to True in the base, spawns 10 basic aliens and merges them
      if player_input== "Infirmary":
        if base.infirmary == True:
          print(f"You aready have an Infirmary! ")
          break
        elif base.storage["wood"] >= 50 and base.storage["stone"] >= 50:
          base.infirmary = True
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          aliens.specs["mid"] += 1
          print(f"\nCongrats you have built an Infirmary now you can heal and revive players! Also there is {aliens.specs['basic']['how_many']} of basic aliens, {aliens.specs['mid']['how_many']} of mid aliens and {aliens.specs['boss']['how_many']} of boss aliens.")
          break
        else:
          print("You don't have enough materials to build an Ifirmary...")
          break
      elif player_input == "Armoury":
        if base.armoury == True:
          print(f"You aready have an Armoury! ")
          break
        elif base.storage["stone"] >= 150 and base.storage["wood"] >= 150 and base.storage["iron"] >= 100:
          base.armoury = True
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          aliens.specs["mid"] += 1
          print(f"\nCongrats you have built an Armoury you can now craft weapons and a bomb! Also there is {aliens.specs['basic']['how_many']} of basic aliens, {aliens.specs['mid']['how_many']} of mid aliens and {aliens.specs['boss']['how_many']} of boss aliens.")
          break
        else:
          print("You don't have enough materials to build an Armoury...")
          break
      elif player_input == "Library":
        if base.library == True:
          print(f"You aready have an Library! ")
          break
        elif base.storage["wood"] >= 100 and base.storage["stone"] >= 100:
          base.library = True
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          aliens.specs["mid"] += 1
          print(f"\nCongrats you have built a Library you can learn new skills now! Also there is {aliens.specs['basic']['how_many']} of basic aliens, {aliens.specs['mid']['how_many']} of mid aliens and {aliens.specs['boss']['how_many']} of boss aliens.")
          break
        else:
          print("You don't have enough materials to build a Library... ")
          break
      elif player_input == "Nothing":
        print(f"\n{self.name} you chose to build nothing! ")
        break
      else:
        print("\nInvalid input... Please type a valid input 'Infirmary', 'Armoury', 'Library or 'Nothing'. ")


  # This function lets players craft gear
  def craft_gear(self, base, armoury, player):

    # Again there is while loop that lets players pick what do they want to craft

    # This prompts the player to input what do they want to build
    player_input = input("""\nWhat do you want to craft? 
    Type either:
    - Spear (adds 20 damage to the player. Costs 20 of wood and stone)
    - Bow (adds 30 damage to the player. Costs 30 of wood and stone)
    - Upgrade defenses (adds 30 to the base defenses. Costs 30 wood and stone and 50 iron)
    - Bomb (adds a bomb to your 'Bomb list' and you can then attack the hive. Costs 150 minerals and 120 chemiscals)
    - Armour (adds 100 armour to the player. Costs 20 stone and 30 iron)
    - Nothing 
    """).capitalize()

    # This conditional statement checks if the requirements for the crafting are met and if so it lets the player build what do they want to build.
    if base.armoury:
      if player_input == "Spear":
        if base.storage["wood"] >= 20 and base.storage["stone"] >= 20:
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          armoury.craft_spear(self)
        else:
          print("You don't have enough materials to craft a Spear...")
      elif player_input == "Bow":
        if base.storage["wood"] >= 30 and base.storage["stone"] >= 30:
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          armoury.craft_bow(self)
        else:
          print("You dno't have enough materials to craft a Bow... ")
      elif player_input == "Upgrade defenses":
        if base.storage["wood"] >= 30 and base.storage["stone"] >= 30 and base.storage["iron"] >= 40:
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          armoury.upgrade_def(base)
        else:
          print("You don't have enough materials to Upgrade defenses...")
      elif player_input == "Bomb":
        if base.storage["minerals"] >= 150 and base.storage["chemicals"] >= 120:
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          armoury.craft_bomb(self)
        else:
          print("You don' have enough materials to craft a Bomb... ")
      elif player_input == "Armour":
        if base.storage["stone"] >= 20 and base.storage["iron"] >= 30:
          subtract_materials(base, player_input, MATERIAL_REQUIREMENTS)
          armoury.craft_armour(self)
        else:
          print("You don't have enough materials to craft Armour...")
      elif player_input == "Nothing":
        print(f"{player.name} chose to craft nothing! ")
      else:
        print(f"Invalid input... Please input 'Spear', 'Bow', 'Upgrade defenses', 'Bomb', 'Armour' or 'Nothing'. ")
    else:
      print("\nYou don't have an Armoury. You can build it for 150 wood, 150 stone and 100 iron. ")


  # This lets the players attack the hive and potentially win the game
  def attack_the_hive(self, aliens, hive):

    # The following statement checks if the requirements for attacking the hive are met
    if "bomb" in self.bomb:

      # This line of code makes the aliens fight the players
      aliens.attack(self, players)

      # The following randomises the success of the mission if the player destroys the hive the won and if not they didn't the might die either way
      if self.alive:
        success = [1, 3, 5, 7, 10]
        rand_num = random.randint(1, 10)
        if rand_num in success and self.bomb.count("bomb") == 2:
          while "bomb" in self.bomb:
            self.bomb.remove("bomb")
          hive.hp = 0
          print(f"\nYou have destroyed the Hive {self.name}! You win!! The remaining aliens die with horriffing screams and you can finally breathe. It's over... ")
        elif rand_num in success and self.bomb.count("bomb") == 1 and hive.hp == 1000:
          self.bomb.remove("bomb")
          hive.hp -= 500
          print(f"\nYou have dealt some damage to the hive {self.name}. One more attack like this and the Hive will fall! Your HP is {self.health}")
        elif rand_num in success and self.bomb.count("bomb") == 1 and hive.hp == 500:
          self.bomb.remove("bomb")
          hive.hp -= 500
          print(f"\nYou have destroyed the Hive {self.name}! You win!! The remaining aliens die with horriffing screams and you can finally breathe. It's over... ")
        elif rand_num not in success:
          self.bomb.remove("bomb")
          print(f"\nYour attack failed... You didn't do any damage to the hive... Your HP is {self.health}")

      elif not self.alive:
        success = [1, 5, 10, 15, 20]
        rand_num = random.randint(1, 20)
        if rand_num in success and self.bomb.count("bomb") == 2:
          while "bomb" in self.bomb:
            self.bomb.remove("bomb")
          print(f"\nYou have destroyed the Hive {self.name}, but you have died trying! The survivors have won!! The remaining aliens die with horriffing screams and you can finally breathe. It's over...")
          hive.hp -= 1000
          for player in players.keys():
            player.end = "Yes"
        elif rand_num in success and self.bomb.count("bomb") == 1 and hive.hp == 1000:
          self.bomb.remove("bomb")
          hive.hp -= 500
          print(f"\nYou have dealt some damage to the hive, but you died trying {self.name}. One more attack like this and the Hive will fall!")
        elif rand_num in success and self.bomb.count("bomb") == 1 and hive.hp == 500:
          self.bomb.remove("bomb")
          hive.hp -= 500
          print(f"\nYou have destroyed the Hive {self.name}, but you have died trying! The survivors have won!! The remaining aliens die with horriffing screams and you can finally breathe. It's over...")
        elif rand_num not in success:
          print(f"\nYou haven't dealt any damage to the hive and you have died in the process {self.name}... ")
    else:
      print("\nYou can't attack the hive because you don't have a bomb...")


  # 
  def save_a_player(self, base, other_player, infirmary): 
    if base.infirmary:
      if base.infirmary == True and base.storage["medicine"] >= 60:
        base.storage["medicine"] -= 60
        infirmary.revive(other_player, players)
      elif base.infirmary == True and base.storage["medicine"] < 60:
        print("\nYou don't have enough medicine!!")
    else:
      print("\nTo heal or save players you need to first build an Infirmary!")
      
      

  def heal_player(self, base, infirmary): 
    if base.infirmary:
      if base.storage["medicine"] >= 15:
        base.storage["medicine"] -= 15
        infirmary.heal(self)
        print(f"\nYour HP is {self.health}!")
      elif base.storage["medicine"] < 15:
        print("\nYou don't have enough medicine...")
    else:
      print("\nTo heal or save players you need to first build an Infirmary!")
    


  def learn(self, base, library):
    if base.library:
      input_p = input("""\nWhat do you want to learn? 
                      1. Combat
                      2. Tracking 
                      """)
      if input_p == "1":
        library.learn_combat(self)
      elif input_p == "2":
        library.learn_tracking(self)
    else:
      print("\nTo learn new skills build a Library first! ")



# This is where players are stored.
players = {}
