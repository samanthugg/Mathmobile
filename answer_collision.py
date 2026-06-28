"""This module contains the AnswerCollision class."""
import pygame

from resource_helper import resource_path
from ui_helper import draw_text_with_shadow


class AnswerCollision:
    """Handles moving answers, drawing them, and detecting collisions."""

    def __init__(self, game_screen):
        """Initializes answer collision handler.

        :param game_screen: game screen object that holds lane and car data
        """
        self.game_screen = game_screen

        # answer movement and font
        self.answer_y = 100
        self.answer_speed = 1.5
        self.answer_font = pygame.font.Font(
            resource_path('assets/font/PressStart2P-Regular.ttf'), 25)
        self.hit_lane = None

        # tracks correct answers for speed changes
        self.correct_count = 0


    def reset(self):
        """Resets answer position and hit state for the next question."""
        self.answer_y = 100
        self.hit_lane = None


    def draw_answers(self, screen, current_question, moving):
        """Draws answer boxes, moves them, and checks for collisions.

        :param screen: pygame display surface
        :param current_question: collection of answers for the current question
        :param moving: whether the answers should move down the screen
        :return: the answer object that was hit, or None
        """
        # map lane numbers to x positions from game screen
        lane_x_positions = {
            1: self.game_screen.lane_x_positions[0],
            2: self.game_screen.lane_x_positions[1],
            3: self.game_screen.lane_x_positions[2],
            4: self.game_screen.lane_x_positions[3],
            5: self.game_screen.lane_x_positions[4]
        }
        # move answers down if game is active
        if moving:
            self.answer_y += self.answer_speed

        # draw each of the 5 lane answers
        for lane in [1, 2, 3, 4, 5]:
            if lane == self.hit_lane:
                continue

            answer = current_question[lane]
            x = lane_x_positions[answer.lane]

            # draw answer box
            box_rect = pygame.Rect(x - 30, int(self.answer_y) - 25, 60, 40)

            pygame.draw.rect(screen, pygame.Color('black'), box_rect)
            pygame.draw.rect(screen, pygame.Color('white'), box_rect, 2)

            # draw text using helper for shadow effect
            draw_text_with_shadow(
                screen, str(
                    answer.value), self.answer_font, (x, int(
                        self.answer_y)))

            # check for collision with car
            if self.game_screen.car.car_rect.colliderect(box_rect):
                self.hit_lane = lane
                return answer
