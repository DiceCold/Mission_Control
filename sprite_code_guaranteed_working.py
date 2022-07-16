import pygame
from sys import exit
from random import randint, choice


pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
global cooldown
cooldown = 0
nameplate_quantity = 0


class Buttons(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'nameplate':
            nameplate_1 = pygame.image.load('graphics/interface/interface_panel_name.png').convert_alpha()
            nameplate_1 = pygame.transform.scale(nameplate_1, (200,50))
            nameplate_2 = pygame.image.load('graphics/interface/interface_panel_name_green.png').convert_alpha()
            nameplate_2 = pygame.transform.scale(nameplate_2, (200,50))
            self.frames = [nameplate_1,nameplate_2]
        if type == "hazard":
            hazard_1 = pygame.image.load('graphics/interface/warning_yellow.png').convert_alpha()
            hazard_1 = pygame.transform.scale(hazard_1, (20,5))
            hazard_2 = pygame.image.load('graphics/interface/warning_red.png').convert_alpha()
            hazard_2 = pygame.transform.scale(hazard_2, (20,5))
            self.frames = [hazard_1,hazard_2]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (600,(600+nameplate_quantity*100)))
    def buttons_input(self):
        keys = pygame.key.get_pressed()
        global cooldown
        if keys[pygame.K_SPACE]:
            if cooldown == 0:
                if self.animation_index == 0:
                    self.animation_index = 1
                else:
                    self.animation_index = 0
                print(self.animation_index)
                cooldown = 60
    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()
    def toggle_button(self):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.animation_index = 1
                print(self.animation_index)
            else:
                self.animation_index = 0
                print(self.animation_index)
    def update(self):
        self.buttons_input()
        self.toggle_button()
        self.image = self.frames[self.animation_index]

game_active = True
buttons_group = pygame.sprite.Group()
buttons_group.add(Buttons('nameplate'))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_active:
        if cooldown == 50:
            nameplate_quantity = len(buttons_group)
            buttons_group.add(Buttons('nameplate'))
        cooldown -= 1
        if cooldown <= 0:
            cooldown = 0
        buttons_group.update()
        buttons_group.draw(screen)
    else:
        screen.fill((94,129,162))
    pygame.display.update()
    clock.tick(60)