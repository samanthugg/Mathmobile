"""This module contains the ConfirmationScreen class."""

import pygame
from PIL import Image

from enums import GameState
from resource_helper import resource_path
from sound import Sound
from ui_helper import draw_text_with_shadow, draw_title, draw_button_text, draw_corners


class ConfirmationScreen:
    """Displays confirmation options and handles confirmation input."""

    def __init__(self, game, sound: Sound):
        """Initializes the confirmation screen UI, assets, and animation state.

        :param game: main game controller object
        :param sound: sound manager for playing effects and music
        """
        self.game = game
        self.sound = sound

        # fonts
        self.title_font = pygame.font.Font(
            resource_path('assets/font/PressStart2P-Regular.ttf'), 50)
        self.button_font = pygame.font.Font(
            resource_path('assets/font/PressStart2P-Regular.ttf'), 20)
        self.text_font = pygame.font.Font(
            resource_path('assets/font/PressStart2P-Regular.ttf'), 15)

        # icons
        self.home_icon = pygame.image.load(resource_path("assets/img/home.png"))
        self.lb_icon = pygame.image.load(resource_path("assets/img/lb.png"))

        self.tutorial_rect = pygame.Rect(125, 210, 350, 250)

        # buttons
        self.button_1 = pygame.Rect(125, 460, 350, 50)
        self.button_2 = pygame.Rect(125, 520, 117, 50)
        self.button_3 = pygame.Rect(242, 520, 117, 50)
        self.button_4 = pygame.Rect(359, 520, 117, 50)

        # load gif frames, convert to pygame surfaces, and scale them smaller for tutorial display
        frames = []
        gif = Image.open(resource_path('assets/img/control.gif'))
        # Art asset created by Jonathan Hungate using Aseprite

        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.convert("RGBA")
            py_frame = pygame.image.frombytes(frame.tobytes(), frame.size, "RGBA")

            scale_width = int(self.tutorial_rect.width * 0.7)
            scale_height = int(self.tutorial_rect.height * 0.7)

            py_frame = pygame.transform.scale(
                py_frame,
                (scale_width, scale_height)
            )

            frames.append(py_frame)

        # initialize gif animation state (frame index, timing, speed)
        self.frames = frames
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 180

        self.mode = "start"

    def draw(self, screen):
        """Renders the confirmation screen, including overlay, tutorial animation,
        title, buttons, and optional warning message.

        :param screen: pygame display surface
        """
        # dark overlay
        overlay = pygame.Surface((600, 750), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (30, 30, 30),
                         self.tutorial_rect, border_radius=12)
        pygame.draw.rect(
            screen,
            "white",
            self.tutorial_rect,
            2,
            border_radius=12)

        # update gif animation timing
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update = now

        # center gif inside tutorial box and shift it up slightly
        frame_rect = self.frames[self.frame_index].get_rect(center=self.tutorial_rect.center)
        frame_rect.y -= 30  # shift up
        if self.mode == "start":
            screen.blit(self.frames[self.frame_index], frame_rect)

            # draw short movement instruction below gif
            draw_text_with_shadow(
                screen,
                "Use \u2190 and \u2192 to move",
                self.text_font,
                (self.tutorial_rect.centerx, self.tutorial_rect.bottom - 25)
            )

        # Setup buttons
        if self.mode == "start":
            title_text = "Ready?"
            active_buttons = [
                (self.button_1, "LET'S GOOOO!", (190, 170, 220), False),
                (self.button_2, "\u2190", (220, 170, 200), False),
                (self.button_3, self.home_icon, (220, 190, 170), True),
                (self.button_4, self.lb_icon, (220, 220, 170), True)
            ]
        else:  # Warning Mode
            title_text = "Main Menu?"
            active_buttons = [
                (self.button_2, "Yes", (220, 170, 200), False),
                (self.button_4, "No", (220, 220, 170), False)
            ]

        soft_colors = [
            (220, 170, 200), (220, 190, 170), (220, 220, 170),
            (170, 220, 200), (170, 220, 220), (170, 190, 220), (190, 170, 220)
        ]

        draw_title(screen, title_text, self.title_font,
                   (310, 150), soft_colors)

        if self.mode == "warning":
            draw_text_with_shadow(
                screen, "ALL PROGRESS\n\nWILL BE LOST", self.text_font, (300, 300))

        # loops
        mouse_pos = pygame.mouse.get_pos()
        for rect, content, color, is_icon in active_buttons:
            hover = rect.collidepoint(mouse_pos)

            if is_icon:
                icon_scaled = pygame.transform.scale(content, (32, 32))
                icon_rect = icon_scaled.get_rect(center=rect.center)
                screen.blit(icon_scaled, icon_rect)
                if hover:
                    hover_rect = icon_rect.inflate(14, 14)
                    draw_corners(
                        screen,
                        hover_rect,
                        offset=0,
                        size=6,
                        width=2,
                        animated=True)
            else:
                draw_button_text(
                    screen,
                    content,
                    rect,
                    self.button_font,
                    normal_color=color)

    def event_handler(self, event):
        """Handles mouse input for the confirmation screen.

        :param event: pygame event object
        """

        # mouse input
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # start screen
            if self.mode == "start":
                if self.button_1.collidepoint(event.pos):
                    self.sound.play_sound_button()
                    self.game.game_screen.start_session()
                    self.game.game_screen.countdown = pygame.time.get_ticks()
                    self.game.state = GameState.GAME

                elif self.button_2.collidepoint(event.pos):
                    self.sound.play_sound_button()
                    self.game.state = GameState.DIFFICULTY

                # back to main menu
                elif self.button_3.collidepoint(event.pos):
                    self.sound.play_sound_button()
                    self.game.state = GameState.MAIN

                elif self.button_4.collidepoint(event.pos):
                    self.sound.play_sound_button()
                    self.game.state = GameState.LEADERBOARD

            # warning
            elif self.mode == "warning":
                if self.button_2.collidepoint(event.pos):
                    self.mode = "start"
                    self.game.state = GameState.MAIN

                elif self.button_4.collidepoint(event.pos):
                    self.mode = "start"
                    self.game.state = GameState.GAME


def draw_icon(screen, x, y, pixels, color=(255, 255, 255)):
    """Draws a pixel style icon using a grid of values.

   :param screen: pygame display surface
   :param x: x position of the icon
   :param y: y position of the icon
   :param pixels: 2D array representing pixel layout
   :param color: RGB color of the icon
   """

    scale = 2
    for row_i, row in enumerate(pixels):
        for col_i, val in enumerate(row):
            if val == "1":
                pygame.draw.rect(
                    screen,
                    color,
                    (x + col_i * scale, y + row_i * scale, scale, scale)
                )
