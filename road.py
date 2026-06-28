"""This module contains the class Road and its methods."""
import pygame

from resource_helper import resource_path
from ui_helper import draw_text_with_shadow


class Road:
    """Draws the road, score display, and question display."""

    def __init__(self):
        """Initializes the road layout, fonts, and score tracking."""
        # fonts
        self.score_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 8)
        self.question_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 25)

        self.heart = pygame.image.load(resource_path("assets/img/heart.png"))
        # Art asset created by Junli Ma using https://www.pixilart.com/
        self.heart = pygame.transform.scale(self.heart, (25,25))

        # score tracking
        self.highest_score = 0
        self.personal_score = 0

        # road layout & scrolling setup
        width = 580
        self.road_rect = pygame.Rect((600 - width) // 2, 80, width, 750)
        self.line = self.road_rect.y
        self.line_speed = 2

    def draw(self, screen, road_movement=False):
        """Draw the road and updates lanes

        :param screen: pygame display surface
        :param road_movement: boolean to indicate if the road is moved or not
        """
        # upper road sign (UI bar)
        # base green sign
        pygame.draw.rect(screen, (0, 100, 60),
                         (0, 0, 600, 80), border_radius=12)
        # white border
        pygame.draw.rect(screen, "white", (0, 0, 600, 80), 3, border_radius=12)
        # inner highlight
        pygame.draw.rect(screen, (0, 140, 80),
                         (14, 9, 572, 15), border_radius=8)

        # asphalt body
        pygame.draw.rect(screen, (130, 130, 130), self.road_rect)

        # outer lane boundaries
        # left solid white line
        pygame.draw.line(
            screen,
            "white",
            (self.road_rect.left + 20,
             self.road_rect.y),
            (self.road_rect.left + 20,
             self.road_rect.bottom),
            2)

        # right white line
        pygame.draw.line(
            screen,
            "white",
            (self.road_rect.right - 20,
             self.road_rect.y),
            (self.road_rect.right - 20,
             self.road_rect.bottom),
            2)

        # lane divider dashes
        dash_length = 40
        gap = 30
        lane_width = self.road_rect.width // 5


        dividers = [
            self.road_rect.left + lane_width,
            self.road_rect.left + lane_width * 2,
            self.road_rect.left + lane_width * 3,
            self.road_rect.left + lane_width * 4,
        ]

        for divider in dividers:
            y = self.line
            while y < self.road_rect.bottom:
                pygame.draw.line(screen, "white", (divider, y),
                                 (divider, y + dash_length), 2)
                y += dash_length + gap

        # vertical scrolling movement
        if road_movement:
            self.line += self.line_speed
            if self.line > self.road_rect.top + dash_length + gap:
                self.line = self.road_rect.top

    def draw_score(self, screen, score):
        """Draw the current score and highest score.

        :param screen: pygame display surface
        :param score: current player score"""
        # high score and current score display
        highest_score_text = self.score_font.render(
            f"Highest: {self.highest_score}", True, "white")
        personal_score_text = self.score_font.render(
            f"Score: {score}", True, "white")

        # pinned to the top right of the green sign bar
        screen.blit(personal_score_text, (480, 30))
        screen.blit(highest_score_text, (480, 8))

    def draw_question(self, screen, equation):
        """Draw the current question

        :param screen: pygame display surface
        :param equation: current equation
        """
        # display math equation using shadow helper
        # Centered at (300, 25) to sit inside the top green sign
        draw_text_with_shadow(screen, equation, self.question_font, (300, 25))

    def draw_health(self, screen, health):
        """Draw the current heart
        :param health:
        :param screen: pygame display surface
        """
        for i in range(health):
            screen.blit(self.heart, (250 + i*30, 45))
