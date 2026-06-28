"""This module contains the LeaderboardScreen class."""
import pygame

from enums import GameState
from resource_helper import resource_path
from ui_helper import draw_button, draw_text_with_shadow, draw_title, draw_button_text
from sound import Sound


class LeaderboardScreen:

    """Displays the leaderboard screen and handles its navigation."""

    def __init__(self, game, sound: Sound):
        """Initialize leaderboard screen.

        :param game: main game controller object
        """

        # reference to main driver
        self.game = game

        self.sound = sound

        # flag to check if we arrived here from game over or from beginning of session
        self.from_gameover = False

        # background
        self.background = pygame.image.load(resource_path("assets/img/background.png"))
        # Art asset created by Jonathan Hungate using Aseprite
        self.background = pygame.transform.smoothscale(
            self.background, (600, 750))

        # fonts
        self.title_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 50)
        self.mode_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)
        self.score_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 15)
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)

        # navigation buttons

        self.back_button_rect = pygame.Rect(80, 620, 200, 60)
        self.main_button_rect = pygame.Rect(320, 620, 200, 60)
        self.restart_button_rect = pygame.Rect(80, 620, 200, 60)

        # leaderboard box
        self.leaderboard_rect = pygame.Rect(100, 250, 400, 360)

    def draw(self, screen):
        """Render leaderboard screen.

        :param screen: pygame display surface
        """
        # background
        screen.blit(self.background, (0, 0))

        # Title
        draw_title(
            screen, "Leaderboard", self.title_font, (300, 150))

        # leaderboard box overlay
        box_surface = pygame.Surface(
            (self.leaderboard_rect.width,
             self.leaderboard_rect.height),
            pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))
        screen.blit(box_surface, self.leaderboard_rect.topleft)

        soft_colors = [
            (220, 170, 200), (220, 190, 170), (220, 220, 170),
            (170, 220, 200), (170, 220, 220), (170, 190, 220), (190, 170, 220)
        ]

        # display current game mode
        mode_text = f"{
            self.game.selected_operation.name}-{
            self.game.selected_difficulty.name}"

        draw_title(screen, mode_text, self.mode_font, (320, 220), soft_colors, 24)

        # score retrieval and display
        all_score = self.game.leaderboard.get_scores(
            self.game.selected_difficulty, self.game.selected_operation)
        display_scores = all_score[:5] if all_score else []

        score_position = 280

        if not display_scores:
            empty_text = self.score_font.render("No Score Yet", True, "white")
            screen.blit(empty_text, (100, score_position))
        else:
            for i, entry in enumerate(display_scores):
                name = entry['name']
                score = entry['score']

                # truncate long names
                display_name = (name[:10] + '..') if len(name) > 10 else name
                text = f"{i + 1}. {display_name} {score}"
                score_text = self.score_font.render(text, True, "white")
                screen.blit(score_text, (180, score_position))
                score_position += 50

        if self.from_gameover:
            active_buttons = [
                (self.restart_button_rect, "Restart", (190, 170, 220)),
                (self.main_button_rect, "Home", (220, 190, 170))
            ]
        else:
            active_buttons = [
                (self.back_button_rect, "Back", (220, 170, 200)),
                (self.main_button_rect, "Main", (220, 190, 170))
            ]

        for rect, text, color in active_buttons:
            draw_button_text(screen, text, rect, self.button_font, normal_color=color)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.from_gameover and self.restart_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.from_gameover = False
                self.game.state = GameState.CONFIRM

            # Check Main/Home
            elif self.main_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.from_gameover = False
                self.game.state = GameState.MAIN

            # Check Back (only if NOT from gameover)
            elif not self.from_gameover and self.back_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.state = GameState.CONFIRM


