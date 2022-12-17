import pygame


def calculate_distance(self, other_pilot):
    dx = other_pilot.x - self.x
    dy = other_pilot.y - self.y
    return (dx ** 2 + dy ** 2) ** 0.5


class Pilot:
    def __init__(self, x, y, loadout):
        self.x = x
        self.y = y
        self.loadout = loadout
        self.speed = 0
        self.shielded = False
        self.damaged = False

    def search_for_closest_target(self, enemy_team):
        closest_distance = float("inf")
        closest_target = None
        for enemy in enemy_team:
            distance = self.calculate_distance(enemy)
            if distance < closest_distance:
                closest_distance = distance
                closest_target = enemy
        return closest_target

    def calculate_distance(self, other_pilot):
        dx = other_pilot.x - self.x
        dy = other_pilot.y - self.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def increase_acceleration(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = self.calculate_distance(target)
        self.speed += 0.1 * (dx / distance)
        self.speed += 0.1 * (dy / distance)


class Weapon:
    def __init__(self, range, cooldown, damage_type, weapon_type):
        self.range = range
        self.cooldown = cooldown
        self.damage_type = damage_type
        self.on_cooldown = False
        self.type = weapon_type

    def can_fire(self, target):
        distance = calculate_distance(self.owner, target)
        return distance <= self.range and not self.on_cooldown

    def fire(self, target):
        if self.can_fire(target):
            if self.type == "seeker_missile":
                self.spawn_projectile(target)
            # Fire weapon at target
            self.on_cooldown = True
            # Start cooldown timer

    def spawn_projectile(self, target):
        projectile = Projectile(self.owner.x, self.owner.y, target)
        # Add projectile to game state

    def update_cooldown(self):
        if self.on_cooldown:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.on_cooldown = False
                self.cooldown = self.initial_cooldown


class Shield:
    def __init__(self, cooldown, owner):
        self.cooldown = cooldown
        self.initial_cooldown = cooldown
        self.on_cooldown = False
        self.owner = owner

    def activate(self):
        if not self.owner.shielded and not self.on_cooldown:
            self.owner.shielded = True
            self.on_cooldown = True

    def update_cooldown(self):
        if self.on_cooldown:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.on_cooldown = False
                self.cooldown = self.initial_cooldown


class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = calculate_distance(self, self.target)
        self.x += 0.1 * (dx / distance)
        self.y += 0.1 * (dy / distance)

    def check_collision(self):
        distance = calculate_distance(self, self.target)
        if distance <= 1:
            # Deal damage to target
            self.destroy()

    def destroy(self):
        # Remove projectile from game state
        pass
