"""Session class holds details of the Mathmobile project game in session"""

import random
from car import Car
from enums import DifficultyLevel, Operation
from equations import Equation, Addition, Subtraction, Multiplication, Division
from answer import Answer


class Session():
    """Class Session has details of current game session
        including speed, score, and the list of equation
        dictionaries. The equations and answers are generated in this class
        based on the operation and difficulty selected by the player"""

    def __init__(self, car: Car, qty_equations: int = 50,
                 level: DifficultyLevel = DifficultyLevel.EASY, op: Operation = Operation.ADD,
                 ):

        self._car = car
        self._score = 0
        self._qty_lanes = 5
        self._op = op
        self._damage = 0
        self._level = level
        self._qty_equations = qty_equations
        self._min_operand = 0  # minimum value of operand created
        self._answer_range = 4

        # determine max operand value and range of answers
        match level:
            case DifficultyLevel.EASY:
                self._max_operand1 = 10
                self._max_operand2 = 10

            case DifficultyLevel.MEDIUM:
                self._min_operand = 2  # minimum value of operand created
                if self._op == Operation.ADD or self._op == Operation.SUBTRACT:
                    self._max_operand1 = 25
                else:
                    self._max_operand1 = 15
                self._max_operand2 = 10

            case DifficultyLevel.HARD:
                self._min_operand = 2
                if self._op == Operation.ADD or self._op == Operation.SUBTRACT:
                    self._max_operand1 = 25
                    self._max_operand2 = 25
                else:
                    self._max_operand1 = 15
                    self._max_operand2 = 15

        self._master_data = self.build_master_data()  # list of dictionaries

# ____Properties____

    @property
    def car(self) -> object:
        """Returns the car object associated with this session"""
        return self._car

    @property
    def score(self) -> int:
        """Returns the score int"""
        return self._score

    @property
    def qty_lanes(self) -> int:
        """Returns the number of road lanes in the game"""
        return self._qty_lanes

    @property
    def damage(self) -> int:
        """returns the amount of damage incurred"""
        return self._damage

    @property
    def master_data(self) -> list:
        """Returns a copy of the master data list"""
        return self._master_data.copy()

# ______Methods________

    def increase_score(self, add_amount: int):
        """adds passed in value to score"""
        self._score += add_amount

    def add_damage(self):
        """adds 1 damage to damage"""
        self._damage += 1

    def generate_equation(self) -> Equation:
        """Returns an equation determined by selected Operation
           and DifficultyLevel"""
        # generate operands - range depends on Difficulty Level
        operand1 = random.randint(self._min_operand, self._max_operand1)
        operand2 = random.randint(self._min_operand, self._max_operand2)

        # Generate equation
        match self._op:
            case Operation.ADD:
                equation = Addition(operand1, operand2)

            case Operation.SUBTRACT:
                if operand1 < operand2:  # ensure no neg value, swap operands
                    temp = operand1
                    operand1 = operand2
                    operand2 = temp
                equation = Subtraction(operand1, operand2)

            case Operation.MULTIPLY:
                equation = Multiplication(operand1, operand2)

            case Operation.DIVIDE:
                # ensure that 0 is not an option for operand2
                while operand2 == 0:
                    operand2 = random.randint(
                        self._min_operand, self._max_operand2)

                # ensure that the division = an int, so operand 1 becomes the answer
                equation = Division(int(operand1 * operand2), operand2)

        return equation

    def make_int_list_in_range(self, min_int: int, max_int: int, omit: int) -> list:
        """Method to return a list of 4 integers in a specified range.
            Omits one integer from the range"""

        int_list = []
        while len(int_list) < 4:
            rand_int = random.randint(min_int, max_int)

            if rand_int not in int_list and rand_int != omit:
                int_list.append(rand_int)

        return int_list

    def build_data_frame(self) -> dict:
        """builds a dictionary that holds the equation and answers
        for one problem of the game - helper method for build_master_data
        """
        # get real result from generated equation
        equation = self.generate_equation()
        result = equation.get_result()

        # determine answer ranges based on result
        min_int = result - self._answer_range
        if min_int < 0:
            min_int = 0

        max_int = result + self._answer_range

        # generate a list of wrong answers different from result
        answers = self.make_int_list_in_range(min_int, max_int, result)

        # assign the correct answer to a random lane
        # this is logic for 5 lanes.  Assumes correct_lane is 5.
        # swaps the number of wrong_lane to 5 if otherwise
        correct_lane = random.randint(1, 5)
        wrong_lane1 = 1
        wrong_lane2 = 2
        wrong_lane3 = 3
        wrong_lane4 = 4

        match correct_lane:
            case 1:
                wrong_lane1 = 5

            case 2:
                wrong_lane2 = 5

            case 3:
                wrong_lane3 = 5

            case 4:
                wrong_lane4 = 5

        # initialize dictionary with equation
        return {
            "Equation": equation,
            correct_lane: Answer(result, True, correct_lane),
            wrong_lane1: Answer(answers[0], False, wrong_lane1),
            wrong_lane2: Answer(answers[1], False, wrong_lane2),
            wrong_lane3: Answer(answers[2], False, wrong_lane3),
            wrong_lane4: Answer(answers[3], False, wrong_lane4)}

    def build_master_data(self) -> list:
        """builds master data list with qty_equations equations.
            Includes correct Answer in random lane assignment
            and incorrect Answers in remaining qty_lanes
        """
        frames = []
        for _ in range(self._qty_equations):
            frames.append(self.build_data_frame())

        return frames


if __name__ == "__main__":
    sess = Session(Car(), 10, DifficultyLevel.MEDIUM, Operation.DIVIDE)
    print("The master data is:")
    for frame in sess.master_data:
        print(frame)

    print(f"Lanes: {sess.qty_lanes}")
    print(f"damage: {sess.damage}")
    sess.add_damage()
    print(f"added damage: {sess.damage}")
    print(f"One dictionary frame: {sess.build_data_frame()}")
    print(f"starting score is: {sess.score}")
    sess.increase_score(100)
    print(f"now the score is {sess.score}")
