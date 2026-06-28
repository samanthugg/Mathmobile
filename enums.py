"""This module contains enum definitions for game states, difficulty levels, and operations."""
from enum import Enum, auto

class GameState(Enum):
    """Tracks which screen or state the game is currently in."""
    MAIN = auto()
    OPERATION = auto()
    DIFFICULTY = auto()
    CREDITS = auto()
    GAME = auto()
    CONFIRM = auto()
    LEADERBOARD = auto()
    GAME_OVER = auto()
    SETTINGS = auto()

class DifficultyLevel(Enum):
    """Defines difficulty levels used for session generation."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Operation(Enum):
    """Defines math operations used in the game session."""
    ADD = "addition"
    SUBTRACT = "subtraction"
    MULTIPLY = "multiplication"
    DIVIDE = "division"