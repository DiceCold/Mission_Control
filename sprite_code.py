import pygame
from sys import exit
from random import randint, choice

screen_width = 1920
screen_height = 1080

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
global cooldown
global pos
cooldown = 0
nameplate_quantity = 0
target_quantity = 0
wide_row = [False,False,False,False,False]
rose = "Intrepid Rose"
unassigned = "Unassigned"
pilot_target = [unassigned,rose]

mission_text_rect = pygame.Rect((400, 500), (600, 900))

pilot_names = ["Unassigned","Nighthawk","Lightbringer","Deadlift","Azure_Kite"]

mission_briefing = "This is a mission briefing for testing the text wrapping function. Go to the forbidden forest and kill some vampires. BTW also bring me the head of a lion. Hopefully this should be enough to wrap a couple of times."



def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    # rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

class Pilot_Names(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        global pilot_name
        global pilot_target
        global wide_row
        global nameplate_quantity
        global name_target
        global name_only
        if type == "pilot_name":
            pilot_name = pilot_names[nameplate_quantity]
            name_only = text_font.render(f'{pilot_name}',False,(111,196,169))
            name_target = text_font.render(f'{pilot_name} targeting:  {pilot_target[0]}',False,(111,196,169))
            self.frames = [name_only,name_target]
            self.name = pilot_name
        self.animation_index = 0
        self.name = pilot_names[nameplate_quantity]
        self.row_number = nameplate_quantity
        self.image = self.frames[self.animation_index]
        self.name_only = name_only
        self.rect = self.image.get_rect(midright = ((screen_width*0.80),((screen_height*0.2)+ 800 + (nameplate_quantity*100))))
    def rerect(self):
        self.rect.top = screen_height*0.2 + self.row_number*100 + 45
        if self.animation_index == 0:
            self.rect.left = screen_width*0.8 - 350
        else: self.rect.left = screen_width*0.8 - 750
    def check_row_wide(self):
        if wide_row[self.row_number] == True:
            self.animation_index = 1
        else: self.animation_index = 0
    def refresh_target_name(self):
        name_only = self.name_only
        pilot_name = self.name
        name_target = text_font.render(f'{pilot_name} targeting: {pilot_target[0]}',False,(111,196,169))
        self.frames = [name_only,name_target]
        self.image = self.frames[self.animation_index]
    def update(self):
        global pilot_target
        global name_target
        pilot_name = self.name
        name_only = self.name_only
        self.refresh_target_name()
        self.check_row_wide()
        self.frames = [name_only,name_target]
        self.image = self.frames[self.animation_index]
        self.rerect()
        self.refresh_target_name()

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
            self.slot = 3
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
            self.slot =1
            self.row_number = 0
        self.animation_index = 0
        self.row_number = nameplate_quantity
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midright = ((screen_width*0.82)-(self.slot*50)-10,((screen_height*0.2)+(nameplate_quantity*100))))
    def rerect(self):
        self.rect.top = screen_height*0.2 + 35 + self.row_number*100
    def update(self):
        self.image = self.frames[self.animation_index]
        self.rerect()

class Nameplates(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        global wide_row
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
    def check_row_wide(self):
        if self.animation_index == 0:
            wide_row[self.row_number] = False
        else: wide_row[self.row_number] = True
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
        self.check_row_wide()
        self.rerect()
        self.destroy
        self.image = self.frames[self.animation_index]
        self.rerect()
        self.rect.right = screen_width*0.8
        
class Target_Options(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        global target_quantity
        if type == 'nameplate':
            nameplate_1 = pygame.image.load('graphics/interface/interface_panel_name.png').convert_alpha()
            nameplate_1 = pygame.transform.scale(nameplate_1, (400,100))
            nameplate_2 = pygame.image.load('graphics/interface/interface_panel_name_green.png').convert_alpha()
            nameplate_2 = pygame.transform.scale(nameplate_2, (400,100))
            self.frames = [nameplate_1,nameplate_2]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midleft = ((screen_width*0.2),((screen_height*0.2)+(100))))
        self.row_number = target_quantity
    def buttons_input(self):
        keys = pygame.key.get_pressed()
        global cooldown
    def destroy(self):
        if self.row_number >= 4:
            self.kill()
    def rerect(self):
        self.rect.left = screen_width*0.2
        self.rect.top = screen_height*0.2 + self.row_number*100
    def become_target(self):
        global cooldown
        global pos
        global pilot_target
        if event.type == pygame.MOUSEBUTTONDOWN: #Click
            if self.rect.collidepoint(event.pos): #Select target
                pilot_target[0] = rose
                self.animation_index = 1
                cooldown = 10
    def update(self):
        self.destroy()
        self.become_target()
        self.image = self.frames[self.animation_index]
        self.rerect()
        
game_active = True
nameplate_quantity_max = 4

buttons_group = pygame.sprite.Group()   
health_icon_group = pygame.sprite.Group()
pilot_names_group = pygame.sprite.Group()
target_names_group = pygame.sprite.Group()

def add_health_tracker():
    global nameplate_quantity
    nameplate_quantity += 1
    buttons_group.add(Nameplates('nameplate'))
    health_icon_group.add(Health_Icons('shield'))
    health_icon_group.add(Health_Icons('damaged'))
    health_icon_group.add(Health_Icons('heavily_damaged'))
    pilot_names_group.add(Pilot_Names("pilot_name"))

add_health_tracker()
target_names_group.add(Target_Options('nameplate'))

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
        drawText(screen, mission_briefing, (64,64,64), mission_text_rect, text_font, False, None)
        buttons_group.update()
        buttons_group.draw(screen)
        health_icon_group.update()
        health_icon_group.draw(screen)
        pilot_names_group.update()
        pilot_names_group.draw(screen)
        target_names_group.update()
        target_names_group.draw(screen)
    else:
        screen.fill((0,0,0))
    pygame.display.update()
    clock.tick(60)