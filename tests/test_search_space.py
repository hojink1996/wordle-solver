import pytest

from wordle_solver.search_space import SearchSpace


@pytest.fixture
def words() -> set[str]:
    return {"abc", "def", "ghi", "jkl"}


@pytest.mark.parametrize(
    "current_search_size,search_size,best_initial_candidate,expected_initial_candidates,expected_follow_up_candidates,use_groups",
    [
        (1, 5, "abc", {"abc", "def", "ghi", "jkl"}, {"abc"}, False),
        (10, 5, "abc", {"abc", "def", "ghi", "jkl"}, {"abc"}, False),
        (
            1,
            5,
            "def",
            {"abc", "def", "ghi", "jkl"},
            {"def"},
            True,
        ),
        (
            10,
            5,
            "def",
            {"abc", "def"},
            {"def", "jkl"},
            True,
        ),
    ],
)
def test_search_space(
    words: set[str],
    groups: dict[str, set[str]],
    current_search_size: int,
    search_size: int,
    best_initial_candidate: str,
    expected_initial_candidates: set[str],
    expected_follow_up_candidates: set[str],
    use_groups: bool,
):
    search_space = SearchSpace(all_words=words, groups=groups if use_groups else None, max_search_size=search_size)
    initial_candidates = search_space.get_initial_candidates(current_search_size=current_search_size)
    follow_up_candidates = search_space.get_follow_up_candidates(
        best_candidate=best_initial_candidate, current_search_size=current_search_size
    )
    assert initial_candidates == expected_initial_candidates
    assert follow_up_candidates == expected_follow_up_candidates
