"""This module contains the DifficultyScreen class."""
import pygame

from enums import *
from resource_helper import resource_path
from sound import Sound
from ui_helper import draw_title, draw_button_text


class DifficultyScreen:
    """Displays difficulty options and handles difficulty selection."""

    def __init__(self, game, sound: Sound):
        """Initializes the difficulty screen.

        :param game: main game controller object
        """
        # reference to main driver
        self.game = game
        self.sound = sound

        # background
        self.background = pygame.image.load(resource_path("assets/img/background.png"))
        # Art asset created by Jonathan Hungate using Aseprite
        self.background = pygame.transform.smoothscale(
            self.background, (600, 750))

        # font
        self.title_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 46)
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 25)

        # button location
        self.easy_button_rect = pygame.Rect(120, 280, 350, 50)
        self.medium_button_rect = pygame.Rect(120, 360, 350, 50)
        self.hard_button_rect = pygame.Rect(120, 440, 350, 50)
        self.back_button_rect = pygame.Rect(70, 620, 200, 60)
        self.main_menu_rect = pygame.Rect(300, 620, 200, 60)

    def draw(self, screen):
        """Draws the difficulty selection screen.

        :param screen: pygame display surface
        """

        # background
        screen.blit(self.background, (0, 0))

        # title with shadow

        soft_colors = [
            (220, 170, 200), (220, 190, 170), (220, 220, 170),
            (170, 220, 200), (170, 220, 220), (170, 190, 220), (190, 170, 220)
        ]
        main_colors = [
            (255, 153, 204), (255, 204, 153), (255, 255, 153),
            (153, 255, 204), (153, 255, 255), (153, 204, 255), (204, 153, 255)
        ]

        draw_title(screen, "Select", self.title_font,
                   (310, 120), soft_colors, letter_width=43)
        draw_title(screen, "Difficulty", self.title_font,
                   (310, 180), main_colors, letter_width=43)

        # buttons from helper
        draw_button_text(screen, "Easy", self.easy_button_rect,
                         self.button_font, (153, 255, 255))
        draw_button_text(
            screen,
            "Medium",
            self.medium_button_rect,
            self.button_font,
            (153,
             204,
             255))
        draw_button_text(screen, "Hard", self.hard_button_rect,
                         self.button_font, (204, 153, 255))
        draw_button_text(screen, "Back", self.back_button_rect,
                         self.button_font, (255, 153, 204))
        draw_button_text(screen, "Main", self.main_menu_rect,
                         self.button_font, (255, 204, 153))

    def event_handler(self, event):
        """Handles mouse input for the difficulty screen.

        :param event: pygame event object
        """

        # mouse action
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # set difficulty and move to confirm screen
            if self.easy_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.selected_difficulty = DifficultyLevel.EASY
                self.game.game_screen.countdown = pygame.time.get_ticks()
                self.game.state = GameState.CONFIRM

            elif self.medium_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.selected_difficulty = DifficultyLevel.MEDIUM
                self.game.game_screen.countdown = pygame.time.get_ticks()
                self.game.state = GameState.CONFIRM

            elif self.hard_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.selected_difficulty = DifficultyLevel.HARD
                self.game.game_screen.countdown = pygame.time.get_ticks()
                self.game.state = GameState.CONFIRM

            # go back to operation selection
            elif self.back_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.state = GameState.OPERATION

            # return to main menu
            elif self.main_menu_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.state = GameState.MAIN
