class Drone:
    def __init__(self, name, health, weapon1, weapon2, ability, passive):
        self.name = name
        self.health = health
        self.weapon_1 = weapon1
        self.weapon_2 = weapon2
        self.ability = ability
        self.passive = passive
    
    def get_health(self):
        return int(self.health)
    
    def decrease_health(self, damage, Invulnerable, Adaptive_Armor):
        if not Invulnerable:
            if Adaptive_Armor:
                self.health = self.health - (damage * self.ability.get_effect() / 100)
            else:
                self.health = self.health - (damage)


    def heal(self, health):
        self.health = self.health + health
    
    def set_health(self, health):
        self.health = health

        
class Weapon:
    def __init__(self, name, weapon_type, damage, sound_link, ammo, cooldown=None, precision=None, time=None, drain=None, leech = 0):
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage
        self.sound_link = sound_link
        self.cooldown = cooldown
        self.precision = precision
        self.time = time
        self.drain = drain
        self.ammo = ammo
        self.leech = leech

    def get_weapon_type(self):
        return f"{self.weapon_type}"
    
    def get_weapon_leech(self, energy_leech):
        if energy_leech:
            return int(self.leech * 2)
        else: return int(self.leech)
    
    def get_weapon_damage(self, overcharge):
        if overcharge:
            return int(self.damage * 1.5)
        else:
            return int(self.damage)

    def get_weapon_name(self):
        return f"{self.name}"
    
    def get_weapon_drain(self):
        return int(self.drain)
    
    def get_weapon_cooldown(self):
        return int(self.cooldown)

    def get_attack_string(self):
        return f"{self.target}{self.weapon_type}"
    
    def get_sound_link(self):
        return f"{self.sound_link}"
    
    def decrease_ammo(self):
        if self.ammo > 0:
            self.ammo = self.ammo - 1
    
    def get_ammo(self):
        return int(self.ammo)
    
    def get_sound(self):
        return str(self.sound_link)

# Define weapon types
class Gun(Weapon):
    def __init__(self, name, damage, sound_link, ammo, cooldown = 100, leech = 0):
        super().__init__(name, 'G', damage, sound_link, ammo, cooldown = cooldown, leech = leech)

class Hitscan(Weapon):
    def __init__(self, name, damage, sound_link, ammo, cooldown, leech=0):
        super().__init__(name, 'H', damage, sound_link, ammo, cooldown=cooldown, leech=leech)

class Projectile(Weapon):
    def __init__(self, name, damage, sound_link, ammo, cooldown, precision, time, drain=None, leech = 0):
        super().__init__(name, 'P', damage, sound_link, ammo, cooldown=cooldown, precision=precision, time=time, drain=drain, leech = leech)

    def get_weapon_time(self):
        return int(self.time)
    
    def get_weapon_precision(self):
        return int(self.time)

class Beam(Weapon):
    def __init__(self, name, damage, sound_link, ammo, cooldown, time, drain=None, leech=0):
        super().__init__(name, 'B', damage, sound_link, ammo, cooldown=cooldown, time=time, drain=drain, leech=leech)

    def get_weapon_time(self):
        return int(self.time)

class Ability:
    def __init__(self, name, ability_type, cooldown, duration=None, effect=None):
        self.name = name
        self.ability_type = ability_type
        self.cooldown = cooldown
        self.duration = duration
        self.effect = effect
    
    def get_ability_type(self):
        return f"{self.ability_type}"

    def get_ability_name(self):
        return f"{self.name}"
    
    def get_cooldown(self):
        return int(self.cooldown)
    
    def get_duration(self):
        return int(self.duration)
    
    def get_effect(self):
        return int(self.effect)

# Define ability types
class Self_Instant(Ability):
    def __init__(self, name, cooldown, effect = 0):
        super().__init__(name, 'S', cooldown, None, effect)

class Self_Duration(Ability):
    def __init__(self, name, cooldown, duration, effect = 0):
        super().__init__(name, 'P', cooldown, duration, effect)

class Opp_Instant(Ability):
    def __init__(self, name, cooldown, effect = 0):
        super().__init__(name, 'L', cooldown, None, effect)

class Opp_Duration(Ability):
    def __init__(self, name, cooldown, duration, effect = 0):
        super().__init__(name, 'D', cooldown, duration, effect)


# Define passive types
class Passive:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Passive1(Passive):
    def __init__(self):
        super().__init__('Passive1', 'Description for Passive1.')

class Passive2(Passive):
    def __init__(self):
        super().__init__('Passive2', 'Description for Passive2.')

class Passive3(Passive):
    def __init__(self):
        super().__init__('Passive3', 'Description for Passive3.')

class Passive4(Passive):
    def __init__(self):
        super().__init__('Passive4', 'Description for Passive4.')