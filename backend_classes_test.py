"""Comprehensive Unit Tests for Mathmobile: Equations, Answers, Leaderboard, and Session"""

import pytest
from unittest.mock import MagicMock, patch

# Import all backend classes from your uploaded files
from equations import Addition, Subtraction, Multiplication, Division, Equation
from leaderboard import Leaderboard
from session import Session
from answer import Answer
from enums import DifficultyLevel, Operation
from car import Car

# =====================================================
# Equation Logic Tests
# =====================================================


def test_equation_functionality():
    """Verifies that the abstract Equation class cannot be instantiated.
    Verifies the parameters and other equation methods return the proper results"""
    with pytest.raises(TypeError):
        Equation(10, 5, "+")
    add = Addition(12, 8)
    add2 = Addition(8, 12)
    mul = Multiplication(10, 2)
    add3 = Addition(12, 8)
    assert add.__eq__(add2) is False
    assert add.__eq__(add3) is True
    assert add.__eq__(mul) is False
    assert str(add) == "12 + 8"
    assert repr(add) == "12 + 8"


def test_addition_functionality():
    """Verifies addition math, equation parameters, equation equality, and string formatting"""
    add = Addition(12, 8)
    assert add.operand1 == 12
    assert add.operator == "+"
    assert add.operand2 == 8
    assert add.get_result() == 20


def test_subtraction_functionality():
    """Verifies subtraction math"""
    sub = Subtraction(20, 5)
    assert sub.operand1 == 20
    assert sub.operator == "-"
    assert sub.operand2 == 5
    assert sub.get_result() == 15


def test_multiplication_functionality():
    """Verifies multiplication uses correct symbol (\u00D7)"""
    mult = Multiplication(5, 5)
    assert mult.operand1 == 5
    assert mult.operator == "×"
    assert mult.operand2 == 5
    assert mult.get_result() == 25



def test_division_safety_and_functionality():
    """Verifies division math and zero-divisor protection"""
    div = Division(10, 2)
    div2 = Division(9, 2)
    assert div.operand1 == 10
    assert div.operator == "÷"
    assert div.operand2 == 2
    assert div.get_result() == 5
    assert div2.operand1 == 9
    assert div2.operator == "÷"
    assert div2.operand2 == 2
    assert div2.get_result() == 4

    with pytest.raises(ZeroDivisionError):
        Division(10, 0)

# =====================================================
# Answer & Session Integration Tests
# =====================================================


def test_answer_object_initialization():
    """Tests if Answer objects store math data correctly"""
    ans = Answer(value=15, correct=True, lane=2)
    assert ans.value == 15
    assert ans.correct is True
    assert ans.lane == 2
    assert str(ans) == "15"
    assert repr(ans) == "15"


def test_session_answer_verification():
    """Verifies that Session generates a correct Answer matching the Equation"""
    mock_car = MagicMock()
    # Create session with Addition
    sess = Session(mock_car, qty_equations=5, op=Operation.ADD)

    for frame in sess.master_data:
        equation = frame["Equation"]
        correct_val = equation.get_result()

        # Check lanes 1, 2, 3, 4, and 5 for the correct Answer object
        found_correct = False
        for lane in [1, 2, 3, 4, 5]:
            ans_obj = frame[lane]
            if ans_obj.correct:
                assert ans_obj.value == correct_val
                found_correct = True
        assert found_correct is True  # Ensure a correct answer always exists

# =====================================================
# Leaderboard & Session Utility Tests
# =====================================================


def test_subtraction_swap_logic():
    """Verifies Session swaps operands to prevent negative subtraction"""
    mock_car = MagicMock()
    # Small range subtraction test
    sess = Session(mock_car, qty_equations=20, op=Operation.SUBTRACT)

    for frame in sess.master_data:
        eqn = frame["Equation"]
        # In subtraction, operand1 must be >= operand2
        assert eqn.operand1 >= eqn.operand2


def test_session_division():
    """Ensure the division equations produced in Session result in integers"""
    mock_car = MagicMock()
    sess = Session(mock_car, 20, DifficultyLevel.HARD, Operation.DIVIDE)

    for frame in sess.master_data:
        equation = frame["Equation"]
        assert isinstance((equation.get_result()), int)
        assert (equation.operand1 / equation.operand2) == equation.get_result()


def test_leaderboard_sorting(tmp_path):
    """Verifies score sorting and persistence"""
    file = tmp_path / "test_lb.json"
    easy = DifficultyLevel.EASY
    add = Operation.ADD
    lb = Leaderboard(str(file))

    lb.insert_score(easy, add, "Sam", 50)
    lb.insert_score(easy, add, "Alex", 100)
    lb.insert_score(easy, add, "Bob", 75)
    lb.insert_score(easy, add, "Tammy", 100)
    lb.insert_score(easy, add, "A", 20)
    lb.insert_score(easy, add, "b", 33)
    lb.insert_score(easy, add, "c", 34)
    lb.insert_score(easy, add, "d", 25)
    lb.insert_score(easy, add, "e", 50)
    lb.insert_score(easy, add, "f", 10)

    # Verify score")
    scores = lb.get_scores(DifficultyLevel.EASY, Operation.ADD)
    assert scores[0]['score'] == 100
    assert scores[1]['score'] == 100
    assert scores[2]['score'] == 75
    assert scores[3]['score'] == 50
    assert scores[4]['score'] == 50
    assert scores[5]['score'] == 34
    assert scores[6]['score'] == 33
    assert scores[7]['score'] == 25
    assert scores[8]['score'] == 20
    assert scores[9]['score'] == 10

    lb.insert_score(easy, add, "Tina", 200)

    scores = lb.get_scores(easy, add)
    assert scores[0]['score'] == 200
    assert scores[0]['name'] == "Tina"
    assert scores[9]['score'] == 20
    assert len(scores) == 10


@pytest.fixture
def mock_car():
    """Mocks the Car object to prevent UI dependencies from breaking tests."""
    return MagicMock(spec=Car)


@pytest.fixture
def default_session(mock_car):
    """Fixture providing a standard easy-mode session."""
    return Session(car=mock_car, qty_equations=5, level=DifficultyLevel.EASY, op=Operation.ADD)


def test_session_initialization(default_session, mock_car):
    """Tests initialization of default session parameters."""
    assert default_session.car == mock_car
    assert default_session.score == 0
    assert default_session.qty_lanes == 5
    assert default_session.damage == 0
    assert len(default_session.master_data) == 5


def test_score_and_damage_modifiers(default_session):
    """Tests methods that alter gameplay state."""
    default_session.increase_score(50)
    assert default_session.score == 50

    default_session.add_damage()
    assert default_session.damage == 1


def test_generate_equation(default_session):
    """Tests that equations are generated within bounds based on selected enums."""
    eq = default_session.generate_equation()

    assert eq.operator == "+"
    # For EASY mode, bounds are 0 to 10
    assert 0 <= eq.operand1 <= 10
    assert 0 <= eq.operand2 <= 10


def test_make_int_list_in_range(default_session):
    """Tests integer randomizer ensures unique answers within range, omitting the correct answer."""
    omit_val = 5
    int_list = default_session.make_int_list_in_range(1, 10, omit=omit_val)

    assert len(int_list) == 4
    assert omit_val not in int_list
    assert len(set(int_list)) == 4  # Validates all numbers are unique


def test_build_data_frame(default_session):
    """Tests the structure of a single equation dictionary frame."""
    frame = default_session.build_data_frame()

    assert "Equation" in frame
    # A complete frame should have the Equation key + 5 lanes (1 through 5)
    assert len(frame) == 6

    # Ensure exactly one lane holds the 'correct' Answer object
    correct_answers = [ans for key, ans in frame.items() if key != "Equation" and ans.correct is True]
    assert len(correct_answers) == 1


def test_build_master_data_length(mock_car):
    """Tests that the master data creates the exact quantity of equations requested."""
    sess = Session(car=mock_car, qty_equations=15, level=DifficultyLevel.MEDIUM, op=Operation.SUBTRACT)
    assert len(sess.master_data) == 15


@pytest.fixture
def temp_leaderboard(tmp_path):
    """Fixture to provide a Leaderboard instance utilizing a temporary file."""
    file_path = tmp_path / "test_leaderboard.json"
    return Leaderboard(file_path=str(file_path))


def test_leaderboard_initialization_empty(temp_leaderboard):
    """Tests that a missing file creates an empty scores list."""
    assert temp_leaderboard.scores_list == []


def test_insert_and_get_scores(temp_leaderboard):
    """Tests inserting a new score and retrieving it accurately."""
    success = temp_leaderboard.insert_score(DifficultyLevel.EASY, Operation.ADD, "QualityTester", 100)
    assert success is True

    scores = temp_leaderboard.get_scores(DifficultyLevel.EASY, Operation.ADD)
    assert len(scores) == 1
    assert scores[0]["name"] == "QualityTester"
    assert scores[0]["score"] == 100


def test_get_scores_not_found(temp_leaderboard):
    """Tests getting scores for an unplayed category returns None."""
    assert temp_leaderboard.get_scores(DifficultyLevel.HARD, Operation.DIVIDE) is None


def test_leaderboard_max_ten_entries(temp_leaderboard):
    """Tests that the leaderboard trims entries beyond the top 10."""
    # Insert 11 scores with varying values
    for i in range(11):
        temp_leaderboard.insert_score(DifficultyLevel.HARD, Operation.MULTIPLY, f"Player{i}", i * 10)

    scores = temp_leaderboard.get_scores(DifficultyLevel.HARD, Operation.MULTIPLY)

    # Assert length is capped at 10
    assert len(scores) == 10

    # The lowest score (Player0, score: 0) should be dropped
    assert not any(s["name"] == "Player0" for s in scores)

    # Assert the highest score is at the top (index 0)
    assert scores[0]["score"] == 100