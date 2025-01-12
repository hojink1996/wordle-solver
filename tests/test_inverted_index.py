from typing import Callable

import pytest

from wordle_solver.inverted_index import InvertedIndex


@pytest.mark.parametrize(
    "letters,words,query_letter,expected_values",
    [
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            "a",
            {"abc", "abd"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            "b",
            {"bcd"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            "c",
            {"bcd", "abc", "bde"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            "d",
            {},
        ),
    ],
)
def test_get_values_from_inverted_index(
    letters: list[str],
    words: list[str],
    query_letter: str,
    expected_values: set[str],
    inverted_index_factory: Callable[[list[str], list[str]], InvertedIndex[str, str]],
):
    inverted_index = inverted_index_factory(letters, words)
    assert inverted_index.get(query_letter) == set(expected_values)


@pytest.mark.parametrize(
    "letters,words,query_letters,expected_values",
    [
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["a", "b"],
            {"abc", "abd", "bcd"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["b"],
            {"bcd"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["a", "b", "c"],
            {"abc", "abd", "bcd", "bde"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            [],
            {},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["d"],
            {},
        ),
    ],
)
def test_get_contains_inverted_index(
    letters: list[str],
    words: list[str],
    query_letters: list[str],
    expected_values: set[str],
    inverted_index_factory: Callable[[list[str], list[str]], InvertedIndex[str, str]],
):
    inverted_index = inverted_index_factory(letters, words)
    assert inverted_index.get_contains(query_letters) == set(expected_values)


@pytest.mark.parametrize(
    "letters,words,query_letters,expected_values",
    [
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["a", "b"],
            {"bcd", "abc", "bde"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["b"],
            {"abc", "abd", "bcd", "bde"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["a", "b", "c"],
            {},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            [],
            {"abc", "abd", "bcd", "bde"},
        ),
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            ["d"],
            {"abc", "abd", "bcd", "bde"},
        ),
    ],
)
def test_get_does_not_contain_inverted_index(
    letters: list[str],
    words: list[str],
    query_letters: list[str],
    expected_values: set[str],
    inverted_index_factory: Callable[[list[str], list[str]], InvertedIndex[str, str]],
):
    inverted_index = inverted_index_factory(letters, words)
    assert inverted_index.get_does_not_contain(query_letters) == set(expected_values)


@pytest.mark.parametrize(
    "letters,words,expected_values",
    [
        (
            ["a", "a", "b", "c", "c", "c"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde"],
            {"a", "b", "c"},
        ),
        (
            ["a", "a", "b", "c", "c", "c", "d", "e"],
            ["abc", "abd", "bcd", "bcd", "abc", "bde", "ddd", "efg"],
            {"a", "b", "c", "d", "e"},
        ),
        ([], [], set()),
    ],
)
def test_get_possible_words_inverted_index(
    letters: list[str],
    words: list[str],
    expected_values: set[str],
    inverted_index_factory: Callable[[list[str], list[str]], InvertedIndex[str, str]],
):
    inverted_index = inverted_index_factory(letters, words)
    assert inverted_index.get_possible_words() == expected_values
