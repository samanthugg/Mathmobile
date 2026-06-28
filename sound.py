"""Allows the use of sound effects and background music. 

    Sounds are created and their volumes are set on class initiation. 
    All background music is looped."""

import pygame

from resource_helper import resource_path


class Sound:
    """Sets the sound effects and background music for the game"""
    def __init__(self):
        pygame.mixer.init()

        # prepare sounds
        # set_volume() - think of percentage (0.70 = 70% sound). Can't go over 100%.
        self._sound_tire_left = pygame.mixer.Sound(resource_path("assets/sound_effects/sound_tire_left.wav"))
        self._sound_tire_right = pygame.mixer.Sound(resource_path("assets/sound_effects/sound_tire_right.wav"))
        self._sound_button = pygame.mixer.Sound(resource_path("assets/sound_effects/sound_button_1.mp3"))
        self._sound_correct = pygame.mixer.Sound(resource_path("assets/sound_effects/sound_correct.mp3"))
        self._sound_incorrect = pygame.mixer.Sound(resource_path("assets/sound_effects/sound_incorrect.wav"))
        self._sound_countdown = pygame.mixer.Sound(resource_path("assets/sound_effects/sound_countdown.wav"))
        self._game_music = pygame.mixer.music

        self._sound_tire_left.set_volume(1)
        self._sound_tire_right.set_volume(1)
        self._sound_button.set_volume(1)
        self._sound_correct.set_volume(0.3)
        self._sound_incorrect.set_volume(0.3)
        self._sound_countdown.set_volume(0.3)

        self._muted_music = False
        self._muted_sound = False

    def play_sound_tire_left(self):
        """Plays the sound effect when turning the car left"""
        self._sound_tire_left.play()

    def play_sound_tire_right(self):
        """Plays the sound effect when turning the car right"""
        self._sound_tire_right.play()

    def play_sound_button(self):
        """Plays the sound effect when pressing a button"""
        self._sound_button.play()

    def play_sound_correct(self):
        """Plays the sound effect when choosing a correct answer"""
        self._sound_correct.play()

    def play_sound_incorrect(self):
        """Plays the sound effect when choosing an incorrect answer"""
        self._sound_incorrect.play()

    def play_sound_countdown(self):
        """Plays the sound effect when the countdown starts"""
        self._sound_countdown.play()

    def play_music_menu(self):
        """Plays the background music for the menu on loop"""
        if not self._muted_music:
            self._game_music.load(resource_path("assets/music/music_menu.mp3"))
            self._game_music.set_volume(0.5)
            self._game_music.play(loops = -1)

    def play_music_gameplay(self):
        """Plays the background music for the gameplay on loop"""
        if not self._muted_music:
            self._game_music.load(resource_path("assets/music/music_game.wav"))
            self._game_music.set_volume(0.05)
            self._game_music.play(loops = -1)

    def mute_music(self):
        """Mutes the background music"""
        self._muted_music = True
        self._game_music.set_volume(0)

    def unmute_music(self):
        """Unmutes the background music on loop"""
        self._muted_music = False
        self._game_music.set_volume(0.5)

    def mute_sound(self):
        """Mutes the sound effects"""
        self._muted_sound = True
        self._sound_tire_left.set_volume(0)
        self._sound_tire_right.set_volume(0)
        self._sound_button.set_volume(0)
        self._sound_correct.set_volume(0)
        self._sound_incorrect.set_volume(0)
        self._sound_countdown.set_volume(0)

    def unmute_sound(self):
        """Unmutes the sound effects"""
        self._muted_sound = False
        self._sound_tire_left.set_volume(1)
        self._sound_tire_right.set_volume(1)
        self._sound_button.set_volume(1)
        self._sound_correct.set_volume(0.3)
        self._sound_incorrect.set_volume(0.3)
        self._sound_countdown.set_volume(0.3)

        self.play_sound_button()


# TESTING
if __name__ == "__main__":
    import sys
    pygame.init()
    sound = Sound()
    screen = pygame.display.set_mode((600, 750))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    sound.play_music_menu()
                if event.key == pygame.K_2:
                    sound.play_music_gameplay()
                if event.key == pygame.K_3:
                    sound.play_sound_tire_left()
                if event.key == pygame.K_4:
                    sound.play_sound_tire_right()
                if event.key == pygame.K_5:
                    sound.play_sound_button()
                if event.key == pygame.K_6:
                    sound.play_sound_correct()
                if event.key == pygame.K_7:
                    sound.play_sound_incorrect()
                if event.key == pygame.K_8:
                    sound.play_sound_countdown()
                if event.key == pygame.K_9:
                    sound.play_music_menu()
                    
                if event.key == pygame.K_q:
                    sound.mute_music()
                if event.key == pygame.K_w:
                    sound.mute_sound()
                if event.key == pygame.K_a:
                    sound.unmute_music()
                if event.key == pygame.K_s:
                    sound.unmute_sound()
