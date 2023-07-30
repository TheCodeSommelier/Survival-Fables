from players import players

# Aliens (aka enemies) 👽
class Aliens:
  
  def __init__(self, specs):
    self.specs = specs # Is a dictionary of type of alien as keys (basic, mid, boss) and a dictionary as a value storing color, size and how many as keys and corresponding values as values.

  
  def merge(self, aliens): # Based on a result of the merge we'll create a color size attr
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


  def die_or_hurt(self, total_player_damage, aliens):
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

  
  def die_or_hurt_base(self, total_base_damage, aliens):
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

    self.die_or_hurt(total_player_damage, aliens)
    
  
  def attack_base(self, base, player, aliens):
    total_base_damage = base.defenses
    total_alien_damage = 0
    for alien_type, alien_info in aliens.specs.items():
      total_alien_damage += alien_info["damage"] * alien_info["how_many"]

    self.die_or_hurt_base(total_base_damage, aliens)
    
    if base.defenses > 0:
      rem_damage = min(base.defenses, total_alien_damage)
      base.defenses -= rem_damage
      total_alien_damage -= total_alien_damage
      print(f"\nGood you fought them off! You have {base.defenses} of your defense left!")

      for alien_type, alien_info in aliens.specs.items():
        print(f"\nNumber of {alien_type} aliens left: {alien_info['how_many']}!")
      
    else:
      for material in base.storage.keys():
        base.storage[material] = int(base.storage[material] / 2)
      print("\nYour base defenses have been destroyed... FIGHT FOR YOUR LIFE!")
      self.attack(player)




# Initilizing aliens
aliens = Aliens({
  "basic": {"how_many": 1, "damage": 10, "health": 10},
  "mid": {"how_many": 0, "damage": 20, "health": 60},
  "boss": {"how_many": 0, "damage": 70, "health": 200}
})

