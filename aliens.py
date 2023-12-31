from players import players
from enums import *

class Alien:
  def __init__(self, damage, health):
    self.damage = damage
    self.health = health
    self.how_many = 0

# Aliens (aka enemies) 👽
class Aliens:
  def __init__(self):
    self.aliens = {
      AlienType.BASIC: Alien(damage=10, health=10),
      AlienType.MID: Alien(damage=30, health=40),
      AlienType.BOSS: Alien(damage=50, health=200)
    }


  def defend(self, player):
    total_alien_damage = sum(alien.damage * alien.how_many for alien in self.aliens.values())
    if player.health > total_alien_damage:
      player.health -= total_alien_damage
      self.take_damage_from_1_player(player)
    else:
      player.health = 0
      self.take_damage_from_1_player(player)


  def merge(self): # Based on a result of the merge we'll create a color size attr
    if self.aliens[AlienType.BASIC].how_many >= 15:
      self.aliens[AlienType.MID].how_many += 1
      self.aliens[AlienType.BASIC].how_many -= 15
      print(f"\nAliens now have {self.aliens[AlienType.MID].how_many} of a Mid level alien. Start killing them before they make a Boss!")
    elif self.aliens[AlienType.MID].how_many >= 10:
      self.aliens[AlienType.BOSS].how_many += 1
      self.aliens[AlienType.MID].how_many -= 10
      print(f"\nAliens now have {self.aliens[AlienType.BOSS].how_many} of Boss alien. Good luck out there!")
    else:
      print("Aliens did not have enough to merge into a bigger one!")


  def take_damage_from_1_player(self, player):
    for i in range(0, player.damage // 10):
      for alien_type, alien in self.aliens.items():
        while alien.health > 0:
          alien.health -= player.damage
          if alien.health <= 0 and self.aliens[alien_type].how_many > 0:
            self.aliens[alien_type].how_many -= 1
          break
      self.aliens[AlienType.BASIC].health = 10
      self.aliens[AlienType.MID].health = 40
      self.aliens[AlienType.BOSS].health = 200


  def take_damage_from_all_players(self, total_player_damage):
    for i in range(0, total_player_damage // 10):
      for alien_type, alien in self.aliens.items():
        while alien.health > 0:
          alien.health -= total_player_damage
          if alien.health <= 0 and self.aliens[alien_type].how_many > 0:
            self.aliens[alien_type].how_many -= 1
          break
      self.aliens[AlienType.BASIC].health = 10
      self.aliens[AlienType.MID].health = 40
      self.aliens[AlienType.BOSS].health = 200


  def take_damage_from_base(self, total_base_damage):
    for _ in range(total_base_damage // 10):
      for alien_type, alien in self.aliens.items():
        if alien.how_many > 0:
          alien.health -= total_base_damage
          if alien.health <= 0:
            alien.health = 0
            alien.how_many -= 1
          break
      self.aliens[AlienType.BASIC].health = 10
      self.aliens[AlienType.MID].health = 40
      self.aliens[AlienType.BOSS].health = 200


  def attack(self, player):
    # Total damage dealt by aliens
    total_alien_damage = sum(alien.damage * alien.how_many for alien in self.aliens.values())

    # This calculates the respective damage to the armour of the players if any
    remainder = 0
    if player.armour > 0:
      if player.armour >= total_alien_damage:
        player.armour -= total_alien_damage
        print("Your armour is damaged but you are fine!")
      else:
        remainder = player.armour - total_alien_damage
        player.armour = 0
        player.health -= remainder
        print(f"\nYou took some hits {player.name} your HP is {player.health}. You should go heal... ")
    else: # damage dealt to the HP
      player.health -= total_alien_damage
      if player.health <= 0:
        player.health = 0
        print(f"\n{player.name} died... Revive them!")


    # This calculates the damage of the players and subtracts the damage from alien health
    total_player_damage = sum(player.damage for player in players.values())
    self.take_damage_from_all_players(total_player_damage)


  def attack_base(self, base, player):
    number_of_aliens = sum(alien.how_many for alien in self.aliens.values())
    total_base_damage = base.defenses
    total_alien_damage = sum(alien.damage * alien.how_many for alien in self.aliens.values())
    if number_of_aliens == 0:
      return
    if base.defenses > 0:
      number_of_players = len(players.keys())
      remaining_damage = min(base.defenses, total_alien_damage)
      base.defenses -= remaining_damage
      self.take_damage_from_base(total_base_damage)
      if base.defenses <= 0:
        base.defenses = 0
        damage_to_be_dealt = total_alien_damage // number_of_players
        for player in players.values():
          player.health -= damage_to_be_dealt
          player.update_alive_status()
        for material in base.storage.keys():
          base.storage[material] = int(base.storage[material] / 2)
        print("\nYour base defenses have been destroyed, your storage has been raided... FIGHT FOR YOUR LIFE!")
      else:
        print(f"\nGood, you fought them off! You have {base.defenses} of your defense left!")


    for alien_type, alien in self.aliens.items():
      print(f"\nNumber of {alien_type} aliens left: {alien.how_many}!")

aliens = Aliens()
