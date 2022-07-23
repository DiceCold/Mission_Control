import pygame
from sys import exit
from random import randint, choice

screen_width = 1920
screen_height = 1080

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
global cooldown
global pos
cooldown = 0
nameplate_quantity = 0

pilot_list_name_nighthawk_surf = pygame.image.load('graphics/interface/pilot_list_name_nighthawk_75.png').convert_alpha()
pilot_list_name_intrepid_rose_surf = pygame.image.load('graphics/interface/pilot_list_name_intrepid_rose_75.png').convert_alpha()
pilot_list_name_lightbringer_surf = pygame.image.load('graphics/interface/pilot_list_name_lightbringer_75.png').convert_alpha()

pilot_name = "Nighthawk"
pilot_target = "Target: " + "Unassigned"

class Pilot_Names(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        global pilot_name
        global pilot_target

class Health_Icons(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        global nameplate_quantity
        if type == 'shield':
            shield_1 = pygame.image.load('graphics/interface/shield.png').convert_alpha()
            shield_1 = pygame.transform.scale(shield_1, (40,40))
            shield_2 = pygame.image.load('graphics/interface/shield_blank.png').convert_alpha()
            shield_2 = pygame.transform.scale(shield_2, (40,40))
            self.frames = [shield_1,shield_2]
            self.slot = 1
            self.row_number = 0
        if type == 'damaged':
            damaged_1 = pygame.image.load('graphics/interface/warning_white.png').convert_alpha()
            damaged_1 = pygame.transform.scale(damaged_1, (40,40))
            damaged_2 = pygame.image.load('graphics/interface/warning_yellow.png').convert_alpha()
            damaged_2 = pygame.transform.scale(damaged_2, (40,40))
            damaged_3 = pygame.image.load('graphics/interface/warning_red.png').convert_alpha()
            self.frames = [damaged_1,damaged_2]
            self.slot = 2
            self.row_number = 0
        if type == 'heavily_damaged':
            heavily_damaged_1 = pygame.image.load('graphics/interface/warning_white.png').convert_alpha()
            heavily_damaged_1 = pygame.transform.scale(heavily_damaged_1, (40,40))
            heavily_damaged_2 = pygame.image.load('graphics/interface/warning_red.png').convert_alpha()
            heavily_damaged_2 = pygame.transform.scale(heavily_damaged_2, (40,40))
            self.frames = [heavily_damaged_1,heavily_damaged_2]
            self.slot =3
            self.row_number = 0
        self.animation_index = 0
        self.row_number = nameplate_quantity
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midright = ((screen_width*0.82)-(self.slot*60),((screen_height*0.2)+(nameplate_quantity*100))))
    def rerect(self):
        self.rect.top = screen_height*0.2 + 35 + self.row_number*100
    def update(self):
        self.image = self.frames[self.animation_index]
        self.rerect()

class Buttons(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'nameplate':
            nameplate_1 = pygame.image.load('graphics/interface/interface_panel_name.png').convert_alpha()
            nameplate_1 = pygame.transform.scale(nameplate_1, (400,100))
            nameplate_2 = pygame.image.load('graphics/interface/interface_panel_name_green.png').convert_alpha()
            nameplate_2 = pygame.transform.scale(nameplate_2, (800,100))
            self.frames = [nameplate_1,nameplate_2]
        if type == "hazard":
            hazard_1 = pygame.image.load('graphics/interface/warning_yellow.png').convert_alpha()
            hazard_1 = pygame.transform.scale(hazard_1, (20,20))
            hazard_2 = pygame.image.load('graphics/interface/warning_red.png').convert_alpha()
            hazard_2 = pygame.transform.scale(hazard_2, (20,20))
            self.frames = [hazard_1,hazard_2]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midright = ((screen_width*0.8),((screen_height*0.2)+(nameplate_quantity*100))))
        self.row_number = nameplate_quantity
    def buttons_input(self):
        keys = pygame.key.get_pressed()
        global cooldown
        # if keys[pygame.K_SPACE]:
            # if cooldown == 0:
                # if self.animation_index == 0:
                    # self.animation_index = 1
                    # self.rect.right = screen_width*0.8
                # else:
                    # self.animation_index = 0
                    # self.rect.right = screen_width*0.8
                # print(self.animation_index)
                # cooldown = 20
    def destroy(self):
        if self.nameplate_quantity >= 5:
            self.kill()
    def rerect(self):
        self.rect.right = screen_width*0.8
        self.rect.top = screen_height*0.2 + self.row_number*100
        
    def toggle_expand(self):
        global cooldown
        global pos
        if event.type == pygame.MOUSEBUTTONDOWN: #Click
            if self.rect.collidepoint(event.pos): #Toggle expand
                if cooldown == 0:
                    if self.animation_index == 0:
                        self.animation_index = 1
                        self.rect = pygame.Rect.inflate(self.rect, +400, 0)
                        self.rect.right = screen_width*0.8
                    else:
                        self.animation_index = 0
                        self.rect = pygame.Rect.inflate(self.rect, -400, 0)
                        self.rect.right = screen_width*0.8
                cooldown = 10
    def update(self):
        self.toggle_expand()
        self.rerect()
        self.destroy
        self.image = self.frames[self.animation_index]
        self.rerect()
        self.rect.right = screen_width*0.8
        
game_active = True
nameplate_quantity_max = 4

buttons_group = pygame.sprite.Group()   
health_icon_group = pygame.sprite.Group()

def add_health_tracker():
    global nameplate_quantity
    nameplate_quantity += 1
    buttons_group.add(Buttons('nameplate'))
    health_icon_group.add(Health_Icons('shield'))
    health_icon_group.add(Health_Icons('damaged'))
    health_icon_group.add(Health_Icons('heavily_damaged'))
    

add_health_tracker()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_active:
        pos = pygame.mouse.get_pos()
        if cooldown == 0:
            # nameplate_quantity = len(buttons_group)
            if nameplate_quantity < nameplate_quantity_max:
                add_health_tracker()
        cooldown -= 1
        if cooldown <= 0:
            cooldown = 0
        screen.fill((0,0,0))
        buttons_group.update()
        buttons_group.draw(screen)
        health_icon_group.update()
        health_icon_group.draw(screen)
    else:
        screen.fill((0,0,0))
    pygame.display.update()
    clock.tick(60)