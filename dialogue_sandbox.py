# sandbox

import pygame
# import random
from sys import exit
# import os
# import copy
# from math import atan2, degrees, pi
import json

# none = "none"
BLACK = (0, 0, 0)
continue_button = False

# load screen
screen_width = 1280
screen_height = 720
centerpoint = (screen_width / 2, screen_height / 2)
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("mission_control")
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 20)
clock = pygame.time.Clock()


def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    y = rect.top
    line_spacing = 10
    # get the height of the font
    font_height = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
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
        y += font_height + line_spacing
        # remove the text we just blitted
        text = text[i:]

    return text


class GameManager:
    def __init__(self):
        self.dialogue_active = False
        self.combat_active = False
        self.scene_id = "intro"
        self.debug_mode = False

class GraphicsManager:
    def __init__(self):
        # self.fullscreen_rect = pygame.Rect((screen_width, screen_height), (center=(screen_width/2,screen_height/2)))
        self.green_filter = pygame.image.load("graphics/interface/green_filter_65.png").convert_alpha()
        self.full_window_frame = pygame.image.load("graphics/interface/frames/full_frame.png").convert_alpha()
        self.vertical_bar = pygame.image.load("graphics/interface/frames/vertical_bar.png")

        self.green_filter = pygame.transform.scale(self.green_filter, (screen_width * 1, screen_height * 1))
        self.full_window_frame = self.resize(self.full_window_frame, (screen_width * 0.95, screen_height * 0.95))
        self.fullscreen_rect = self.full_window_frame.get_rect(center=(screen_width / 2, screen_height / 2))
        self.vertical_bar = self.resize(self.vertical_bar, (screen_width * 0.01, screen_height * 0.92))

    def resize(self, image, size):
        image = pygame.transform.scale(image, size)
        return image

    def draw_window_frames(self):
        screen.blit(self.full_window_frame, self.fullscreen_rect)
        screen.blit(self.vertical_bar, (screen_width * 0.7, screen_height * 0.05))

    # screen.blit(self.right_window_frame, (screen_width*0.6, screen_height*0))

    def update(self):
        screen.fill((0, 0, 0))
        dialogue.update()
        self.draw_window_frames()
        screen.blit(self.green_filter, (0, 0))


class DialogueManager:
    def __init__(self):
        self.scene = "null"
        self.line_number = 1
        self.line = " "
        self.speaker = "null"
        self.mood = "default"
        self.text = "null"
        self.portrait = pygame.image.load("graphics/blank.png").convert_alpha()
        self.text_box = pygame.Rect((screen_width * 0.05, screen_height * 0.25),
                                    (screen_width * 0.6, screen_height * 0.5))
        self.data = json.load(open("data/dialogue_data.json", "r"))
        self.available_choice = False
        self.scene = self.data["Nasha demands a duel"]
        self.section = self.scene["intro"]

    def select_choice(self, choice_number):
        try:
            print(f"You selected option {choice_number}")
            choices = self.line["choices"]
            choice = choices[choice_number - 1]
            print(choices)
            print(choice["text"])
        except(Exception, ):
            print("Error: something went wrong while selecting a choice")

        try:
            section = choice["next_section"]
            self.section = self.scene[section]
            print(section)
        except(Exception, ):
            self.section = "intro"

        try:
            self.line_number = choice["next_line"]
        except(Exception, ):
            self.line_number = 1
        print(self.line_number)

        try:
            game_effects = choice["game_effects"]
        except(Exception, ):
            game_effects = "none"

    def update(self):
        try:
            line = self.section[f"line {self.line_number}"]
            self.line = line
            name = line["speaker"]
            self.available_choice = False
            mood = "default"
            if name != "Player":
                try:
                    self.mood = line["mood"]
                    mood = self.mood
                except(Exception, ):
                    mood = self.mood
            elif name == "Player":
                try:
                    self.available_choice = line["available_choice"]
                    if self.available_choice == "False":
                        self.available_choice = False
                    elif self.available_choice == "True":
                        self.available_choice = True
                except(Exception, ):
                    pass

            # update portrait
            try:
                try:
                    self.portrait = pygame.image.load(f"graphics/pilots/{name}/{mood}.png")
                except(Exception, ):
                    self.portrait = pygame.image.load(f"graphics/pilots/{name}/default.png")
                self.portrait = pygame.transform.scale(self.portrait, (screen_height * 0.45, screen_height * 0.9))
                screen.blit(self.portrait, (screen_width * 0.7, screen_height * 0.07))
            except(Exception, ):
                print("unable to update portrait")

            # update text
            try:
                if not self.available_choice:
                    self.text = line["text"]
                    draw_text(screen, self.text, (255, 255, 255), self.text_box, text_font_small)
                elif self.available_choice:
                    choices = line["choices"]
                    choice_number = 1
                    for choice in choices:
                        text = choice["text"]
                        text = f"{choice_number}) {text}"
                        rect = pygame.Rect((screen_width * 0.05, screen_height * (0.25 + (choice_number - 1) / 7)),
                                           (screen_width * 0.6, screen_height * 0.5))
                        draw_text(screen, text, (255, 255, 255), rect, text_font_small)
                        choice_number += 1

                else:
                    print("something went wrong")
            except(Exception, ):
                print("unable to draw text")
        except(Exception, ):
            pass
        # print("Error: unable to update dialogue")


class Pilot:
    def __init__(self, name):
        self.name = name
        self.mood = "default"


game = GameManager()
dialogue = DialogueManager()
graphics = GraphicsManager()

# pilots
Rose = Pilot("Rose")
nasha = Pilot("Nasha")
roger = Pilot("Roger")

while True:  # game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            # toggle debug mode
            if event.key == pygame.K_q:
                if not game.debug_mode:
                    game.debug_mode = True
                    print("debug_mode enabled")
                elif game.debug_mode:
                    game.debug_mode = False
                    print("debug_mode disabled")

            # cycle through dialogue scenes
            if event.key == pygame.K_x:
                print("starting scene:", dialogue.scene["scene_id"])
                if dialogue.scene == dialogue.data["Nasha demands a duel"]:
                    dialogue.scene = dialogue.data["Baal's satellite crash"]
                elif dialogue.scene == dialogue.data["Baal's satellite crash"]:
                    dialogue.scene = dialogue.data["Rose social intro"]
                elif dialogue.scene == dialogue.data["Rose social intro"]:
                    dialogue.scene = dialogue.data["Nasha demands a duel"]
                print("new current scene:", dialogue.scene["scene_id"])
                dialogue.line_number = 1
                dialogue.mood = "default"
                dialogue.section = dialogue.scene["intro"]

            # get details of current dialogue
            if event.key == pygame.K_c:
                try:
                    print(dialogue.scene["scene_id"])
                except(Exception, ):
                    print("Error: invalid scene_id")
                try:
                    print(dialogue.section["section_id"])
                except(Exception,):
                    print("Error: invalid section_id")
                try:
                    print(dialogue.line_number)
                except(Exception,):
                    print("Error: invalid line_number somehow")

            # dialogue choices
            if not dialogue.available_choice:
                if event.key == pygame.K_d:
                    try:
                        dialogue.line_number += 1
                    except(Exception, ):
                        print("Error: unable to advance dialogue line")
                if event.key == pygame.K_a:
                    try:
                        dialogue.line_number -= 1
                    except(Exception, ):
                        print("Error: unable to reverse dialogue line")

            if dialogue.available_choice:
                if event.key == pygame.K_1:
                    dialogue.select_choice(1)
                elif event.key == pygame.K_2:
                    dialogue.select_choice(2)
                elif event.key == pygame.K_3:
                    dialogue.select_choice(3)
                elif event.key == pygame.K_4:
                    dialogue.select_choice(4)

    graphics.update()
    pygame.display.update()
    clock.tick(60)
