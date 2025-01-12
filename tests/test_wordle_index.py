from typing import Callable

import pytest

from wordle_solver.clue import Clue
from wordle_solver.wordle_index import WordleIndex


@pytest.mark.parametrize(
    "clue_position,clue_character,in_word,correct_position,expected_valid_words",
    [
        (0, "a", True, True, {"apple", "awake", "alive", "arise"}),
        # TODO: Fix the expected value so that "awake" is not included in the set.
        (0, "a", True, False, {"awake", "happy", "grape", "peach"}),
        (4, "o", True, True, {"hello"}),
        (0, "z", True, True, set()),
        (0, "a", False, False, {"hello", "world", "melon", "other", "green"}),
        (
            0,
            "z",
            False,
            False,
            {
                "hello",
                "world",
                "happy",
                "apple",
                "grape",
                "melon",
                "peach",
                "arise",
                "awake",
                "alive",
                "other",
                "green",
            },
        ),
    ],
)
def test_add_clue(
    clue_position: int,
    clue_character: str,
    in_word: bool,
    correct_position: bool,
    expected_valid_words: set[str],
    all_words: set[str],
    word_length: int,
    clue_factory: Callable[[int, str, bool, bool], Clue],
    wordle_index_factory: Callable[[list[str], int], WordleIndex],
):
    wordle_index = wordle_index_factory(list(all_words), word_length)
    clue = clue_factory(clue_position, clue_character, in_word, correct_position)
    wordle_index.add_clue(clue)
    assert wordle_index.get_possible_words() == expected_valid_words
    assert wordle_index.get_all_words() == all_words
    wordle_index.reset_clues()
    assert wordle_index.get_possible_words() == all_words


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
def test_add_clues(
    clue_positions: list[int],
    clue_characters: list[str],
    clue_in_words: list[bool],
    clue_correct_positions: list[bool],
    expected_valid_words: set[str],
    all_words: set[str],
    word_length: int,
    clue_factory: Callable[[int, str, bool, bool], Clue],
    wordle_index_factory: Callable[[list[str], int], WordleIndex],
):
    wordle_index = wordle_index_factory(list(all_words), word_length)
    clues = []
    for clue_position, clue_character, in_word, correct_position in zip(
        clue_positions, clue_characters, clue_in_words, clue_correct_positions
    ):
        clues.append(clue_factory(clue_position, clue_character, in_word, correct_position))
    wordle_index.add_clues(clues)
    assert wordle_index.get_possible_words() == expected_valid_words
    assert wordle_index.get_all_words() == all_words
    wordle_index.reset_clues()
    assert wordle_index.get_possible_words() == all_words
