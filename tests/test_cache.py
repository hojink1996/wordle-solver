from typing import Optional

import pytest

from wordle_solver.cache import WordleCache
from wordle_solver.clue import Clue


@pytest.mark.parametrize(
    "key,expected_value",
    [
        (Clue(position=0, character="a", in_word=True, correct_position=True), {"abc"}),
        (Clue(position=1, character="a", in_word=False, correct_position=False), None),
        (Clue(position=0, character="z", in_word=False, correct_position=False), {"abc", "def", "ghi", "jkl"}),
        (Clue(position=1, character="c", in_word=True, correct_position=False), None),
        (Clue(position=1, character="d", in_word=True, correct_position=False), None),
        (Clue(position=0, character="z", in_word=True, correct_position=True), None),
    ],
)
def test_wordle_cache(
    clues: list[Clue], valid_words_per_clue: list[set[str]], key: Clue, expected_value: Optional[set[str]]
):
    cache = WordleCache()
    for clue, valid_words in zip(clues, valid_words_per_clue):
        cache.set(clue, valid_words)
    assert cache.get(key) == expected_value
