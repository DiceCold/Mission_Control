import pygame
import settings


class text_label(pygame.sprite.Sprite):
    def __init__(self, type, list_index, text=""):
        super().__init__()
        self.type = type
        self.list_index = list_index
        self.text = text
        self.active = False
        self.animation_index = 0

        # set text
        try:
            if self.type == "Pilot":
                self.reference = pilot_roster[self.list_index]
                self.text = self.reference.name
            elif self.type == "button":
                self.text = text
        except:
            self.text = "error: invalid text"

    def update_text(self):
        try:
            if self.type == "Pilot":
                self.reference = pilot_roster[self.list_index]
                self.text = self.reference.name
            elif self.type == "button":
                self.text = "text"
        except:
            self.text = "error: invalid text"


text_label_group = pygame.sprite.Group()
pilot_roster = pygame.sprite.Group()
