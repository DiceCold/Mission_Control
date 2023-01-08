import pygame
from settings import *
import modules.navigation_module as nav
from settings import pixel_font_15


def highlight_pilot(mouse_pos, pilot):
    if pilot.rect.left < mouse_pos[0] < pilot.rect.right and pilot.rect.top < mouse_pos[1] < pilot.rect.bottom:
        pilot.highlighted = True
    elif pilot.selected:
        pilot.highlighted = True
    else:
        pilot.highlighted = False
    # set color based on if highlighted
    pilot.handle_highlight()


def issue_orders(pilot, target_type, mouse_pos):
    if pilot.targeting_mode == "manual":
        if target_type == "waypoint":
            pilot.target["move"] = nav.Waypoint(mouse_pos[0], mouse_pos[1])

            print(f"{pilot.name} is targeting waypoint {mouse_pos}")


class InterfaceManager:
    def __init__(self, game_manager):
        self.game = game_manager
        self.click_cooldown_max = 25
        self.click_cooldown = self.click_cooldown_max

        self.buttons = pygame.sprite.Group()
        self.button_labels = pygame.sprite.Group()

        self.selected_pilot = None

        self.menu = MenuManager(self.game)
        self.status_frame_manager = StatusFrameManager(self.game)

    def reset_cooldown(self):
        self.click_cooldown = self.click_cooldown_max

    def create_button(self, button_type, text, pos_x, pos_y, width=screen_width * 0.2, height=screen_height * 0.15):
        button = Button(button_type, pos_x, pos_y, width, height)
        self.buttons.add(button)
        label = TextLabel("button", button, text)
        self.button_labels.add(label)

    def highlight_button(self, mouse_pos):
        for button in self.buttons:
            if button.status != "hidden":
                rect = button.rect
                # highlight if mouse collides with rect
                if rect.left < mouse_pos[0] < rect.right and rect.top < mouse_pos[1] < rect.bottom:
                    button.status = "highlight"
                else:
                    button.status = "default"

    def select_pilot(self, pilot):
        pilot.selected = True
        # change to manual depends if I want to see their current target or just override it
        pilot.targeting_mode = "manual"
        self.selected_pilot = pilot
        print(f"{pilot.name} selected")

    def deselect_pilot(self, pilot):
        pilot.selected = False
        self.selected_pilot = None
        print(f"{pilot.name} deselected")

    def update(self):
        game = self.game
        mouse_pos = pygame.mouse.get_pos()

        # tick down the cooldown on clicking
        if self.click_cooldown > 0:
            self.click_cooldown -= 1

        # highlight pilots on mouseover when combat is paused
        if game.mode == "combat" and game.paused:
            # check to see if mouse intersects with pilot's rect
            for pilot in game.pilots:
                highlight_pilot(mouse_pos, pilot)
        # try:
        #     if game.mode == "combat" and game.paused is False:
        #         # make sure no pilot is highlighted if combat is unpaused
        #         game.pilots.deselect()
        # except(Exception, ):
        #     pass

        # highlight button on mouseover when game is paused
        if game.paused:
            self.highlight_button(mouse_pos)

        self.status_frame_manager.update_status_frames()


class TextLabel(pygame.sprite.Sprite):
    def __init__(self, label_type, reference, text=""):
        super().__init__()
        self.label_type = label_type
        self.reference = reference
        self.text = text
        self.active = True
        self.status = "default"
        self.pos_x = reference.pos_x
        self.pos_y = reference.pos_y
        self.font = text_font
        self.color = (0, 0, 0)
        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def update(self):
        if self.label_type == "button":
            # update based on reference
            self.status = self.reference.status
            self.pos_x = self.reference.pos_x
            self.pos_y = self.reference.pos_y
            self.active = self.reference.active
            # update image
            self.image = self.font.render(self.text, False, self.color)
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))


class MenuManager:
    def __init__(self, game_manager):
        self.game = game_manager
        self.menu_type = "combat"
        self.hidden = True

        self.pos_x = screen_width*0.5
        self.pos_y = screen_height*0.5
        self.width = screen_width*0.5
        self.height = screen_height*0.3

        self.back_image = pygame.image.load("graphics/menu/menu_back.png").convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (self.width, self.height))
        self.back_rect = self.back_image.get_rect(center=(self.pos_x, self.pos_y))

        self.menu_options = []

    def load_menu(self, menu_type, pos_x, pos_y, width, height):
        self.menu_type = menu_type
        self.hidden = False
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

        # update back image since positions/dimensions may change
        # self.back_image = pygame.image.load("graphics/menu/menu_back.png").convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (self.width, self.height))
        self.back_rect = self.back_image.get_rect(center=(self.pos_x, self.pos_y))

        self.update_menu_options()

    def draw_menu(self):
        # draw back of menu
        screen.blit(self.back_image, self.back_rect)

        # draw options
        for option in self.menu_options:
            text = option
            color = (0, 0, 0)
            index = self.menu_options.index(option)
            print(text, color, index)
            image = text_font_small.render(text, False, color)
            pos_x = self.pos_x - self.width*0.4
            pos_y = self.pos_y - self.height * 0.4
            rect = image.get_rect(topleft=(pos_x, pos_y + self.height*0.15*(index + 1)))
            screen.blit(image, rect)

    def update_menu_options(self, reference=None):
        if self.menu_type == "combat":
            if reference is not None:
                self.menu_options = [
                    f"Selected Pilot: {reference.name}",
                    f"Targeting Mode: {reference.targeting_mode}",
                    "Select Target",
                    "Redirect Power",
                    "Activate Ability"
                ]


class StatusFrameManager:
    def __init__(self, game_manager):
        self.game = game_manager
        self.hidden = False
        self.status_frame_group = []

    def update_frame_quantity(self):
        pilot_quantity = len(self.game.pilots)
        status_frame_quantity = len(self.status_frame_group)
        # if there are fewer frames than pilots add another status_frame
        if status_frame_quantity < pilot_quantity:
            status_frame = PilotFrame(status_frame_quantity, self.game.pilots)
            self.status_frame_group.append(status_frame)
        # if there are more frames than pilots delete the last status_frame from the list
        elif status_frame_quantity > pilot_quantity:
            del(self.status_frame_group[-1])
            
    def update_status_frames(self):
        self.update_frame_quantity()
        for status_frame in self.status_frame_group:
            status_frame.update_status_frame()
    
    def draw_status_frames(self):
        for status_frame in self.status_frame_group:
            status_frame.draw_status_frame()


class PilotFrame:
    def __init__(self, index, pilot_list):
        self.index = index
        self.pilot_list = pilot_list
        self.text_color = (255, 255, 255)

        # try to load the info for the pilot based on position in list
        try:
            self.pilot = self.pilot_list[self.index]
            self.name = self.pilot.name
            self.overcharge_system = self.pilot.overcharge_system
        except(Exception, ):
            self.pilot = None
            self.name = "default"
            self.overcharge_system = {
                "red": False,
                "blue": True,
                "green": False
            }

        self.width = screen_width*0.2
        self.height = screen_height*0.05
        self.pos_x = screen_width*0.01
        self.pos_y = self.height*(self.index + 1)
        self.name_pos_x = self.pos_x+self.width*0.05
        self.name_pos_y = self.pos_y + self.height * 0.2

        # add overcharge button lights
        circle_size = screen_width*0.01
        red_pos = (self.pos_x + self.width*0.8, self.pos_y + self.height*0.3)
        blue_pos = (self.pos_x + self.width*0.85, self.pos_y + self.height*0.3)
        green_pos = (self.pos_x + self.width * 0.9, self.pos_y + self.height * 0.3)
        size = (circle_size, circle_size)
        self.red_light = Button("overcharge_light", red_pos[0], red_pos[1], circle_size, circle_size, "red", self.pilot)
        self.blue_light = Button("overcharge_light", blue_pos[0], blue_pos[1], circle_size, circle_size, "blue", self.pilot)
        self.green_light = Button("overcharge_light", green_pos[0], green_pos[1], circle_size, circle_size, "green", self.pilot)
        self.light_group = pygame.sprite.Group()
        self.light_group.add(self.red_light, self.blue_light, self.green_light)
        
        # add toggle for automatic control
        # toggle
        auto_size = (self.width*0.25, self.height*0.35)
        auto_pos = (self.pos_x + self.width * 0.85, self.pos_y + self.height * 0.65)
        self.toggle_auto = Button("toggle_auto", auto_pos[0], auto_pos[1], auto_size[0], auto_size[1], None, self.pilot)
        self.toggle_group = pygame.sprite.Group(self.toggle_auto)
        # text labels
        # self.manual_text_image = text_font_micro.render("Manual", False, (0, 0, 0))
        self.auto_text_image = pixel_font_15.render("AUTO", False, (255, 255, 255))
        self.auto_text_rect = self.auto_text_image.get_rect(center=(self.pos_x+self.width*0.9, self.pos_y+self.height*0.7))

        # load backing image
        self.back_image = pygame.image.load("graphics/pilot_frames/frame_back_4.png").convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (self.width, self.height))
        self.back_rect = self.back_image.get_rect(topleft=(self.pos_x, self.pos_y))
        # load text image
        self.name_text_image = text_font.render(self.name, False, self.text_color)
        self.name_text_rect = self.name_text_image.get_rect(topleft=(self.name_pos_x, self.name_pos_y))

        # load status icons for shield and damage
        shield_icon = StatusIcon("shield", self.pos_x+self.width*0.5, self.pos_y+self.height*0.2, self.width*0.1, self.width*0.1, self.pilot)
        damage_icon = StatusIcon("damage", self.pos_x+self.width*0.6, self.pos_y+self.height*0.2, self.width*0.1, self.width*0.1, self.pilot)
        self.status_icon_group = pygame.sprite.Group(shield_icon, damage_icon)

    def update_auto_toggle_labels(self):
        if self.pilot.targeting_mode == "automatic":
            self.auto_text_image = pixel_font_15.render("AUTO", False, (255, 255, 255))
        else:
            self.auto_text_image = pixel_font_15.render("AUTO", False, (0, 0, 0))

    def draw_auto_toggle_labels(self):
        screen.blit(self.auto_text_image, self.auto_text_rect)

    def update_overcharge_lights(self):
        if self.pilot is not None:
            self.overcharge_system = self.pilot.overcharge_system
        for light in self.light_group:
            if self.overcharge_system[f"{light.color}"]:
                light.status = "overcharged"
            else:
                light.status = "default"
        self.light_group.update()

    def draw_status_icons(self):
        self.status_icon_group.draw(screen)

    def update_status_frame(self):
        self.update_overcharge_lights()
        # try to load the info for the pilot based on position in list
        # I'm sure there's a better way to get the position of an object in the sprite group, but this works for now
        list_position = -1
        for pilot in self.pilot_list:
            list_position += 1
            if list_position == self.index:
                self.pilot = pilot

        if self.pilot is not None:
            self.name = self.pilot.name
            # update overcharge lights
            self.overcharge_system = self.pilot.overcharge_system
            for i in self.light_group:
                i.reference = self.pilot
            # update status icons
            for i in self.status_icon_group:
                i.reference = self.pilot
            self.status_icon_group.update()

            # update toggle for automatic control
            self.toggle_auto.reference = self.pilot
            self.toggle_auto.status = self.pilot.targeting_mode
            self.toggle_auto.update()
            self.update_auto_toggle_labels()
        # except(Exception,):
        #     self.pilot = None
        #     self.name = "default"
        # update image and rect for text
        self.name_text_image = text_font.render(self.name, False, self.text_color)
        self.name_text_rect = self.name_text_image.get_rect(topleft=(self.name_pos_x, self.name_pos_y))

    def draw_status_frame(self):
        if self.pilot is not None:
            # draw the back
            screen.blit(self.back_image, self.back_rect)
            # draw text name
            screen.blit(self.name_text_image, self.name_text_rect)
            # draw overcharge lights
            # screen.blit(self.red_image, self.red_rect)
            # screen.blit(self.blue_image, self.blue_rect)
            # screen.blit(self.green_image, self.green_rect)
            self.light_group.draw(screen)
            self.toggle_group.draw(screen)
            self.draw_auto_toggle_labels()
            self.draw_status_icons()


class StatusIcon(pygame.sprite.Sprite):
    def __init__(self, icon_type, pos_x=0, pos_y=0, width=screen_width*0.1, height=screen_height*0.1, reference=None):
        super().__init__()
        self.icon_type = icon_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.reference = reference

        # load images
        if self.icon_type == "shield":
            self.shield_icon_blue = pygame.image.load("graphics/icons/shield.png").convert_alpha()
            self.shield_icon_black = pygame.image.load("graphics/icons/shield_icon_black.png").convert_alpha()
            self.shield_icon_blue = pygame.transform.scale(self.shield_icon_blue, (self.width, self.height))
            self.shield_icon_black = pygame.transform.scale(self.shield_icon_black, (self.width, self.height))
            self.image = self.shield_icon_blue
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        if self.icon_type == "damage":
            self.damage_icon_white = pygame.image.load("graphics/icons/warning_white.png").convert_alpha()
            self.damage_icon_red = pygame.image.load("graphics/icons/warning_red.png").convert_alpha()
            self.damage_icon_yellow = pygame.image.load("graphics/icons/warning_yellow.png").convert_alpha()
            self.damage_icon_white = pygame.transform.scale(self.damage_icon_white, (self.width, self.height))
            self.damage_icon_red = pygame.transform.scale(self.damage_icon_red, (self.width, self.height))
            self.damage_icon_yellow = pygame.transform.scale(self.damage_icon_yellow, (self.width, self.height))
            self.image = self.damage_icon_white
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def update_shield_icon(self):
        if self.reference is not None:
            if self.reference.shielded:
                self.image = self.shield_icon_blue
            else:
                self.image = self.shield_icon_black

    def update_damage_icon(self):
        if self.reference is not None:
            # show icon as white if > 60% health
            if self.reference.hp_current > self.reference.hp_max*0.6:
                self.image = self.damage_icon_white
            # show as yellow if > 30% health
            elif self.reference.hp_current > self.reference.hp_max*0.3:
                self.image = self.damage_icon_yellow
            # show as red if < 30% health
            else:
                self.image = self.damage_icon_red

    def update_reference(self, reference):
        self.reference = reference

    def update(self):
        if self.icon_type == "shield":
            self.update_shield_icon()
        elif self.icon_type == "damage":
            self.update_damage_icon()
        else:
            print(self.icon_type)

    def draw_icon(self):
        screen.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, button_type, pos_x=0, pos_y=0, width=100, height=100, color=None, reference=None):
        super().__init__()
        self.button_type = button_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.active = True
        # set status between default, hidden, and highlight
        self.status = "default"
        # set cooldown/max
        self.cooldown_max = 25
        self.cooldown = self.cooldown_max
        self.color = color
        self.reference = reference

        if self.button_type == "x_button":
            self.frame_1 = pygame.image.load("graphics/icons/x_button.png").convert_alpha()
            self.frame_1 = pygame.transform.scale(self.frame_1, (screen_width*0.05,screen_height*0.05))
            self.pos_x = screen_width*0.2
            self.pos_y - screen_height*0.2
        
        elif self.button_type == "dashboard_map":
            self.animation_index = 1
            self.pos_x = screen_width*0.1
            self.pos_y = screen_height*0.15
            self.frame_1 = pygame.image.load("graphics/interface/cockpit/clickscreen.png").convert_alpha()
            self.frame_1 = pygame.transform.scale(self.frame_1, (screen_width*0.2,screen_height*0.2))
        
        elif self.button_type == "continue_button":
            self.pos_x = screen_width*0.15
            self.pos_y = screen_height*0.14
            self.width = screen_width*0.2
            self.height = screen_height*0.07
            self.frame_1 = pygame.image.load("graphics/interface/labels/continue_button.png")
            self.frame_1 = pygame.transform.scale(self.frame_1, (self.width,self.height))
        
        elif button_type == "swap_button":
            self.width = screen_width*0.2
            self.height = screen_height*0.15
            self.pos_x = screen_width*0.5
            self.pos_y = screen_height*0.85 
            self.match = False
            self.frame_1 = pygame.image.load("graphics/interface/labels/label_white_selected_lowres.png").convert_alpha()
            self.frame_1 = pygame.transform.scale(self.frame_1,(self.width,self.height))
            self.frame_2 = pygame.image.load("graphics/interface/labels/noswap_label.png").convert_alpha()
            self.frame_2 = pygame.transform.scale(self.frame_2,(self.width,self.height))
        
        elif button_type == "dispatch_button":
            self.width = screen_width*0.2
            self.height = screen_height*0.15
            self.pos_x = screen_width*0.5
            self.pos_y = screen_height*0.85 
            self.frame_1 = pygame.image.load("graphics/interface/labels/label_white_selected_lowres.png").convert_alpha()
            self.frame_1 = pygame.transform.scale(self.frame_1, (self.width, self.height))

        elif button_type == "overcharge_light":
            # load overcharge-light images
            self.on_image = pygame.image.load(f"graphics/icons/{self.color}_light_on.png").convert_alpha()
            self.on_image = pygame.transform.scale(self.on_image, (self.width, self.width))
            self.off_image = pygame.image.load(f"graphics/icons/{self.color}_light_off.png").convert_alpha()
            self.off_image = pygame.transform.scale(self.off_image, (self.width, self.width))
            self.status = "overcharged"
            self.images = {
                "default": self.off_image,
                "overcharged": self.on_image
            }
            self.image = self.images[self.status]
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        elif button_type == "toggle_auto":
            self.auto_image = pygame.image.load("graphics/pilot_frames/toggle_auto_2.png").convert_alpha()
            self.auto_image = pygame.transform.scale(self.auto_image, (self.width, self.height))
            self.manual_image = pygame.image.load("graphics/pilot_frames/toggle_manual_2.png").convert_alpha()
            self.manual_image = pygame.transform.scale(self.manual_image, (self.width, self.height))
            self.status = "automatic"
            self.images = {
                "automatic": self.auto_image,
                "manual": self.manual_image
            }
            self.image = self.images[self.status]
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        elif button_type == "default_button":
            # set dimensions
            self.width = screen_width * 0.2
            self.height = screen_height * 0.15

            # set images
            self.image_hidden = pygame.image.load("graphics/blank.png").convert_alpha()
            self.image_hidden = pygame.transform.scale(self.image_hidden, (self.width, self.height))
            self.image_default = pygame.image.load("graphics/buttons/button1_default.png").convert_alpha()
            self.image_default = pygame.transform.scale(self.image_default, (self.width, self.height))
            self.image_highlight = pygame.image.load("graphics/buttons/button1_highlight.png").convert_alpha()
            self.image_highlight = pygame.transform.scale(self.image_highlight, (self.width, self.height))
            self.images = {
                "hidden": self.image_hidden,
                "default": self.image_default,
                "highlight": self.image_highlight
            }
            self.image = self.image_default
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def update_image(self):
        # self.image = self.images(self.status)
        self.image = self.images[self.status]
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def toggle_auto(self):
        targeting_mode = self.reference.targeting_mode
        # update pilot's targeting mode
        if targeting_mode == "automatic":
            targeting_mode = "manual"
            print(self.reference.name, "switching to manual control")
        else:
            targeting_mode = "automatic"
            print(self.reference.name, "switching to automatic control")
        # update button status
        self.status = targeting_mode
        # update pilot targeting mode
        self.reference.targeting_mode = targeting_mode
        if targeting_mode == "automatic":
            self.reference.find_target(self.reference.target_list["enemies"])

    def toggle_light(self):
        # set all lights off so that only one can be lit at a time
        self.reference.overcharge_system["red"] = False
        self.reference.overcharge_system["blue"] = False
        self.reference.overcharge_system["green"] = False

        # switches status of overcharge light between default and overcharged
        if self.status == "default":
            self.status = "overcharged"
            self.reference.overcharge_system[f"{self.color}"] = True
        else:
            self.status = "default"
            self.reference.overcharge_system[f"{self.color}"] = False

    def click_button(self):
        # reset cooldown
        self.cooldown = self.cooldown_max
        print("You clicked a button")

        # toggle overcharge lights
        if self.button_type == "overcharge_light":
            print("status was: ", self.status)
            self.toggle_light()
            print("status is now", self.status)
            
        # toggle automatic/manual control mode
        if self.button_type == "toggle_auto":
            self.toggle_auto()

    def update(self):
        # reduce cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
        # update image based on status
        self.update_image()

        