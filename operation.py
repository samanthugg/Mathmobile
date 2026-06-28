"""This module contains the OperationScreen class."""
import pygame

from enums import *
from resource_helper import resource_path
from sound import Sound
from ui_helper import draw_title, draw_button_text


class OperationScreen:
    """Displays operation options and handles operation selection."""

    def __init__(self, game, sound: Sound):
        """Initializes the operation selection screen.

        :param game: main game controller object
        """
        # reference to main driver
        self.game = game

        self.sound = sound

        # background image
        self.background = pygame.image.load(resource_path("assets/img/background.png"))
        # Art asset created by Jonathan Hungate using Aseprite
        self.background = pygame.transform.smoothscale(
            self.background, (600, 750))

        self.title_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 46)
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)

        # buttons
        self.add_button_rect = pygame.Rect(120, 280, 350, 50)
        self.minus_button_rect = pygame.Rect(120, 360, 350, 50)
        self.multi_button_rect = pygame.Rect(120, 440, 350, 50)
        self.divide_button_rect = pygame.Rect(120, 520, 350, 50)
        self.main_menu_rect = pygame.Rect(200, 620, 200, 60)

    def event_handler(self, event):
        """Handles mouse input for the operation screen.

        :param event: pygame event object
        """
        # mouse input
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.add_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.selected_operation = Operation.ADD
                self.game.state = GameState.DIFFICULTY

            elif self.minus_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.selected_operation = Operation.SUBTRACT
                self.game.state = GameState.DIFFICULTY

            elif self.multi_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.selected_operation = Operation.MULTIPLY
                self.game.state = GameState.DIFFICULTY

            elif self.divide_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.selected_operation = Operation.DIVIDE
                self.game.state = GameState.DIFFICULTY

            elif self.main_menu_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.state = GameState.MAIN

    def draw(self, screen):
        """Draws the operation selection screen.

        :param screen: pygame display surface
        """

        # background
        screen.blit(self.background, (0, 0))
        # title

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
        draw_title(screen, "Operation", self.title_font,
                   (310, 180), main_colors, letter_width=43)

        # buttons from helper
        draw_button_text(
            screen,
            "Addition",
            self.add_button_rect,
            self.game.button_font,
            (255, 255, 153))

        draw_button_text(
            screen,
            "Subtraction",
            self.minus_button_rect,
            self.game.button_font,
            (153, 255, 204))

        draw_button_text(
            screen,
            "Multiplication",
            self.multi_button_rect,
            self.game.button_font,
            (153, 255, 255))

        draw_button_text(
            screen,
            "Division",
            self.divide_button_rect,
            self.game.button_font,
            (153, 204, 255))

        draw_button_text(
            screen,
            "Back",
            self.main_menu_rect,
            self.game.button_font,
            (204, 153, 255))
