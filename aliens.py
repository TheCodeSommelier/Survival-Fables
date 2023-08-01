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
      AlienType.MID: Alien(damage=20, health=60),
      AlienType.BOSS: Alien(damage=70, health=200)
    }

  def defend(self, player):
    total_alien_damage = sum(alien.damage * alien.how_many for alien in self.aliens.values())
    if player.health > total_alien_damage:
      player.health -= total_alien_damage
      self.die_or_hurt(player.damage)
    else:
      player.health = 0
      self.die_or_hurt(player.damage)
  
  def merge(self): # Based on a result of the merge we'll create a color size attr
    if self.aliens[AlienType.BASIC].how_many >= 20:
      self.aliens[AlienType.MID].how_many += 1
      self.aliens[AlienType.BASIC].how_many -= 20
      print(f"\nAliens now have {self.aliens[AlienType.MID].how_many} of a Mid level alien. Start killing them before they make a Boss!")
    elif self.aliens[AlienType.MID].how_many >= 10:
      self.aliens[AlienType.BOSS].how_many += 1
      self.aliens[AlienType.MID].how_many -= 10
      print(f"\nAliens now have {self.aliens[AlienType.BOSS].how_many} of Boss alien. Good luck out there!")
    else:
      print("\nAliens did not have enough to merge into a bigger one!")


  def die_or_hurt(self, total_player_damage):
    for alien in self.aliens.values():
      if alien.health > 0:
        dealable_damage = alien.health * alien.how_many
        if total_player_damage >= dealable_damage:
          alien.how_many = 0
        else:
          remaining_damage = dealable_damage - total_player_damage
          remaining_aliens = remaining_damage // alien.health 
          alien.how_many -= remaining_aliens



  def die_or_hurt_base(self, total_base_damage):
    for alien in self.aliens.values():
      if alien.health > 0:
        dealable_damage = alien.health * alien.how_many
        if total_base_damage > dealable_damage:
          alien.how_many = 0
        else:
          remaining_damage = dealable_damage - total_base_damage
          remaining_aliens = remaining_damage // alien.health
          alien.how_many -= remaining_aliens
        
  

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
    self.die_or_hurt(total_player_damage)
    
  
  def attack_base(self, base, player):
    total_base_damage = base.defenses
    total_alien_damage = sum(alien.damage * alien.how_many for alien in self.aliens.values())
    
    if base.defenses > 0:
      number_of_players = 0
      number_of_players  = (number_of_players + 1 for player in players.keys())
      remaining_damage = min(base.defenses, total_alien_damage)
      base.defenses -= remaining_damage
      self.die_or_hurt_base(total_base_damage)
      if base.defenses <= 0:
        base.defenses = 0
        damage_to_be_dealt = alien.damage / number_of_players
        for player in players.values():
          for alien in self.aliens.values():
            player.health -= damage_to_be_dealt
          player.update_alive_status()
        for material in base.storage.keys():
          base.storage[material] = int(base.storage[material] / 2)
        print("\nYour base defenses have been destroyed, your storage has been raided... FIGHT FOR YOUR LIFE!")
      else:
        print(f"\nGood you fought them off! You have {base.defenses} of your defense left!")
      

      for alien_type, alien in self.aliens.items():
        print(f"\nNumber of {alien_type} aliens left: {alien.how_many}!")
      
    else:
      for material in base.storage.keys():
        base.storage[material] = int(base.storage[material] / 2)
      self.attack(player)
      print("\nYour base defenses have been destroyed, your storage has been raided... FIGHT FOR YOUR LIFE!")
      

aliens = Aliens()