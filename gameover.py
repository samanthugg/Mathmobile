"""This module contains the GameOverScreen class."""
import pygame

from enums import GameState
from resource_helper import resource_path
from ui_helper import draw_button_text, draw_text_with_shadow, draw_title
from sound import Sound

class GameOverScreen:
    """Displays the game over screen and handles score submission."""
    def __init__(self, game, sound: Sound):
        """Initializes the game over screen.

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

        # fonts
        self.title_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 50)
        self.score_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)
        self.input_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 20)

        # button layout
        self.box_rect = pygame.Rect(100, 180, 400, 400)
        self.next_button_rect = pygame.Rect(200, 620, 200, 60)

        # input box setup
        self.player_name = ""
        self.input_box = pygame.Rect(160, 420, 300, 40)
        self.active = False
        self.color_active = pygame.Color("lightskyblue3")
        self.color_passive = pygame.Color("gray")
        self.color = self.color_passive

    def draw(self, screen):
        """Draws the game over screen.

        :param screen: pygame display surface
        """

        # background & overlay
        screen.blit(self.background, (0, 0))

        # dark transparent box
        box_surface = pygame.Surface(
            (self.box_rect.width, self.box_rect.height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))
        screen.blit(box_surface, self.box_rect.topleft)

        # text messages using shadow helper
        draw_title(screen, "You Did Great!",
                              self.title_font, (310, 120))

        draw_text_with_shadow(
            screen, "Your Score", self.score_font, (310, 220), (255, 204, 153) )

        # display actual session score
        score = self.game.game_screen.session.score if self.game.game_screen.session else 0
        score_text = self.score_font.render(
            f"{score} " + "pts", True, (255, 255, 255))
        screen.blit(score_text, score_text.get_rect(center=(300, 300)))

        draw_text_with_shadow(screen, " Enter your name\nto save your score",
                              self.score_font, (310, 380), (255, 255, 153))

        # input field rendering
        current_color = self.color_active if self.active else self.color_passive

        # dark background for the box so the name is readable
        pygame.draw.rect(screen, (30, 30, 30), self.input_box)

        # the border using our skyblue/gray variable
        pygame.draw.rect(screen, current_color, self.input_box, 3)

        # name
        input_name_surface = self.input_font.render(
            self.player_name, True, (255, 255, 255))
        screen.blit(
            input_name_surface,
            (self.input_box.x + 10,
             self.input_box.y + 10))

        # button
        draw_button_text(screen, "Next", self.next_button_rect,  self.button_font,  (153, 255, 204))

    def event_handler(self, event):
        """Handles mouse and keyboard input for the game over screen.

        :param event: pygame event object
        """

        # mouse input
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.sound.play_sound_button()
            self.active = self.input_box.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_passive

            if self.next_button_rect.collidepoint(event.pos):
                self.submit_score()

        # keyboard input
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN:
                self.submit_score()
            else:
                if len(self.player_name) < 10 and event.unicode.isprintable():
                    self.player_name += event.unicode

    def submit_score(self):
        """Saves the score if a name was entered, then moves to leaderboard."""
        # save and navigate
        if self.player_name.strip():

            self.game.entered_name = self.player_name

            session = self.game.game_screen.session
            score = session.score if session else 0

            self.game.leaderboard.insert_score(
                self.game.selected_difficulty,
                self.game.selected_operation,
                self.player_name,
                score
            )

        # Reset state and navigate
        self.game.leaderboard_screen.from_gameover = True
        self.player_name = ""
        self.active = False
        self.game.state = GameState.LEADERBOARD
