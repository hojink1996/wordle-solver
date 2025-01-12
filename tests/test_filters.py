import pytest

from wordle_solver.filters import filter_repeated_characters, group_by_overlapping_characters


@pytest.mark.parametrize(
    "words,expected_output",
    [
        ({"abc", "def", "ghi", "jkl"}, {"abc", "def", "ghi", "jkl"}),
        ({"aab", "aac", "aad"}, set()),
        ({"abc", "def", "ghi", "jkl", "aab", "aac", "aad"}, {"abc", "def", "ghi", "jkl"}),
        ({"aaa", "bbb", "aab", "abd", "def", "ccc"}, {"abd", "def"}),
    ],
)
def test_filter_repeated_characters(words: set[str], expected_output: set[str]):
    assert filter_repeated_characters(words) == expected_output


@pytest.mark.parametrize(
    "words,max_groups,iou_threshold,expected_groups",
    [
        (["abc", "bcd", "abe", "bde"], 2, 0.5, {"abc": {"abc", "bcd", "abe"}, "bde": {"bde"}}),
        (["abc", "bcd", "abe", "bde"], 1, 0.5, {"abc": {"abc", "bcd", "abe", "bde"}}),
        (
            ["abc", "bcd", "fgh", "afg", "ghi", "fhi", "axy"],
            2,
            0.5,
            {"abc": {"abc", "bcd", "axy"}, "fgh": {"fhi", "fgh", "ghi", "afg"}},
        ),
        ([], 2, 0.5, dict()),
    ],
)
def test_group_by_overlapping_characters(
    words: list[str], max_groups: int, iou_threshold: float, expected_groups: dict[str, set[str]]
):
    assert group_by_overlapping_characters(words, max_groups, iou_threshold) == expected_groups
