#navigator

group.pilots = pygame.sprite.Group()
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

class Waypoint:
    def __init__(self, pos_x, pos_y):
        self.type = "waypoint"
        self.pos_x = pos_x
        self.pos_y = pos_y

class Game_Manager:
    def __init_(self):
        self.pilot_roster = []
        self.inventory = []
        self.current_scene = "empty"
        self.scene_queue = []
        self.current_mission = "empty"
        self.available_missions = ["mission 1: train attack"]
        self.completed_missions = []
        self.unavailable_missions = ["mission 2: collect boxes", "Rupert Thorn 1: an invitation from the crimelord", "Marko Munitions 1: free trial"]

class Navigator:
    def __init__(self, name, type, battlesuit, team):
        super().__init__()
        
        self.name = name
        self.type = type
        self.battlesuit = battlesuit
        self.team = team
        self.link = "empty"
        
        self.injured = False
        self.alive = True
        self.shielded = False
        
        self.pos_x = 0
        self.pos_y = 0
        self.momentum_x = 0
        self.momentum_y = 0
        self.max_speed = 12
        
        self.on_mission = False
        self.attack_target = "empty"
        self.attack_distance = screen_width
        self.move_target = "empty"
        self.move_distance = screen_width
        
        if self.team == "vanguard": self.image = pygame.image.load("graphics/interface/blue_dot.png").convert_alpha()
        
    def find_target(self, type):
        #set defaults
        current_distance = screen_width
        current_target = "empty"
        
        #determine what list to sort through
        try:
            if type == "move" and self.orders = "aggro": type == "attack"
            elif type == "move" and self.orders = "follow": target_group = mission.pilots
            elif type == "move" and self.orders = "objective": target_group = mission.objectives
                
            if type == "attack": target_group = mission.pilots
        except:
            if debug_mode == True: print(self.name, "was unable to determine target group. Type was:", type, "and orders were:", self.orders)
            else: pass
            
        #sort through list to find closest
        for target in target_list:
            #disqualifiers
            if type == "attack" and target.team == self.team:pass
            #check distance
            else:
                distance = find_distance(self, target)
                if distance < current_distance: current_target = target
                else: pass
            
        return current_target
    
    def maneuver(self):
        #update momentum
        if self.pos_x < self.move_target.pos_x: self.momentum_x += 0.1
        else: self.momentum_x -= 0.1
        
        if self.pos_y < self.move_target.pos_y: self.momentum_y += 0.1
        else: self.momentum_y -= 0.1
        
        #speed limit
        if abs(self.momentum_x) > self.max_speed: self.momentum_x *= 0.9
        if abs(self.momentum_y) > self.max_speed: self.momentum_y *= 0.9
                
        #update position
        self.pos_x = self.pos_x + self.momentum_x
        self.pos_y = self.pos_y + self.momentum_y
    
    def create_visual_effect(self, visual, origin, target)
        group.visual_effects.add(Visual_Effect(visual, origin, target))
    
    def use_equipment(self):
        for item in self.battlesuit.loadout:
            if item.cooldown == 0:
                #check if item is a weapon, target distance, and whether target has invuln
                if item.type == "weapon" and self.attack_distance < item.distance and self.attack_target.invuln_timer == 0:
                    item.cooldown = item.cooldown_max
                    self.roll_to_hit()
                    self.create_visual_effect(item.visual, self, self.attack_target)
                
                #restore shields and put item on cooldown
                elif item.type == "shield" and self.shielded == False:
                    self.shielded = True
                    item.cooldown = item.cooldown_max
                
                #making movement item based allows suits to use multiple movement modules
                elif item.type == "movement":
                    self.pos_x += (self.momentum_x * item.mobility)
                    self.pos_y += (self.momentum_y * item.mobility)
                    
    def update(self):
        #movement
        self.move_target = self.find_target("move")
        self.move_distance = find_distance(self, self.move_target)
        self.maneuver()
        
        #attacking
        self.attack_target = self.find_target("attack")
        self.attack_distance = find_distance(self, self.attack_target)
        
class Mission_Manager:
    def __init__ (self):
        self.pilots = pygame.sprite.Group()
        self.objectives = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.biome = "desert"
        self.terrain = pygame.sprite.Group()
        
        self.map_momentum_x = 0
        self.map_momentum_y = 0
        self.map_offset_x = 0
        self.map_offset_y = 0
        
    def spawn_random_crates(self, quantity):
        while quantity > 0:
            pos_x = random.ranint(screen_width*0.2, screen_width*0.8)
            pos_y = random.randint(screen_height*0.2, screen_height*0.8)
            self.objectives.add(Objective("pickup", "supply_crate", pos_x, pos_y)
            quantity -= 1
            
    def spawn_drones(quantity, pos_x, pos_y, position_variance, team):
        if quantity == 1d6: quantity = random.randint(1,6)
        while quantity > 0:
            drone = Navigator("drone", copy.deepcopy(drone_suit), team)
            drone.pos_x = pos_x + random.randint(-position_offset, position_variance)
            drone.pos_y = pos_y + random.ranint(-position_offset, position_variance)
            self.pilots.add(drone)
            
    def spawn_waypoint(pos_x, pos_y):
        self.waypoints.add(Waypoint(pos_x, pos_y))
        
    def spawn_train(pos_x, pos_y):
        train = Navigator("train", "train", copy.deepcopy(train_suit), "vanguard")
        train.pos_x = pos_x
        train.pos_y = pos_y
        self.pilots.add(train)
            
    def reset(self):
        self.pilots.empty()
        self.objectives.empty()
        self.waypoints.empty()
        self.terrain.empty()
        self.biome = "desert"
        for pilot in game.pilot_roster: pilot.on_mission = False
        
    def load(self, name):
        if name = "mission 1: train attack":
            #spawn waypoints for train
            self.spawn_waypoint(screen_width*0.2, screen_height*0.2)
            self.spawn_waypoint(screen_width*0.6, screen_height*0.3)
            self.spawn_waypoint(screen_width*0.3, screen_height*0.5)
            self.spawn_waypoint(screen_width*0.6, screen_height*0.6)
            self.spawn_waypoint(screen_width*0.2, screen_height*0.9)
            self.spawn_waypoint(screen_width*1.2, screen_height*0.7)
            #spawn train
            self.spawn_train(screen_width*0.15, screen_height*0.15)
            
            
        
class Objective:
    def __init__(self, type, name, pos_x, pos_y):
        super().__init__()
        
        self.type = type
        self.name = name
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.link = empty
        self.radius = screen_width*0.01
        self.pull_strength = 400
        
        self.progress_min = 0
        self.progress_max = 100
        self.progress = 0
        
        self.animation_index = 1
        self.frame_0 = pygame.image.load("graphics/blank.png")
        
        if self.type == "pickup" and self.name == "supply_crate":
            self.width = screen_width*0.05
            self.height = screen_width*0.05
            self.frame_1 = pygame.image.load("graphics/interface/icons/box_closed.png")
            self.frame_2 = pygame.image.load("graphics/interface/icons/box_open.png")
            self.frames = [self.frame_0, self.frame_1, self.frame_2]
            
        if self.type == "train":
            self.width = screen_width*0.05
            self.height = screen_width*0.05
            self.frame_1 = pygame.image.load("graphics/icons/blue_dot.png")
            
        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self,width, self.height))
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
    
    def establish_link(self):
        #search for unlinked pilots active on the mission
        for pilot in mission.pilots:
            if pilot.link == "empty" and self.link == "empty":
                #check distance
                if abs(self.pos_x - pilot.pos_x) < self.radius and abs(self.pos_y - pilot.pos_y) < self.radius:
                    #assign link to pilot and objective
                    pilot.link = self
                    self.link = pilot
                else: pass
    
    def pull(pilot):
        #pull tethered pilot closer, becoming stronger as distance decreases
        if pilot.pos_x < self.pos_x: pilot.momentum_x += self.pull_strength/abs(self.pos_x - pilot.pos_x)
        elif pilot.pos_x > self.pos_x: pilot.momentum_x -= self.pull_strength/abs(self.pos_x - pilot.pos_x)
        
        if pilot.pos_y < self.pos_y: pilot.momentum_y += self.pull_strength/abs(self.pos_y - pilot.pos_y)
        elif pilot.pos_y > self.pos_y: pilot.momentum_y -= self.pull_strength/abs(self.pos_y - pilot.pos_y)
        
    def manage_link(self):
        if self.link != "empty":
            pilot = self.link
            
            #unlink if the pilot is injured or dead
            if pilot.injured == True or pilot.alive == False: self.link = "empty"
            
            #draw tether to linked pilot
            pygame.draw.line(screen, (80,80,80), (self.pos_x, self.pos_y), (pilot.pos_x, pilot.pos_y, 10)
            
    def track_progress(self):
        #fill
        if self.link != "empty" and self.progress < self.progress_max: self.progress += 1
        #empty
        elif self.link == "empty" and self.progress_min < self.progress: self.progress -= 1
        #follow linked pilot with y offset if progress is full
        elif self.link != "empty" and self.progress = self.progress_max:
            self.pos_x = self.link.pos_x
            self.pos_y = self.link.pos_y + screen_height*0.05
            
    def update(self):
        #update image and rect
        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
    
        #update link
        if self.link == "empty": self.establish_link()
        elif self.link != "empty":
            #pull pilot if not at 100% progress
            if self.progress < self.progress_max: 
                try: self.pull(self.link)
                except: if debug_mode == True: print("Error:", self.name, "was unable to pull linked pilot", self.link.name)
            
            try: self.manage_link()
            except: if debug_mode == True: print("Error: there was a problem managing link between", self.name, "and", self.link.name)
        
        #update progress
        self.track_progress()
            
            
            