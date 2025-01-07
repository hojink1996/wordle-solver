from typing import Optional


class SearchSpace:
    """Class used to specify the search space for the Wordle game.

    This class contains certain optimizations for when the search space is too large to evaluate all candiadtes.

    Attributes:
        all_words:
            A set containing all of the possible words that can be used in the game.
        groups:
            An optional dictionary containing a mapping from key words to groups of words that are similar to the key.
        max_search_size:
            The maximum number of candidates for which the solver can use all words as the search space.
            This value determines when to use the groups instead of all words.
    """

    def __init__(self, all_words: set[str], groups: Optional[dict[str, set[str]]], max_search_size: int = 20):
        self.all_words = all_words
        self.groups = groups
        self.max_search_size = max_search_size

    def _use_all_words(self, current_search_size: int) -> bool:
        return self.groups is None or current_search_size <= self.max_search_size

    def get_initial_candidates(self, current_search_size: int) -> set[str]:
        """Get the set of initial candidates for the current search size.

        Args:
            current_search_size:
                The current number of candidates that are being considered.

        Returns:
            A set of strings containing the candidates for the current search size.
        """
        if self._use_all_words(current_search_size):
            return self.all_words
        return set(self.groups.keys())

    def get_follow_up_candidates(self, best_candidate: str, current_search_size: int) -> set[str]:
        """Get the set of follow-up candidates after the initial evaluating the initial candidate.

        Args:
            best_candidate:
                The best candidate that was found from the initial candidates.
            current_search_size:
                The current number of candidates that are being considered.

        Returns:
            A set of strings containing the follow-up candidates.
        """
        if self._use_all_words(current_search_size):
            return {best_candidate}
        return self.groups[best_candidate]
