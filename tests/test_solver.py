from typing import Callable
import pytest

from wordle_solver.clue import Clue
from wordle_solver.solver import WordleSolver


@pytest.mark.parametrize(
    "clue_positions,clue_characters,clue_in_words,clue_correct_positions,expected_valid_words",
    [
        (
            [0, 0],
            ["a", "e"],
            [True, True],
            [True, False],
            {"apple", "awake", "alive", "arise"},
        ),
        (
            [0, 0],
            ["h", "h"],
            [True, True],
            [True, True],
            {"hello", "happy"},
        ),
        (
            [0, 1, 2],
            ["h", "a", "p"],
            [True, True, True],
            [True, True, True],
            {"happy"},
        ),
        (
            [0, 0, 3],
            ["z", "g", "e"],
            [False, True, True],
            [False, True, False],
            # TODO: Fix this so that "green" is not included in the set.
            {"grape", "green"},
        ),
        (
            [0, 0, 4],
            ["z", "g", "e"],
            [False, True, False],
            [False, True, False],
            set(),
        ),
    ],
)
def test_get_possible_words(
    clue_positions: list[int],
    clue_characters: list[str],
    clue_in_words: list[bool],
    clue_correct_positions: list[bool],
    expected_valid_words: set[str],
    clue_factory: Callable[[int, str, bool, bool], Clue],
    wordle_solver: WordleSolver,
):
    clues = []
    for clue_position, clue_character, in_word, correct_position in zip(
        clue_positions, clue_characters, clue_in_words, clue_correct_positions
    ):
        clues.append(clue_factory(clue_position, clue_character, in_word, correct_position))
    wordle_solver.add_clues(clues)
    assert wordle_solver.get_possible_words() == expected_valid_words


@pytest.mark.parametrize(
    "clue_positions,clue_characters,clue_in_words,clue_correct_positions,possible_words",
    [
        (
            [0, 1, 2],
            ["h", "a", "p"],
            [True, True, True],
            [True, True, True],
            ["happy"],
        ),
        ([0], ["z"], [True], [True], []),
        ([0], ["h"], [True], [True], ["happy", "hello"]),
        ([4], ["a"], [True], [False], ["grape", "alive"]),
    ],
)
def test_get_next_word(
    clue_positions: list[int],
    clue_characters: list[str],
    clue_in_words: list[bool],
    clue_correct_positions: list[bool],
    possible_words: list[str],
    clue_factory: Callable[[int, str, bool, bool], Clue],
    wordle_solver: WordleSolver,
):
    clues = []
    for clue_position, clue_character, in_word, correct_position in zip(
        clue_positions, clue_characters, clue_in_words, clue_correct_positions
    ):
        clues.append(clue_factory(clue_position, clue_character, in_word, correct_position))
    wordle_solver.add_clues(clues)
    if len(possible_words) == 0:
        with pytest.raises(ValueError):
            wordle_solver.get_next_word()
    else:
        assert wordle_solver.get_next_word() in possible_words
