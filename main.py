"""This module contains the MainMenu class and game loop."""
import sys

import pygame

from confirm import ConfirmationScreen
from credits import CreditsScreen
from difficulty import DifficultyScreen
from enums import GameState
from game import GameScreen
from gameover import GameOverScreen
from leaderboard import Leaderboard
from leaderboard_ui import LeaderboardScreen
from operation import OperationScreen
from resource_helper import resource_path
from settings import SettingsScreen
from sound import Sound
from ui_helper import draw_title, draw_button_text


class MainMenu:
    """Controls the main menu, game states, and overall game loop."""

    def __init__(self):
        """Initializes the main menu and all game screens."""
        pygame.init()

        # Set the Window's title
        pygame.display.set_caption("Mathmobile")
        # Set Window icon
        pygame.display.set_icon(pygame.image.load(resource_path("assets/img/icon.ico")))
        # Art asset created by Jonathan Hungate using Aseprite

        # screen configuration
        self.screen = pygame.display.set_mode((600, 750))

        # background picture
        self.background = pygame.image.load(resource_path("assets/img/background.png"))
        # Art asset created by Jonathan Hungate using Aseprite

        self.background = pygame.transform.smoothscale(
            self.background, (600, 750))

        # fonts
        self.title_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 50)
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 25)

        # main menu button locations
        self.start_button_rect = pygame.Rect(200, 280, 200, 60)
        self.setting_button_rect = pygame.Rect(200, 380, 200, 60)
        self.credits_button_rect = pygame.Rect(200, 480, 200, 60)
        self.exit_button_rect = pygame.Rect(200, 580, 200, 60)

        # game session variables
        self.selected_operation = None
        self.selected_difficulty = None
        self.state = GameState.MAIN

        self.prev_state = None
        self.sound = Sound()

        # initialize all screen objects
        self.operation_screen = OperationScreen(self, self.sound)
        self.difficulty_screen = DifficultyScreen(self, self.sound)
        self.credits_screen = CreditsScreen(self, self.sound)
        self.game_screen = GameScreen(self, self.sound)
        self.confirmation_screen = ConfirmationScreen(self, self.sound)
        self.leaderboard_screen = LeaderboardScreen(self, self.sound)
        self.game_over_screen = GameOverScreen(self, self.sound)
        self.leaderboard = Leaderboard()
        self.setting_screen = SettingsScreen(self, self.sound)

        self.clock = pygame.time.Clock()

    def draw(self):
        """Draws the main menu screen."""
        # title
        self.screen.blit(self.background, (0, 0))
        # draw_text_with_shadow(self.screen, "Mathmobile",
        # self.title_font, (300, 150))

        # text = "Mathmobile"

        draw_title(self.screen, "Mathmobile",
                   self.title_font, (310, 130), letter_width=42)

        # show buttons

        draw_button_text(self.screen, "Start", self.start_button_rect, self.button_font, (153, 255, 204))

        draw_button_text(self.screen, "Setting", self.setting_button_rect, self.button_font, (153, 204, 255))

        draw_button_text(self.screen, "Credits", self.credits_button_rect, self.button_font, (153, 255, 255))

        draw_button_text(self.screen, "Exit", self.exit_button_rect, self.button_font, (153, 204, 255))

    def run_game(self):
        """Main game loop that handles events and rendering."""
        # primary game loop
        while True:
            # handle event polling
            for event in pygame.event.get():
                # close game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # route input based on current state

                if self.state == GameState.MAIN:
                    self.main_events_handler(event)

                elif self.state == GameState.SETTINGS:
                    self.setting_screen.event_handler(event)

                elif self.state == GameState.CREDITS:
                    self.credits_screen.event_handler(event)
                elif self.state == GameState.OPERATION:
                    self.operation_screen.event_handler(event)
                elif self.state == GameState.DIFFICULTY:
                    self.difficulty_screen.event_handler(event)
                elif self.state == GameState.CONFIRM:
                    self.confirmation_screen.event_handler(event)
                elif self.state == GameState.GAME:
                    self.game_screen.event_handler(event)
                elif self.state == GameState.LEADERBOARD:
                    self.leaderboard_screen.event_handler(event)
                elif self.state == GameState.GAME_OVER:
                    self.game_over_screen.event_handler(event)

            if self.state != self.prev_state:
                if self.state == GameState.MAIN:
                    self.sound.play_music_menu()
                self.prev_state = self.state

            # draw screen based on current state
            if self.state == GameState.MAIN:
                self.draw()

            elif self.state == GameState.SETTINGS:
                self.setting_screen.draw(self.screen)

            elif self.state == GameState.CREDITS:
                self.credits_screen.draw(self.screen)
            elif self.state == GameState.OPERATION:
                self.operation_screen.draw(self.screen)
            elif self.state == GameState.DIFFICULTY:
                self.difficulty_screen.draw(self.screen)
            elif self.state == GameState.CONFIRM:
                self.game_screen.draw(self.screen)
                self.confirmation_screen.draw(self.screen)
            elif self.state == GameState.GAME:
                self.game_screen.draw(self.screen)
            elif self.state == GameState.LEADERBOARD:
                self.leaderboard_screen.draw(self.screen)
            elif self.state == GameState.GAME_OVER:
                self.game_over_screen.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

    def main_events_handler(self, event):
        """Handles input events for the main menu.

        :param event: pygame event object
        """
        # handle menu navigation
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.state = GameState.OPERATION

            elif self.setting_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.state = GameState.SETTINGS

            elif self.credits_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.credits_screen.scroll_y = 750
                self.state = GameState.CREDITS
            elif self.exit_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    game = MainMenu()
    game.run_game()
