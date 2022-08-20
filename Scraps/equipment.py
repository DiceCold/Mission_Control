#Inventory management
import pygame
import copy

startup = True

screen_width = 600
screen_height = 600
centerpoint = ((screen_width)/2, (screen_height)/2)
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
jet_red_surf = pygame.image.load('graphics/pilots/red_dot_icon.png').convert_alpha()

text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
clock = pygame.time.Clock()
none = "none"
red_dot_surf = pygame.image.load('graphics/pilots/red_dot_icon.png').convert_alpha()
red_dot_surf = pygame.transform.scale(jet_red_surf, (10,10))

class Equipment_Slot(pygame.sprite.Sprite):
    def __init__(self, slot_number, pos_x, pos_y):
        if slot == 1:
            super().__init__()
            self.slot_number = slot_number
            self.equipped = "Unassigned"
            text_surf = text_font.render(f"{self.equipped}",False,(90,90,90))
            self.image = text_surf
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
        def update():
            self.image = text_font.render(f"{self.equipped}",False,(90,90,90))

class Battlesuit(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "majestic":
            self.name = "Majestic"
            self.mobility = 1
            self.refresh = 4
            self.power_core = "cold_fusion_core"
        if type == "leviathan":
            self.name = "Leviathan"
            self.mobility = 0.5
            self.refresh = 44
            self.power_core = "dirty_fission_core"
        if type == "tower":
            self.name = "Tower"
            self.mobility = 0
        self.equipment = {1:beam_cannon, 2:none, 3:none, 4:none}
        self.shields = []
        self.weapons = [beam_cannon,beam_cannon]
        self.damaged = False
        self.severely_damaged = False
        self.target = "unassigned"
        self.pos_x = 500
        self.pos_y = 500
        self.momentum_x = 10
        self.momentum_y = 10
        self.angle = 0
        self.image = red_dot_surf
        self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        self.invuln_timer = 200
    def update(self):
        self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        self.invuln_timer -= 1
        if self.invuln_timer > 0:
            self.invuln_timer = 0
        

damage_types = ["thermal","cold","piercing","concussive","magnetic","shock"]
status_effects = ["frozen","overheated","disrupted","blinded","knockback","energized","supressed","tethered"]
power_cores = {"01":"trapped_combustion_core", "02":"dirty_fission_core", "04":"solar_array_core", "06":"cold_fusion_core", "07":"entropy_core", "08":"black_pinhole_core", "10":"wave_collapse_core", "11":"phantom_pinnacle_core", "0x":"alien_crystal_core", "00":"no_core"}



class Weapon:
    def __init__(self, type):
        if type == "beam_cannon":
            self.name = "Beam Cannon"
            self.accuracy = 1
            self.distance = "mid"
            self.cooldown = 200
            self.damage_type = "thermal"
            self.apply_status = "overheated"
        if type == "cryo_shot":
            self.name = "Cryo Shot"
            self.accuracy = 1
            self.distance = "close"
            self.cooldown = 200
            self.damage_type = "cold"
            self.apply_status = "frozen"
        if type == "powersword":
            self.name = "Powersword"
            self.accuracy = 1
            self.distance = "melee"
            self.cooldown = 200
            self.damage_type = "pierce"
            self.apply_status = "knockback"
        if type == "flame_lance":
            self.name = "Flame Lance"
            self.accuracy = 1
            self.distance = "melee"
            self.cooldown = 200
            self.damage = "thermal"
            self.apply_status = "knockback" + "overheated"
        if type == "lightning_chain":
            self.name = "Lightning Chain"
            self.accuracy = 1
            self.distance = "melee"
            self.cooldown = 200
            self.damage = "shock"
            self.apply_status = "disrupted" + "tethered"
            

beam_cannon = Weapon("beam_cannon")

#formatting is "Owner's _ Suit_Type _ ID" eg "Rose's Majestic 086603"
#suit code is size class, power core type , power core capacity, product generation
#086403 = 08.6.4.03 = size 8, fusion core, capacity 4, generation 3
#core type determines what kind of fuel the suit needs to operate
#not all core types are legal for use, either due to hazards or restrictions on their fuel supply
#can replace core with high capacity battery that does not recharge outside of base. Each unit of stored charge = 60 seconds of powercore output

        

class Shields:
    def __init__(self, name, cooldown, charged):
            self.name = name
            self.cooldown = cooldown
            self.charged = charged

# equipment_group = pygame.sprite.Group()
# equipment_group.add(Equipment_Slot(1))

# while True:
    # equipment_group.update()
    # equipment_group.draw(screen)
    # for event in pygame.event.get():
        # if event.type == pygame.QUIT: #Quit
            # pygame.quit()
            # exit()
    # pygame.display.update()
    # clock.tick(60)
    
#Equipment info
# if startup == True: #load Weapons
    # powersword = weapon("Powersword", 3, "melee", 100)
    # burst_cannon = weapon("Burst cannon", 3, "Close", 200)
    # beam_cannon = weapon("beam cannon", 3, "Close", 200)
    
if startup == True: #load shields
    light_shield = Shields("Light shields", 18, True)
    majestic_shield1 = copy.copy(light_shield)
    majestic_shield2 = copy.copy(light_shield)

# if startup == True: #load Battlesuits
    # Majestic = battlesuit("Majestic", 3, "Quick", [majestic_shield1, majestic_shield2], majestic_beam_cannon, False, False, "unassigned.battlesuit", 300, 300, 0, 0, copy.copy(jet_red_surf), copy.copy(jet_red_rect))
    # Leviathan = battlesuit("Leviathan", 4, "Slow", light_shield, beam_cannon, False, False, "unassigned.battlesuit", 300, 300, 0, 0, copy.copy(jet_red_surf), copy.copy(jet_red_rect))
    # Tower = battlesuit("Tower", 4, "none", light_shield, beam_cannon, False, False, "unassigned.battlesuit", 800, 800, 0, 0, copy.copy(radio_surf), copy.copy(radio_rect))