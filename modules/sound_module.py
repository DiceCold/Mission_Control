import random

import pygame


class SoundController:
    def __init__(self):
        self.current_music = None

        # load sound effect files
        directory = "sounds/effects/"

        # load thunder
        thunder_sound_1 = pygame.mixer.Sound(f"{directory}thunder_1.mp3")
        thunder_sound_1.set_volume(0.3)
        thunder_sound_2 = pygame.mixer.Sound(f"{directory}thunder_2.mp3")
        thunder_sound_2.set_volume(0.3)
        thunder_sound_3 = pygame.mixer.Sound(f"{directory}thunder_3.mp3")
        thunder_sound_3.set_volume(0.6)
        self.thunder_sounds = [thunder_sound_1, thunder_sound_2, thunder_sound_3]

        # load explosion
        explosion_sound_1 = pygame.mixer.Sound(f"{directory}explosion_bass_quick.mp3")
        explosion_sound_2 = pygame.mixer.Sound(f"{directory}explosion_quick.mp3")
        explosion_sound_3 = pygame.mixer.Sound(f"{directory}explosion_quick2.mp3")
        self.explosion_sounds = [explosion_sound_1, explosion_sound_2, explosion_sound_3]

        # load laser sounds
        laser_sound_1 = pygame.mixer.Sound(f"{directory}laser_charge_1.mp3")
        laser_sound_1.set_volume(0.5)
        laser_sound_2 = pygame.mixer.Sound(f"{directory}laser_charge_2.mp3")
        laser_sound_1.set_volume(0.5)
        laser_sound_3 = pygame.mixer.Sound(f"{directory}laser_charge_3.mp3")
        laser_sound_1.set_volume(0.5)
        self.laser_sounds = [laser_sound_1, laser_sound_2, laser_sound_3]

    def play_sound(self, sound_name):
        # determine list to pull random sound from \
        if sound_name == "thunder":
            sound_list = self.thunder_sounds
        elif sound_name == "explosion":
            sound_list = self.explosion_sounds
        elif sound_name == "laser":
            sound_list = self.laser_sounds
        else:
            # use thunder list as catchall
            sound_list = self.thunder_sounds
        # select and play random sound from the list
        sound = random.choice(sound_list)
        sound.play()

    def play_music(self, music_name):
        # load and play a song from the music file
        directory = "sounds/music/"
        pygame.mixer.music.load(f"{directory}{music_name}.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.current_music = music_name
