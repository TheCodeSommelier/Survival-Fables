from players import *

from base_and_buildings import *

from aliens import aliens

from hive import Hive

import random



# A solo standing function that starts a randomised attack on the base
def random_base_attack(base, aliens, player):
  numbers = [16, 33, 12, 42, 22]
  random_number = random.randint(1, 50)
  if random_number in numbers:
    aliens.attack_base(base, player, aliens)

def help(player):
  while True:
    help_menu = input(f"""What do you need help with {player.name}?
    1. Beginning of the game
    2. Fighting aliens
    3. Building
    4. Crafting
    5. Attacing the hive
    6. Revivng players
    7. Healing
    8. Learing
    9. Don't need help
    """)

    if help_menu == "1":
      print("""\nIn the beginning you can really do only two things explore or fight aliens. 
      We highly recommend exploration as that is how you get materials. Just remeber to fight every now and then,
      otherwise the aliens will be spawning and merging endlessly. So start with exploring and take it from there!""")
      break
    elif help_menu == "2":
      print(f"""\nFighting aliens is pretty straight forward in this game.
      Everytime you explore 1 basic alien spawns every 10 basic = 1 mid, every 10 mid = 1 boss. 
      If your damage is higher then the aliens health you kill them and if it is high enough 
      to cover all of the health of all the aliens, you kill them all. Try to fight often, 
      as it will make your game easier. """)
      break
    elif help_menu == "3":
      print("""\nYou need buidings to be able to craft (Armoury), learn (Library), heal (Infirmary) and revive (Infirmary). 
      So definitely BUILD! Just keep in mind that for every building you build 1 mid alien spawns.
      Requirements: 
      """)
      for building in MATERIAL_REQUIREMENTS.keys():
        if building in {"Infirmary", "Armoury", "Library"}:
          print(f"""\n{building} - {MATERIAL_REQUIREMENTS[building]}""")
      break
    elif help_menu == "4":
      print(f"""\nTo craft anything you need an Armoury first. 
      Once you have it you can craft these weapons and upgrades.
      Requirements:
      """)
      for item, requirements in MATERIAL_REQUIREMENTS.items():
        if item in {"Spear", "Bow", "Knife", "Gun", "Upgrade defenses", "Bomb", "Armour",}:
          print(f"{item} - {MATERIAL_REQUIREMENTS[item]}")
      break
    elif help_menu == "5":
      print("""\nIf you have a bomb you can attack the hive. Success rate is randomised so you never know...
      You need two bombs to destroy the hive completely in single go (Attack needs to be successful). 
      Once you destroy the hive either in multiple attacks or in a single go you win!""")
      break
    elif help_menu == "6":
      print(f"""\nIf a player dies you can revive them for 60 medicine. It will add 20 hp to their health. """)
      break
    elif help_menu == "7":
      print(f"""\nWhen you take some damage you can heal for 20 medicine and each heal will add 20hp to your health. """)
      break
    elif help_menu == "8":
      print(f"""\nIf you have a library built you can learn new skills 'Combat' will increase your damage
      and 'Tracking' will increase the probability of finding materials when exploring. """)
      break
    elif help_menu == "9":
      break


base = Base({
  "wood": 1000,
  "stone": 1000,
  "iron": 1000,
  "medicine": 1000,
  "minerals": 1000,
  "chemicals": 1000
})
infirmary = Infirmary()
armoury = Armoury()
library = Library()


hive = Hive()

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


# This piece of code asks for the number of players playing and then lets the players assign their names
number_of_players = int(input("How many of you are playing? "))
for i in range(number_of_players):
  name = input(f"What is the name of player {i + 1}? ")
  players[name] = Survivors(name)


# This is where the game loop starts
game_running = True
while game_running:


  for player in players.values():
    if not player.alive:
      continue

    if hive.hp <= 0 or all(player.end == True for player in players.values()):
      print("Thank you for playing Survival Fables the game is now over! 🙏 ")
      game_running = False
      break
    elif all(player.alive == False for player in players.values()):
      print("""All players have died! 
      Thank you for playing Survival Fables the game is now over! 🙏 """)
      game_running = False
      break


    random_base_attack(base, aliens, player)
        
    # This is the player interface!
    choice = input(f"""
  
    NEW ROUND {player.name.upper()} IS PLAYING

    ============ Base stats ============
    Storage - Wood: {base.storage['wood']}
            - Stone: {base.storage['stone']}
            - Iron: {base.storage['iron']}
            - Medicine: {base.storage['medicine']}
            - Minerals: {base.storage['minerals']}
            - Chemicals: {base.storage['chemicals']}

    ============ {player.name}'s stats ============
    Player stats - Your damage {player.damage}
                 - Your health {player.health}
                 - Your armour {player.armour}

    Your weapons: - Melee: {player.equipped_melee_weapon} 
                  - Ranged: {player.equipped_ranged_weapon}
                 
    Your skills: - Combat: {player.combat_skill}
                 - Tracking: {player.tracking_skill}

                 
    ============ Aliens stats ============
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
    9. Help (Will display a manual)
    10. End game 
    """).lower()

    # This if/elif/else statement lets players pick their action
    if choice == "1":
      player.explore(hive, aliens, base)
    elif choice == "2":
      player.fight_aliens(aliens, player)
    elif choice == "3":
      player.build(base, hive, aliens)
    elif choice == "4":
      player.craft_gear(base, armoury, player)
    elif choice == "5":
      player.attack_the_hive(aliens, hive, player)
    elif choice == "6":
      other_player = input("Who do you want to save? ")
      player.save_a_player(base, other_player, infirmary)
    elif choice == "7":
      player.heal_player(base, infirmary)
    elif choice == "8":
      player.learn(base, library)
    elif choice == "9":
      help(player)
    elif choice == "10":
      for player in players.values():
        end = input(f"Are you sure you want to end the game {player.name}? (Yes/No) ")
        if end.capitalize() == "Yes":
          player.end = True
    else:
      print("\nInvalid choice try again.")


    if not player.alive:
      player.alive = False
  