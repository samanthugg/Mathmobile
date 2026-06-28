"""This Module contains Answer class for Mathmobile game
    They can be correct True or False (wrong or right answer)
    They hold the answer value and are assigned a lane at creation"""


class Answer():
    """Defines the Answer class - correct and incorrect answer to equations"""

    def __init__(self, value: int, correct: bool, lane: int):
        self._value = value
        self._correct = correct
        self._lane = lane

        """Removed out of date todo statements
            drawing and images will be handled 
            in the ui files"""

    @property
    def value(self) -> int:
        """returns the int value property"""
        return self._value

    @property
    def correct(self) -> bool:
        """returns the boolean correct property"""
        return self._correct

    @property
    def lane(self) -> int:
        """Returns the lane property"""
        return self._lane

    def __str__(self) -> str:
        """returns the string representation of the value"""
        return f"{self._value}"

    def __repr__(self) -> str:
        """added to ensure this prints nicely on print statement"""
        return self.__str__()
