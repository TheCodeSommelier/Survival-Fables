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

    You have these skills - Combat: {player.combat_skill}
                          - Tracking: {player.tracking_skill}

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
      for player in players.values():
        end = input(f"Are you sure you want to end the game {player.name}? (Yes/No) ")
        if end.capitalize() == "Yes":
          player.end = True
    else:
      print("\nInvalid choice try again.")


    if not player.alive:
      player.alive = False
  