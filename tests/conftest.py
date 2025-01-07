import pytest

from wordle_solver.clue import Clue


@pytest.fixture
def all_words() -> set[str]:
    return {"abc", "def", "ghi", "jkl"}


@pytest.fixture
def groups() -> dict[str, set[str]]:
    return {"abc": {"abc", "ghi"}, "def": {"def", "jkl"}}


@pytest.fixture
def clues() -> list[Clue]:
    return [
        Clue(position=0, character="a", in_word=True, correct_position=True),
        Clue(position=0, character="b", in_word=True, correct_position=False),
        Clue(position=2, character="c", in_word=True, correct_position=True),
        Clue(position=1, character="d", in_word=False, correct_position=False),
        Clue(position=0, character="z", in_word=False, correct_position=False),
    ]


@pytest.fixture
def valid_words_per_clue() -> list[set[str]]:
    return [
        {"abc"},
        {"abc"},
        {"abc"},
        {"abc", "ghi", "jkl"},
        {"abc", "def", "ghi", "jkl"},
    ]
