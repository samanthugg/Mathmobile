"""This module contains the GameScreen class."""
import pygame

from answer_collision import AnswerCollision
from car import Car
from enums import GameState
from resource_helper import resource_path
from road import Road
from session import Session
from sound import Sound
from ui_helper import draw_button


class GameScreen:
    """Handles gameplay logic, rendering, and input during the game."""

    def __init__(self, game, sound: Sound):
        """ Initializes the game screen.

        :param game: main game controller object
        """

        # reference to main drive
        self.game = game
        self.road = Road()
        self.session = None
        self.current_index = 0
        self.hit_time = None

        # background
        self.background = pygame.image.load(resource_path("assets/img/gameplay.png"))
        # Art asset created by Jonathan Hungate using Aseprite
        self.background = pygame.transform.smoothscale(
            self.background, (600, 780))

        # fonts
        self.button_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 30)
        self.countdown_font = pygame.font.Font(
            resource_path("assets/font/PressStart2P-Regular.ttf"), 50)

        # button
        self.back_button_rect = pygame.Rect(20, 10, 70, 30)

        # countdown timer
        self.countdown = pygame.time.get_ticks()
        self.countdown_timer = 4

        # car + lanes setup
        self.road_rect = self.road.road_rect
        lane_width = self.road_rect.width // 5

        self.lane_x_positions = [
            self.road_rect.left + lane_width * i + lane_width // 2
            for i in range(5)
        ]

        self.lanes = self.lane_x_positions
        self.car = Car()
        self.answer_collision = AnswerCollision(self)

        # question quantity
        self.question_quantity = 40

        self.sound = sound

        # prevent repeat sound
        self.countdown_sound = False

    def game_countdown(self, screen=None):

        if self.game.state != GameState.GAME:
            return False

        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.countdown) / 1000
        remaining = self.countdown_timer - elapsed
        light_remaining = remaining + 0.1

        if remaining > 0:

            # play sound once
            if not self.countdown_sound:
                self.sound.play_sound_countdown()
                self.countdown_sound = True

            if screen is not None:
                radius = 25
                y = 300

                positions = [380, 300, 220]  # right → left
                off = (60, 60, 60)

                colors = [
                    (255, 0, 0),  # right
                    (255, 255, 0),  # mid
                    (0, 255, 0)  # left
                ]

                active = int(light_remaining) - 1

                for i in range(3):
                    color = colors[i] if i >= 3 - active else off
                    pygame.draw.circle(screen, color, (positions[i], y), radius)
                    pygame.draw.circle(screen, "white", (positions[i], y), radius, 3)

                if 0 < remaining <= 1:
                    go_text = self.countdown_font.render("GO!", True, "white")
                    rect = go_text.get_rect(center=(320, 380))
                    screen.blit(go_text, rect)

            return False

        return True

    def start_session(self):
        """Initializes a new gameplay session."""
        all_scores = self.game.leaderboard.get_scores(
            self.game.selected_difficulty, self.game.selected_operation)

        if all_scores:
            self.road.highest_score = all_scores[0]['score']
        else:
            self.road.highest_score = 0

        # initialize new session
        self.session = Session(self.car, self.question_quantity,
                               level=self.game.selected_difficulty,
                               op=self.game.selected_operation)

        # reset speed and correct answer counter for new session
        self.answer_collision.answer_speed = 1.5
        self.answer_collision.correct_count = 0
        self.current_index = 0
        self.hit_time = None

        # reset positions
        self.answer_collision.reset()
        self.car.current_lane = 2

        # restart countdown and music
        self.countdown = pygame.time.get_ticks()
        self.countdown_sound = False
        self.sound.play_music_gameplay()

    def event_handler(self, event):
        """Handles user input during gameplay.

        :param event: pygame event object
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button_rect.collidepoint(event.pos):
                self.sound.play_sound_button()
                self.game.confirmation_screen.mode = "warning"
                self.game.state = GameState.CONFIRM

        # keyboard input (disabled during countdown)
        if event.type == pygame.KEYDOWN and self.hit_time is None:
            if self.game_countdown():
                if event.key == pygame.K_LEFT:
                    self.car.move_left()
                    self.sound.play_sound_tire_left()
                if event.key == pygame.K_RIGHT:
                    self.car.move_right()
                    self.sound.play_sound_tire_right()

    def draw(self, screen):
        """Draws the game screen and handles gameplay rendering.

        :param screen: pygame display surface
        """

        # draw order: background ->  road -> car -> UI
        screen.blit(self.background, (0, 0))

        # check countdown status
        done = self.game_countdown(screen)

        # draw road, score, and health
        self.road.draw(screen, road_movement=done)
        score = self.session.score if self.session is not None else 0
        self.road.draw_score(screen, score)

        if done:
            health = 3 if self.session is None else 3 - self.session.damage
            self.road.draw_health(screen, health)

        # draw car
        self.car.draw(screen)

        self.game_countdown(screen)

        # gameplay logic
        if done and self.session is not None and self.game.state == GameState.GAME:
            # retrieve the active question from the session data
            current_question = self.session.master_data[self.current_index]
            question = f"{current_question['Equation']} = ?"

            # draw math problem using road method
            self.road.draw_question(screen, question)

            # check if we are currently mid-collision/pause
            if self.hit_time is None:
                # check collision; returns the hit answer object if one exists
                hit_answer = self.answer_collision.draw_answers(
                    screen, current_question, done)

                if hit_answer is not None:
                    if hit_answer.correct:
                        # correct: add points
                        self.session.increase_score(10)
                        self.sound.play_sound_correct()
                        self.road.personal_score = self.session.score
                        self.hit_time = pygame.time.get_ticks()

                        # increment correct answer counter
                        self.answer_collision.correct_count += 1

                        # every 2 correct answers, increase falling speed
                        if self.answer_collision.correct_count % 2 == 0:
                            self.answer_collision.answer_speed += .3
                            print("speed:", self.answer_collision.answer_speed)

                    else:
                        # wrong: reset collision state and end the game
                        self.session.add_damage()
                        self.sound.play_sound_incorrect()
                        self.hit_time = pygame.time.get_ticks()

                        # end game if player loses all health
                        if self.session.damage >= 3:
                            self.answer_collision.reset()
                            self.game.state = GameState.GAME_OVER

                        # reset correct answer counter
                        self.answer_collision.correct_count = 0

                        # decrease falling speed with a minimum limit
                        self.answer_collision.answer_speed = max(1.2, self.answer_collision.answer_speed - 1)
                        print("speed:", self.answer_collision.answer_speed)
            else:
                # show answers while pausing for hit effect
                self.answer_collision.draw_answers(
                    screen, current_question, done)

            # next question transition delay
            if self.hit_time is not None:
                if pygame.time.get_ticks() - self.hit_time > 800:
                    self.answer_collision.reset()
                    self.current_index += 1
                    self.hit_time = None

                    # restart session loop if end reached
                    if self.current_index >= len(self.session.master_data):
                        self.game.state = GameState.GAME_OVER

        # draw navigation buttons
        draw_button(screen, self.back_button_rect, "\u2190", self.button_font)
