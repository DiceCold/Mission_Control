import pygame 
debug_mode = False

def find_distance(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pox_y - origin.pos_y
    distance_h = (distance_x**2 + distance_y**2)**0.5
    return distance_h
        
def find_angle(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pos_y - origin.pos_y
    
    rads = atan2(-distance_y, distance_x)
    rads %= 2*pi
    angle = degrees(rads) 
    return angle

class Equipment:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        
        self.cooldown_max = 100
        self.cooldown = self.cooldown_max
        
        if self.type == "weapon":
            #set defaults for weapons
            self.weapon_type = "rapid_fire"
            self.shots = 1
            self.distance = 24
            self.hit_bonus = 0
            self.strength = 4
            self.ap = 0
            self.damage = 1
            self.special_rules = []
            self.visual = "bullets"
            
            if self.name == "bolter":
                self.weapon_type = "rapid_fire"
                self.shots = 1
                self.distance = 24
                self.strength = 4
                self.ap = 0
                self.damage = 1
                self.visual = "bullets"
            
            elif self.name == "burst cannon":
                self.weapon_type = "assault"
                self.shots = 6
                self.distance = 18
                self.strength = 5
                self.ap = 0
                self.damage = 1
                self.visual = "bullets"
                
            elif self.name = "missile pod":
                self.weapon_type = "assault"
                self.shots = 2
                self.distance = 30
                self.strength = 7
                self.ap = 2
                self.damage = 2
                self.visual = "explosion"
            
            elif self.name = "plasma rifle":
                self.weapon_type = "assault"
                self.shots = 1
                self.distance = 30
                self.strength = 8
                self.ap = 4
                self.damage = 3
                self.visual = "plasma"
                
            elif self.name = "flamer":
                self.weapon_type = "assault"
                self.shots = random.randint(1,6) + 2
                self.distance = 12
                self.strength = 4
                self.ap = 0
                self.damage = 1
                self.special_rules = ["autohit"]
                self.visual = "flames"
                
            
        elif self.type == "shield":
            self.flashtime_max = 10
            self.flashtime = 0
        
        elif self.type == "movement":
            #set default mobility
            self.mobility = 1
        
    def update(self):
        #reduce cooldown
        if self.cooldown > 0: self.cooldown -= 1
        
        #reduce flashtime on shields
        if self.type == "shield" and self.flashtime > 0: self.flashtime -= 1
        
class Visual_Effect:
    def __init__(self, type, name, origin, target)
        self.type = type
        self.name = name
        self.origin = origin
        self.target = target
        
        #set defaults
        self.length = find_distance(self.origin, self.target)
        self.angle = find_angle(self.origin, self.target)
        self.countdown = 60
        
        if self.type == "beam":
            self.length = find_distance(self.origin, self.target)
            self.width = screen_width*0.01
            
        elif self.type == "projectile": pass
    
    def update(self):
        if self.countdown > 0: self.countdown -= 1
        elif self.countdown == 0: self.kill()