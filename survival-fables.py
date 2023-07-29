# This is imports the python random package into the code
import random

# This class are essentially the players
class Survivors:

  def __init__(self, name, bomb=[], armour=0, health=100, alive=True, damage=40, end="No"):
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
    hive.spawn_aliens()
    aliens.merge()
    
    # This combination of coditionals and for loops allow for the materials to be gathered and also check if a player has learned tracking and if so, it lets them collect more materials
    if random_num_m in rand_materials:
      for material in base.storage.keys():
        if material == "wood" or material == "stone":
          base.storage[material] += random_num_m
        elif material == "iron" or material == "medicine":
          base.storage[material] += int(random_num_m / 2)
        elif material == "minerals" or material == "chemicals":
          base.storage[material] += int(random_num_m / 3)
      if "tracking" in self.skills:
        for material in base.storage.keys():
          if material == "wood" or material == "stone":
            base.storage[material] += random_num_m + 20
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
  def build(self, base):

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
        if base.storage["wood"] >= 50 and base.storage["stone"] >= 50:
          base.infirmary = True
          base.storage["wood"] -= 50
          base.storage["stone"] -= 50
          for i in range(10):
            hive.spawn_aliens()
          aliens.merge()
          print(f"\nCongrats you have built an Infirmary now you can heal and revive players! Also there is {aliens.specs['basic']['how_many']} of basic aliens, {aliens.specs['mid']['how_many']} of mid aliens and {aliens.specs['boss']['how_many']} of boss aliens.")
          break
        elif base.storage["wood"] < 50 or base.storage["stone"] < 50:
          print("You don't have enough materials to build an Ifirmary...")
          break
      elif player_input == "Armoury":
        if base.storage["stone"] >= 150 and base.storage["wood"] >= 150 and base.storage["iron"] >= 100:
          base.armoury = True
          base.storage["wood"] -= 150
          base.storage["stone"] -= 150
          base.storage["iron"] -= 100
          for i in range(10):
            hive.spawn_aliens()
          aliens.merge()
          print(f"\nCongrats you have built an Armoury you can now craft weapons and a bomb! Also there is {aliens.specs['basic']['how_many']} of basic aliens, {aliens.specs['mid']['how_many']} of mid aliens and {aliens.specs['boss']['how_many']} of boss aliens.")
          break
        elif base.storage["stone"] < 150 or base.storage["iron"] < 100:
          print("You don't have enough materials to build an Armoury...")
          break
      elif player_input == "Library":
        if base.storage["wood"] >= 100 and base.storage["stone"] >= 100:
          base.library = True
          base.storage["wood"] -= 100
          base.storage["stone"] -= 100
          for i in range(10):
            hive.spawn_aliens()
          aliens.merge()
          print(f"\nCongrats you have built a Library you can learn new skills now! Also there is {aliens.specs['basic']['how_many']} of basic aliens, {aliens.specs['mid']['how_many']} of mid aliens and {aliens.specs['boss']['how_many']} of boss aliens.")
          break
        elif base.storage["wood"] < 100 or base.storage["stone"] < 100:
          print("You don't have enough materials to build a Library... ")
          break
      elif player_input == "Nothing":
        print(f"\n{self.name} you chose to build nothing! ")
        break
      else:
        print("\nInvalid input... Please type a valid input 'Infirmary', 'Armoury', 'Library or 'Nothing'. ")


  # This function lets players craft gear
  def craft_gear(self, base, armoury):

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
          base.storage["wood"] -= 20
          base.storage["stone"] -= 20
          armoury.craft_spear(self)
        else:
          print("You don't have enough materials to craft a Spear...")
      elif player_input == "Bow":
        if base.storage["wood"] >= 30 and base.storage["stone"] >= 30:
          base.storage["wood"] -= 30
          base.storage["stone"] -= 30
          armoury.craft_bow(self)
        else:
          print("You dno't have enough materials to craft a Bow... ")
      elif player_input == "Upgrade defenses":
        if base.storage["wood"] >= 30 and base.storage["stone"] >= 30 and base.storage["iron"] >= 40:
          base.storage["wood"] -= 30
          base.storage["stone"] -= 30
          base.storage["iron"] -= 50
          armoury.upgrade_def(base)
        else:
          print("You don't have enough materials to Upgrade defenses...")
      elif player_input == "Bomb":
        if base.storage["minerals"] >= 150 and base.storage["chemicals"] >= 120:
          base.storage["minerals"] -= 150
          base.storage["chemicals"] -= 120
          armoury.craft_bomb(self)
        else:
          print("You don' have enough materials to craft a Bomb... ")
      elif player_input == "Armour":
        if base.storage["stone"] >= 20 and base.storage["iron"] >= 30:
          base.storage["stone"] -= 20
          base.storage["iron"] -= 30
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
      aliens.attack(self)

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
        infirmary.revive(other_player)
        print(f"{other_player} has been revived! {other_player}! ")
      elif base.infirmary == True and base.storage["medicine"] < 60:
        print("\nYou don't have enough medicine!!")
    else:
      print("\nTo heal or save players you need to first build an Infirmary!")
      
      

  def heal_player(self, base, infirmary): 
    if base.infirmary:
      if base.storage["medicine"] >= 15:
        base.storage["medicine"] -= 15
        infirmary.heal(self)
        print(f"\nThe {self.name} HP is {self.health}!")
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
          

    
      
# Works!!!
class Base:
  def __init__(self, storage={}, defenses=50, main_building=True):
    self.storage = storage # A dictionary contianing type of materials as keys and values as how much
    self.defenses = defenses
    self.main_building = main_building
    self.infirmary = False
    self.armoury = False
    self.library = False


class Infirmary:
  
  def revive(self, other_player):
    for player in players.values():
      if player.name == other_player:
        if player.health == 0:
          player.health = 20
        else:
          print("\nTo revive a player they need to be dead first... ")
    
      
  def heal(self, player):
    if player.health in range(80, 101):
      player.health = 100
    else:
      player.health += 20


class Armoury:
  
  def craft_spear(self, player): # wood + stone
    if player.equipped_melee_weapon is None:
      player.equipped_melee_weapon = "Spear"
      player.damage += 20
      print(f"{player.name} has crafted a Spear. {player.name} has {player.damage} damage! ")
    else:
      print(f"\n{player.name} already has a spear.")
  
  def craft_bow(self, player): # wood + stone
    if player.equipped_ranged_weapon is None:
      player.equipped_ranged_weapon = "Bow"
      player.damage += 30
      print(f"{player.name} has crafted a Bow. {player.name} has {player.damage} damage! ")
    else:
      print(f"\n{player.name} already has a bow!")

  def upgrade_def(self, base): # lots of iron and stone
    base.defenses += 30
    print(f"\nCongrats you have upgraded your defenses! {base.defenses}!")
  
  def craft_bomb(self, player): # minerals + chemicals
    player.bomb.append("bomb")
    print(f"{player.name} has crafted a Bomb. There are {len(player.bomb)} in the Armoury")
  
  def craft_armour(self, player): # stone + iron
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
  

# Aliens (aka enemies) 👽
class Aliens:
  
  def __init__(self, specs):
    self.specs = specs # Is a dictionary of type of alien as keys (basic, mid, boss) and a dictionary as a value storing color, size and how many as keys and corresponding values as values.

  
  def merge(self): # Based on a result of the merge we'll create a color size attr
    if self.specs["basic"]["how_many"] >= 10:
      self.specs["mid"]["how_many"] += 1
      self.specs["basic"]["how_many"] -= 10
      print(f"\nAliens now have {aliens.specs['mid']['how_many']} of a Mid level alien. Start killing them before they make a Boss!")
    elif self.specs["mid"]["how_many"] >= 10:
      self.specs["boss"]["how_many"] += 1
      self.specs["mid"]["how_many"] -= 10
      print(f"\nAliens now have {aliens.specs['boss']['how_many']} of Boss alien. Good luck out there!")
    else:
      print("\nAliens did not have enough to merge into a bigger one!")


  def die_or_hurt(self, total_player_damage):
    for alien_type, alien_info in aliens.specs.items():
      if alien_info["how_many"] > 0:
        if alien_type == "boss":
          remainder = total_player_damage // (alien_info["health"] * alien_info["how_many"])
          if remainder > alien_info["how_many"]:
            alien_info["how_many"] = 0
          else:
            alien_info["how_many"] -= remainder
        elif alien_type == "mid":
          remainder = total_player_damage // (alien_info["health"] * alien_info["how_many"])
          if remainder > alien_info["how_many"]:
            alien_info["how_many"] = 0
          else:
            alien_info["how_many"] -= remainder
        elif alien_type == "basic":
          remainder = total_player_damage // (alien_info["health"] * alien_info["how_many"])
          if remainder > alien_info["how_many"]:
            alien_info["how_many"] = 0
          else:
            alien_info["how_many"] -= remainder

  
  def die_or_hurt_base(self, total_base_damage):
    for alien_type, alien_info in aliens.specs.items():
      if alien_info["how_many"] > 0:
        if alien_type == "boss":
          remainder = total_base_damage // alien_info["health"]
          if remainder > alien_info["how_many"]:
            alien_info["how_many"] = 0
          else:
            alien_info["how_many"] -= remainder
        elif alien_type == "mid":
          remainder = total_base_damage // alien_info["health"]
          if remainder > alien_info["how_many"]:
            alien_info["how_many"] = 0
          else:
            alien_info["how_many"] -= remainder
        elif alien_type == "basic":
          remainder = total_base_damage // alien_info["health"]
          if remainder > alien_info["how_many"]:
            alien_info["how_many"] = 0
          else:
            alien_info["how_many"] -= remainder
  

  def attack(self, player): 
    # Total damage dealt by aliens
    total_alien_damage = 0
    for alien_type, alien_info in self.specs.items():
      total_alien_damage += alien_info["damage"] * alien_info["how_many"]


    # This calculates the respective damage to the armour of the players if any
    remainder = 0
    if player.armour > 0:
      if player.armour >= total_alien_damage:
        player.armour -= total_alien_damage
      else:
        remainder = player.armour - total_alien_damage
        player.armour = 0
        player.health -= remainder
        print(f"\nYou took some hits {player.name} your HP is {player.health}. You should go heal... ")
    else: # damage dealt to the HP
      player.health -= total_alien_damage
      if player.health <= 0:
        player.health = 0
        player.alive = False
        print(f"\n{player.name} died... Revive them!")


    # This calculates the damage of the players and subtracts the damage from alien health
    total_player_damage = 0
    for instance in players.values():
        total_player_damage += instance.damage

    self.die_or_hurt(total_player_damage)
    
  
  def attack_base(self, base, player):
    total_base_damage = base.defenses
    total_alien_damage = 0
    for alien_type, alien_info in aliens.specs.items():
      total_alien_damage += alien_info["damage"] * alien_info["how_many"]

    self.die_or_hurt_base(total_base_damage)
    
    if base.defenses > 0:
      rem_damage = min(base.defenses, total_alien_damage)
      base.defenses -= rem_damage
      total_alien_damage -= total_alien_damage
      print(f"\nGood you fought them off! You have {base.defenses} of your defense left!")

      for alien_type, alien_info in aliens.specs.items():
        print(f"\nNumber of {alien_type} aliens left: {alien_info['how_many']}!")
      
    else:
      for material in base.storage.keys():
        base.storage[material] /= 2
      print("\nYour base defenses have been destroyed... FIGHT FOR YOUR LIFE!")
      self.attack(player)


# A solo standing function that initialises a random base attack
def initialize_rand_attack(base, aliens, player):
  random_attack = [16, 33, 12, 42, 22]
  random_number = random.randint(1, 50)
  if random_number in random_attack:
    aliens.attack_base(base, player)

      


# The alien hive 🧠
class Hive:
  def __init__(self):
    self.number_of = 1
    self.hp = 1000

  def spawn_aliens(self):
    aliens.specs["basic"]["how_many"] += 1


# THE WORLD!! 🌎
# To use / build from 🪵 🪨 ⛏️ 🧪
class Materials:
  
  def __init__(self, type):
    self.type = type


# Initializing materials in the world
wood = Materials("wood")
stone = Materials("stone")
iron = Materials("iron")
minerals = Materials("minerals")
chemicals = Materials("chemicals")
medicine = Materials("medicine")

# Initializing base 
base = Base({
  "wood": 1000,
  "stone": 1000,
  "iron": 1000,
  "medicine": 1000,
  "minerals": 1000,
  "chemicals": 1000
})

# Initializing buildings
infirmary = Infirmary()
armoury = Armoury()
library = Library()

# Initializing hive
hive = Hive()

# Initilizing aliens
aliens = Aliens({
  "basic": {"how_many": 1, "damage": 10, "health": 10},
  "mid": {"how_many": 0, "damage": 20, "health": 60},
  "boss": {"how_many": 0, "damage": 70, "health": 200}
})


# Starting message what players see when they start the game!
print("""\nWelcome to 'Survival Fables'!!
\nThe world has been invaded by hostile aliens! You have to fight, build and survive to win the game!
Go and save the world! Destroy the 'Hive'!
\nBeginnig - Start by exploring! Get some materials and then build buildings! Don't forget to kill aliens every now and then!
                        
  ____         _____ 
 / ___|       |  ___|
| |___        | |_
 \___ \       |  _|   
 ____) |  _   | |    _
|_____/  |_|  |_|   |_|  

      """)
    


# Players dictionary 🙅🏼‍♂️ 👨🏼‍🔧 🙋🏼‍♂️
players = {}

# This piece of code asks for the number of players playing and then lets the players assign their names
num_of_p = int(input("How many of you are playing? "))
for i in range(num_of_p):
  name = input(f"What is the name of player {i + 1}? ")
  players[name] = Survivors(name)


# This is the actual game loop
while True:

  # This loop check which players are alive
  num_of_alive_players = 0
  for player in players.values():
    if player.alive:
      num_of_alive_players += 1

  # If all players are dead the message below gets printed  
  if num_of_alive_players == 0:
    print("All players are dead. Game Over!")
    break
  
  # This loop checks if a player is alive and skips their turn if not!
  for player in players.values():
    if not player.alive:
      continue

    # Random base attack function call
    initialize_rand_attack(base, aliens, player)
        
    # This is the player interface!
    choice = input(f"""
    
    ============ MANUAL ============
    \nFight aliens - You have to fight aliens to keep them in check. If you won't they will grow in numbers and attack you!
    \nBuilding - Armoury (lets you craft gear and upgrade defenses, this is how you craft a bomb) costs 150 of wood and stone 100 of iron.
             - Infirmary (lets you heal and revive other players) costs 50 of wood and stone.
             - Library (lets you learn skills) you can learn tracking or combat. Costs 100 of wood and stone. Combat ups your damage, tracking lets you collect more materials.
             - WATCH OUT THOUGH!!! Every time you build a building a Middle level alien gets spawned!
    \nCrafting - Once you have an Armoury you can choose to build a bunch of stuff
                   1. Spear - Adds 20 to your damage and costs 20 of wood and stone
                   2. Bow - Adds 30 to your damage and costs 30 of wood and stone
                   3. Upgrade defences - Adds 30 to your base defenses and costs 30 wood and stone and 50 iron
                   4. Bomb - Lets you attack the Hive and win the game and costs 150 minerals and 120 chemicals
                   5. Armour - Adds armour to your 100 character and costs 20 stone and 30 iron
    \nHealing - Once you have an infirmary you can heal yourself or revive dead players
                   1. Heal - For 15 medicine you can add 20 hp to your health
                   2. Revive a dead player - For 60 medicine you can revive a dead player
    \nLearn - Once you have a Library you can actually just learn new skills free of charge
                   1. Combat - You could learn combat (it adds 30 to your damage)
                   2. Tracking - Gives you a higher probability of getting materials when you explore
    \nAttack the hive - Once you have a bomb even just one you can start attacking th hive but carful you won't always get your way! You might not get the bomb in place if you die before! If you have two bombs in your 'bomb list' you might destroy the hive with one attack!
                   
    
    
    ============ NEW ROUND {player.name.upper()} IS PLAYING ============
                   
    You have {base.storage['wood']} of wood, {base.storage['stone']} of stone, {base.storage['iron']} of iron, {base.storage['medicine']} of medicine, {base.storage['minerals']} of minerals and {base.storage['chemicals']} of chemicals.

    You have these weapons {player.equipped_melee_weapon} and {player.equipped_ranged_weapon}, this is your damage {player.damage} and this is your health {player.health} and armour {player.armour}!

    You have these skills {player.skills} 

    And there are these aliens in the world:
    Basic: {aliens.specs['basic']['how_many']} and their damage is {aliens.specs['basic']['how_many'] * aliens.specs['basic']['damage']}
    Middle: {aliens.specs['mid']['how_many']} and their damage is {aliens.specs['mid']['how_many'] * aliens.specs['mid']['damage']}
    Boss: {aliens.specs['boss']['how_many']} and their damage is {aliens.specs['boss']['how_many'] * aliens.specs['boss']['damage']}

    What do you want to do {player.name}? (Type a number below to make your choice of activity!)
    
    1. Explore (that is how you get materials)
    2. Fight aliens (that is how keep alines in check)
    3. Build buildings (only possible with materials)
    4. Craft gear (only possible with an Armoury built)
    5. Attack the hive (only possible with a bomb)
    6. Revive a player (only functional when a player is dead)
    7. Heal (only functional with less health than a 100)
    8. Learn (learn extra skills either tracking or combat)
    9. End game 
    """).lower()

    # This if/elif/else statement lets players pick their action
    if choice == "1":
      player.explore(hive, aliens, base)
    elif choice == "2":
      player.fight_aliens(aliens, player)
    elif choice == "3":
      player.build(base)
    elif choice == "4":
      player.craft_gear(base, armoury)
    elif choice == "5":
      player.attack_the_hive(aliens, hive)
    elif choice == "6":
      other_player = input("Who do you want to save? ")
      player.save_a_player(base, other_player, infirmary)
    elif choice == "7":
      player.heal_player(base, infirmary)
    elif choice == "8":
      player.learn(base, library)
    elif choice == "9":
      player.end = "Yes"
      for player in players.values():
        if player.alive == False:
          player.end = "Yes"
    else:
      print("\nInvalid choice try again.")

    # This checks if a plaer is alive and if not subtracts 1 from the number of alive players
    if not player.alive:
      player.alive = False
      num_of_alive_players -= 1

  # This checks if the hive is still ok and all alive players want to end the game and if so ends it
  if hive.hp <= 0 or all(player.end == "Yes" for player in players.values()):
        print("Thank you for playing Survival Fables the game is now over! 🙏 ")
        break
  