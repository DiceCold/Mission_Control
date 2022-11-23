#dialogue module
import pygame
from settings import *

class Speaker:
    def __init__(self, name):
        self.name = name
        self.mood = "default"
        
        self.image_default = self.import_image("default")
        self.image_happy = self.import_image("happy")
        self.image_serious = self.import_image("serious")
        self.image_concerned = self.import_image("concerned")
        self.image_fierce = self.import_image("fierce")
        self.image_surprised = self.import_image("surprised")
        self.images = {"default":self.image_default, "happy":self.image_happy, "serious":self.image_serious, "concerned":self.image_concerned, "fierce":self.image_fierce, "surprised":self.image_surprised}
    
    def import_image(self, mood): #imports and scales the speaker's image for a specific mood
        try: image = pygame.image.load(f"graphics/pilots/{self.name}/{mood}.png").convert_alpha()
        except: 
            image = pygame.image.load(f"graphics/pilots/{self.name}/default.png").convert_alpha()
            if debug_mode == True: print("Error: image for", self.name, mood, "is missing. Substituting default image.")
        image = pygame.transform.scale(image, (screen_height*0.36 , screen_height*0.8))
        return image
    
    def update(self):
        #update speaker's image based on current mood
        try: self.image = self.images[self.mood]
        except:
            self.image = self.image_default
            if debug_mode == True: print("Error: unable to correctly assign speaker's image based on mood for", self.name, self.mood)
        
            

speaker_kite = Speaker("Kite")

class Dialogue:
    def __init__(self):
        self.conversation_topic = "select_mood"
        self.conversation_stage = 1
        self.choices = []
        self.cooldown_max = 20
        self.cooldown = self.cooldown_max
        
        self.speaker_right = speaker_kite
        self.speaker_left = "null"
        self.current_lines = "Hello, and welcome to the Mission Control Testing Environment"
        self.font = pygame.font.Font("font/Pixeltype.ttf", 50)
        self.text_rect = pygame.Rect((screen_width*0.2, screen_height*0.75),(screen_width*0.6, screen_height*0.15))
        
        self.box_surf = pygame.image.load("graphics/interface/dialogue_box_back.png").convert_alpha()
        self.box_surf = pygame.transform.scale(self.box_surf, (screen_width*0.8, screen_height*0.2))
        self.box_rect = self.box_surf.get_rect(center = (screen_width*0.5, screen_height*0.8))
        
        self.speaker_right_rect = pygame.Rect((screen_width*0.8, screen_height*0.1),(screen_width*0.36, screen_height*0.8))
        
    def draw_text(self, surface, text, color, rect, font, aa=False, bkg=None):
        y = rect.top
        lineSpacing = 10
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
    
    def make_choice(self, option_number=1):
        if self.cooldown > 0: pass
        else:
            if self.conversation_topic == "select_mood" and self.conversation_stage == 2: #select a mood
                if option_number == 1: self.speaker_right.mood = "default"
                elif option_number == 2: self.speaker_right.mood = "happy"
                elif option_number == 3: self.speaker_right.mood = "serious"
                elif option_number == 4: self.speaker_right.mood = "surprised"
                
                self.cooldown = self.cooldown_max
                self.conversation_stage += 1
                
    def advance_dialogue(self):
        self.conversation_stage += 1
        if debug_mode == True: print("Converation stage advanced to:", self.conversation_stage)
        self.cooldown = self.cooldown_max
    
    def display_choices(self):
        if len(self.choices) >= 1:
            image = self.font.render(self.choices[0], False, (250,250,250))
            screen.blit(image, (screen_width*0.2, screen_height*0.8))
        if len(self.choices) >= 2:
            image = self.font.render(self.choices[1], False, (250,250,250))
            screen.blit(image, (screen_width*0.6, screen_height*0.8))
        if len(self.choices) >= 3:
            image = self.font.render(self.choices[2], False, (250,250,250))
            screen.blit(image, (screen_width*0.2, screen_height*0.85))
        if len(self.choices) >= 4:
            image = self.font.render(self.choices[3], False, (250,250,250))
            screen.blit(image, (screen_width*0.6, screen_height*0.85))
    
    def update_text(self):
        if self.conversation_topic == "select_mood":
            if self.conversation_stage == 1: self.current_lines = "Hello, and welcome to the Mission Control Testing Environment"
            elif self.conversation_stage == 2: 
                self.current_lines = "Select a mood for the character to express:"
                self.choices = ["1) default", "2) happy", "3) serious", "4) surprised"]
            elif self.conversation_stage == 3:
                self.current_lines = f"You chose {self.speaker_right.mood}"
                self.choices = []
    
    def update(self):
        self.update_text()
        if self.cooldown > 0: self.cooldown -= 1 #reduce cooldown
        self.speaker_right.update() #update speaker's image
        screen.blit(self.speaker_right.image, self.speaker_right_rect) #draw speaker
        screen.blit(self.box_surf, self.box_rect) #draw box background
        self.display_choices()
        self.draw_text(screen, self.current_lines, (250,250,250), self.text_rect, self.font) #draw text

        