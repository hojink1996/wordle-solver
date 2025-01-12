from typing import Callable

import pytest

from wordle_solver.cache import WordleCache
from wordle_solver.clue import Clue
from wordle_solver.inverted_index import InvertedIndex
from wordle_solver.search_space import SearchSpace
from wordle_solver.solver import WordleSolver
from wordle_solver.wordle_index import WordleIndex


@pytest.fixture
def groups() -> dict[str, set[str]]:
    return {"abc": {"abc", "ghi"}, "def": {"def", "jkl"}}


@pytest.fixture
def clue_factory() -> Callable[[int, str, bool, bool], Clue]:
    def _clue_factory(position: int, character: str, in_word: bool, correct_position: bool) -> Clue:
        return Clue(position=position, character=character, in_word=in_word, correct_position=correct_position)

    return _clue_factory


@pytest.fixture
def clues(clue_factory) -> list[Clue]:
    return [
        clue_factory(0, "a", True, True),
        clue_factory(0, "b", True, False),
        clue_factory(2, "c", True, True),
        clue_factory(1, "d", False, False),
        clue_factory(0, "z", False, False),
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


@pytest.fixture
def inverted_index_factory() -> Callable[[list[str], list[str]], InvertedIndex[str, str]]:
    def _inverted_index_factory(letters: list[str], words: list[str]) -> InvertedIndex[str, str]:
        index = InvertedIndex[str, str]()
        for letter, word in zip(letters, words):
            index.add(letter, word)
        return index

    return _inverted_index_factory


@pytest.fixture
def all_words() -> set[str]:
    return {
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
    }


@pytest.fixture
def word_length() -> int:
    return 5


@pytest.fixture
def wordle_index_factory() -> Callable[[list[str], int], WordleIndex]:
    def _wordle_index_factory(words: list[str], word_length: int) -> WordleIndex:
        cache = WordleCache()
        return WordleIndex(words=words, word_length=word_length, cache=cache)

    return _wordle_index_factory


@pytest.fixture
def search_space(all_words: set[str]) -> SearchSpace:
    return SearchSpace(all_words=all_words, groups=None)


@pytest.fixture
def wordle_solver(
    search_space: SearchSpace,
    wordle_index_factory: Callable[[list[str], int], WordleIndex],
    all_words: set[str],
    word_length: int,
) -> WordleSolver:
    wordle_index = wordle_index_factory(list(all_words), word_length)
    return WordleSolver(candidate_lister=wordle_index, search_space=search_space)
