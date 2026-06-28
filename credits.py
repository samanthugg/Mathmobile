"""This module contains the CreditsScreen class."""
import pygame

from resource_helper import resource_path
from ui_helper import draw_button_text
from enums import GameState
from sound import Sound
from ui_helper import draw_title


class CreditsScreen:
    """Displays scrolling credits and handles navigation."""

    def __init__(self, game, sound: Sound):
        """Initializes the credits screen.

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
        self.credits_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 15)
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)

        # main menu button
        self.main_menu_rect = pygame.Rect(200, 650, 200, 60)

        # rolling credit
        self.scroll_y = 750
        self.scroll_speed = 0.9
        self.line_spacing = 55

        # credit box
        self.box_rect = pygame.Rect(100, 180, 400, 450)

        # credit text
        self.credits_lines = [
            "Jonathan Hungate",
            "Team Lead / Art",
            "keeps us on track and ",
            "play referee when needed",
            "",
            "Dennis Parraga",
            "Developer",
            "writes the code and",
            "keep design from going",
            "off track",
            "",
            "Junli Ma",
            "UI Designer",
            "Constantly at war ",
            "with the UI",
            "",
            "Naomi Stolo",
            "Backend",
            "handles the logic ",
            "with big brain energy",
            "",
            "Samantha Green",
            "QA/Tester",
            "finds all the bugs that",
            "we pretend don't exist"
        ]

        self.credit_font = pygame.font.Font(None, 16)
        self.credit_text = self.credit_font.render(
            "Art: Jonathan Hungate", True, "white")

    # mouse input

    def event_handler(self, event):
        """Handles mouse input for the credits screen.

        :param event: pygame event object
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.main_menu_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.state = GameState.MAIN

    def draw(self, screen):
        """Draws the credits screen and scroll animation.

        :param screen: pygame display surface
        """
        screen.blit(self.background, (0, 0))

        # title

        main_colors = [
            (255, 153, 204), (255, 204, 153), (255, 255, 153),
            (153, 255, 204), (153, 255, 255), (153, 204, 255), (204, 153, 255)
        ]

        draw_title(screen, "Credits", self.title_font,
                   (310, 120), main_colors, letter_width=43)

        # credit box
        box_surface = pygame.Surface(
            (self.box_rect.width, self.box_rect.height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))
        screen.blit(box_surface, self.box_rect.topleft)

        # credit boarder
        pygame.draw.rect(screen, "white", self.box_rect, 2, border_radius=10)

        # rolling credit
        self.scroll_y -= self.scroll_speed

        screen.set_clip(self.box_rect)
        for index, line in enumerate(self.credits_lines):
            text = self.credits_font.render(line, True, "white")
            y = self.scroll_y + index * self.line_spacing
            text_rect = text.get_rect(center=(300, int(y)))
            screen.blit(text, text_rect)

        # reset credit
        last_y = self.scroll_y + len(self.credits_lines) * self.line_spacing
        if last_y < self.box_rect.top:
            self.scroll_y = self.box_rect.bottom

        screen.set_clip(None)

        # button
        draw_button_text(screen, "Main", self.main_menu_rect,
                         self.game.button_font, (255, 153, 204))

        rect = self.credit_text.get_rect(bottomright=(590, 740))
        screen.blit(self.credit_text, rect)
