import pygame
from settings import *
import modules.navigation_module as nav


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
    pilot.targeting_mode = "manual"
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
        self.pilot_frame_manager = PilotFrameManager(self.game)

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
        try:
            if game.mode == "combat" and game.paused is False:
                # make sure no pilot is highlighted if combat is unpaused
                game.pilots.deselect()
        except(Exception, ):
            pass

        # highlight button on mouseover when game is paused
        if game.paused:
            self.highlight_button(mouse_pos)

        self.pilot_frame_manager.update_pilot_frames()


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


class PilotFrameManager:
    def __init__(self, game_manager):
        self.game = game_manager
        self.hidden = False
        self.pilot_frame_group = []

    def update_frame_quantity(self):
        pilot_quantity = len(self.game.pilots)
        pilot_frame_quantity = len(self.pilot_frame_group)
        # if there are fewer frames than pilots add another pilot_frame
        if pilot_frame_quantity < pilot_quantity:
            pilot_frame = PilotFrame(pilot_frame_quantity, self.game.pilots)
            self.pilot_frame_group.append(pilot_frame)
        # if there are more frames than pilots delete the last pilot_frame from the list
        elif pilot_frame_quantity > pilot_quantity:
            del(self.pilot_frame_group[-1])
            
    def update_pilot_frames(self):
        self.update_frame_quantity()
        for pilot_frame in self.pilot_frame_group:
            pilot_frame.update_pilot_frame()
    
    def draw_pilot_frames(self):
        for pilot_frame in self.pilot_frame_group:
            pilot_frame.draw_pilot_frame()


class PilotFrame:
    def __init__(self, index, pilot_list):
        self.index = index
        self.pilot_list = pilot_list

        # try to load the info for the pilot based on position in list
        try:
            self.pilot = self.pilot_list[self.index]
            self.name = self.pilot.name
        except(Exception, ):
            self.pilot = None
            self.name = "default"

        self.width = screen_width*0.2
        self.height = screen_height*0.2
        self.pos_x = screen_width*0.1
        self.pos_y = self.height*(self.index + 1)

        # load backing image
        self.back_image = pygame.image.load("graphics/menu/menu_back.png").convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (self.width, self.height))
        self.back_rect = self.back_image.get_rect(center=(self.pos_x, self.pos_y))
        # load text image
        self.text_image = text_font.render(self.name , False, (0, 0, 0))
        self.text_rect = self.text_image.get_rect(center=(self.pos_x, self.pos_y))

    def update_pilot_frame(self):
        # try to load the info for the pilot based on position in list
        # I'm sure there's a better way to get the position of an object in the sprite group, but this works for now
        list_position = -1
        for pilot in self.pilot_list:
            list_position += 1
            if list_position == self.index:
                self.pilot = pilot

        # self.pilot = self.pilot_list[self.index]
        self.name = self.pilot.name
        # except(Exception,):
        #     self.pilot = None
        #     self.name = "default"
        # update image and rect for text
        self.text_image = text_font.render(self.name, False, (0, 0, 0))
        self.text_rect = self.text_image.get_rect(center=(self.pos_x, self.pos_y))

    def draw_pilot_frame(self):
        if self.pilot is not None:
            # draw the back
            screen.blit(self.back_image, self.back_rect)
            # draw text name
            screen.blit(self.text_image, self.text_rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, button_type, pos_x=0, pos_y=0, width=screen_width*0.1, height=screen_width*0.1):
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
            self.frame_1 = pygame.transform.scale(self.frame_1,(self.width,self.height))

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

    def click_button(self):
        # reset cooldown
        self.cooldown = self.cooldown_max
        print("You clicked a button")
    # def check_active(self):
    #     # determine if active
    #     if self.button_type == "dashboard_map":
    #         if mode == "cockpit":
    #             self.active = True
    #         else:
    #             self.active = False
    #
    #     elif self.button_type == "swap_button":
    #         if mode != "inventory":
    #             self.active = False
    #         elif selected.inventory_slot > -1 and selected.pilot_slot > -1 and selected.loadout_slot > -1:
    #             self.active = True
    #             if group.inventory[selected.inventory_slot].function != selected.pilot.battlesuit.loadout[
    #                 selected.loadout_slot].function:
    #                 self.match = False
    #             else:
    #                 self.match = True
    #         else:
    #             self.active = False
    #
    #     elif self.button_type == "dispatch_button":
    #         if mode == "pilot_select" and selected.pilot_slot > 0 and selected.pilot.on_mission == False:
    #             self.active = True
    #         else:
    #             self.active = False
    #
    #     elif self.button_type == "continue_button":
    #         # make the continue button active if at least one Pilot is dispatching
    #         if mode == "pilot_select":
    #             self.active = False
    #             for pilot in group.pilot_roster:
    #                 if pilot.dispatching: self.active = True
    #
    #         # make the continue button active if there are scenes in queue and game is not awaiting a choice
    #         elif mode == "dialogue":
    #             if len(scene.scene_queue) > 0 and dialogue.choices_available == False: self.active = True
    #
    #         # always hide continue button on world map
    #         elif mode == "map":
    #             self.active = False
    #
    #         # always hide continue button during combat
    #         elif mode == "combat":
    #             self.active = False
    #
    #         # make the continue button visible if active and hidden otherwise
    #         if self.active == True:
    #             self.animation_index = 1
    #         else:
    #             self.animation_index = 0
    #
    #     elif self.button_type == "x_button":
    #         pass
    #
    #     else:
    #         if debug_mode:
    #             print("Error: unrecognized button type when checking if active", self.button_type)
    #         else:
    #             pass

    def update(self):
        # reduce cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
        # update image based on status
        self.update_image()
        # mouse inputs
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if self.rect.collidepoint(event.pos) and self.active == True and self.cooldown == 0:
        #
        #         # reset cooldown
        #         self.cooldown = self.cooldown_max
        #
        #         # close ui window
        #         if self.button_type == "x_button" and mode != "cockpit":
        #             mode = "cockpit"
        #
        #         # show world map
        #         elif mode == "cockpit" and self.button_type == "dashboard_map":
        #             mode = "map"
        #
        #         # swap loadout and inventory items
        #         elif self.button_type == "swap_button" and self.match == True:
        #             # swap items
        #             new_loadout_item = group.inventory[selected.inventory_slot]
        #             new_inventory_item = selected.pilot.battlesuit.loadout[selected.loadout_slot]
        #             selected.pilot.battlesuit.loadout[selected.loadout_slot] = new_loadout_item
        #             group.inventory[selected.inventory_slot] = new_inventory_item
        #             # reset which items are currently selected
        #             selected.loadout_slot = -1
        #             selected.inventory_slot = -1
        #
        #         # assign Pilot to mission
        #         elif self.button_type == "dispatch_button":
        #             if selected.pilot.dispatching == False: selected.pilot.dispatching = True
        #             else: selected.pilot.dispatching = False
        #
        #         # load the departing messages and return to dialogue screen. This should probably be a method like overlay.continue().
        #         elif self.button_type == "continue_button" and self.active == True and mode == "pilot_select":
        #             scene.scene_queue.clear()
        #             mode = "dialogue"
        #             for pilot in group.pilot_roster:
        #                 if pilot.dispatching:
        #                     pilot.dispatching = False
        #                     pilot.on_mission = True
        #                 if pilot.on_mission:
        #                     scene.scene_queue.append(f"{pilot.name} departing")
        #
        #             # conclude npcs with nighthawk and making sure she speaks last
        #             if len(scene.scene_queue) > 1 and scene.scene_queue[0] == "Nighthawk departing":
        #                 scene.scene_queue.append("Nighthawk departing")
        #                 scene.scene_queue.remove("Nighthawk departing")
        #
        #             scene.scene_queue.append("combat")
        #
        #             if debug_mode == True: print(scene.scene_queue)
        #                 # mission.mission_setup(selected.active_mission_number)
        #
        #         # advance to next scene if queue is not empty
        #         elif self.button_type == "continue_button" and self.active == True and mode == "dialogue" and dialogue.choices_available == False:
        #             try:
        #                 if debug_mode == True:
        #                     print(" ")
        #                     print(scene.scene_queue)
        #                     print("removing scene: ", scene.scene_queue[0])
        #                     print("advancing to scene:", scene.scene_queue[1])
        #                 dialogue.advance_scene(-1)
        #                 if debug_mode == True:
        #                     print("current scene is now:", scene.scene_queue[0])
        #                     print("next scene in queue:", scene.scene_queue[1])
        #                     print(scene.scene_queue)
        #                     print(" ")
        #             except:
        #                 if debug_mode == True: print("Error: no scenes in queue to remove")
        #                 else: pass
        #
        #         # if none of the above button is not activated
        #         else: self.active = False
        #
        # # update image
        # if self.active == False: self.animation_index = 0
        # else: self.animation_index = 1
        # if self.type == "swap_button" and self.active == True:
        #     if self.match == False: self.animation_index = 2
        # self.image = self.frames[self.animation_index]
        # self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        