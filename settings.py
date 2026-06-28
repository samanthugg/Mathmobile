"""This module contains the SettingsScreen class.

    Used to mute or unmute sound effects and background music in the game.
    Can also change the language of the game"""
import pygame

from enums import GameState
from resource_helper import resource_path
from sound import Sound
from ui_helper import draw_button, draw_title, draw_button_text, draw_corners, draw_text_with_shadow


class SettingsScreen:
    """Displays setting options and handles sound and language changes."""

    def __init__(self, game, sound: Sound):
        """Initializes the settings screen.

        :param game: main game controller object
        """
        # reference to main driver
        self.game = game
        self.sound = sound

        # background
        self.background = pygame.image.load(resource_path("assets/img/background.png"))
        self.background = pygame.transform.smoothscale(
            self.background, (600, 750))

        # font
        self.title_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 46)
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)

        # main menu button
        self.main_menu_rect = pygame.Rect(200, 650, 200, 60)

        # settings box area

        self.box_rect = pygame.Rect(100, 180, 400, 400)

        self.button_width = 180
        self.label_width = 180

        self.x_align_left = self.box_rect.left + 25
        self.x_align_right = self.box_rect.centerx + 50

        self.y_placement_sound = self.box_rect.top + 90
        self.y_placement_music = self.box_rect.top + 240

        # labels and buttons placement
        self.rect_label_music = pygame.Rect(
            self.x_align_left, self.y_placement_sound, self.button_width, 60)
        self.rect_button_music = pygame.Rect(
            self.x_align_right, self.y_placement_sound, 60, 60)

        self.rect_label_sound = pygame.Rect(
            self.x_align_left, self.y_placement_music, self.button_width, 60)
        self.rect_button_sound = pygame.Rect(
            self.x_align_right, self.y_placement_music, 60, 60)

        # state of music and sound
        self.state_music = True
        self.state_sound = True
        self.display_music = ""
        self.display_sound = ""

    def event_handler(self, event):
        """Handles mouse input for the credits screen.

        :param event: pygame event object
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.main_menu_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.state = GameState.MAIN
            if self.rect_button_music.collidepoint(event.pos):
                if self.state_music:
                    self.display_music = "X"
                    self.sound.mute_music()
                    self.state_music = False
                else:
                    self.display_music = ""
                    self.sound.unmute_music()
                    self.state_music = True
                self.sound.play_sound_button()
            if self.rect_button_sound.collidepoint(event.pos):
                if self.state_sound:
                    self.display_sound = "X"
                    self.sound.mute_sound()
                    self.state_sound = False
                else:
                    self.display_sound = ""
                    self.sound.unmute_sound()
                    self.state_sound = True
                self.sound.play_sound_button()

    def draw(self, screen):
        """Draws the credits screen and scroll animation.

        :param screen: pygame display surface
        """
        screen.blit(self.background, (0, 0))

        # settings box background and border
        box_surface = pygame.Surface(
            (self.box_rect.width, self.box_rect.height), pygame.SRCALPHA
        )
        box_surface.fill((0, 0, 0, 180))
        screen.blit(box_surface, self.box_rect.topleft)

        pygame.draw.rect(screen, "white", self.box_rect, 2, border_radius=10)

        main_colors = [
            (255, 153, 204), (255, 204, 153), (255, 255, 153),
            (153, 255, 204), (153, 255, 255), (153, 204, 255), (204, 153, 255)
        ]

        # title
        draw_title(screen, "Settings", self.title_font, (310, 120), main_colors, letter_width=43)

        # return to main button
        draw_button_text(screen, "Main", self.main_menu_rect,
                         self.game.button_font, (153, 255, 204))

        mouse = pygame.mouse.get_pos()
        # Draw labels and buttons
        draw_text_with_shadow(
            screen,
            "Music",
            self.button_font,
            self.rect_label_music.center,
            (255, 204, 153)
        )

        draw_button(screen, self.rect_button_music, self.display_music, self.button_font)
        if self.rect_button_music.collidepoint(mouse):
            draw_corners(screen, self.rect_button_music, offset=4, size=6, width=2, animated=True)

        draw_text_with_shadow(
            screen,
            "Sounds",
            self.button_font,
            self.rect_label_sound.center,
            (255, 255, 153)
        )
        draw_button(screen, self.rect_button_sound, self.display_sound, self.button_font)
        if self.rect_button_sound.collidepoint(mouse):
            draw_corners(screen, self.rect_button_sound, offset=4, size=6, width=2, animated=True)
