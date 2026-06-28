"""This module contains the Car class."""
import pygame

from resource_helper import resource_path


class Car:
    """Handles drawing the car and controlling its movement."""

    def __init__(self):
        """Initializes the car.
        """
        self.lanes = [80, 189, 300, 411, 530]
        # car image
        self.car_image = pygame.image.load(resource_path('assets/img/car.png'))
        # Art created by Jonathan Hungate (Aseprite)
        # Inspired by public domain vector:
        # https://publicdomainvectors.org/en/free-clipart/Blue-racing-car-vector-illustration/9683.html

        self.car_rect = self.car_image.get_rect()

        # lane setup
        self.current_lane = 2
        self.y = 650

    def draw(self, screen):
        """Draws the car on screen.

        :param screen: pygame display surface
        """

        # draw car at current lane
        x = self.lanes[self.current_lane]
        self.car_rect = self.car_image.get_rect(center=(x, self.y))
        screen.blit(self.car_image, self.car_rect)

    def move_left(self):
        """Moves the car one lane to the left."""
        if self.current_lane > 0:
            self.current_lane -= 1

    def move_right(self):
        """Moves the car one lane to the right."""
        if self.current_lane < 4:
            self.current_lane += 1
