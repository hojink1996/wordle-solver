from typing import Protocol

from wordle_solver.clue import Clue


class CandidateLister(Protocol):
    """Class in charge of listing the possible candidate words for a given set of clues in Wordle."""

    def add_clue(self, clue: Clue):
        """Adds a clue to the list of clues."""
        ...

    def add_clues(self, clues: list[Clue]):
        """Adds a set of clues to the list of clues."""
        ...

    def get_possible_words(self) -> set[str]:
        """Returns the set of possible words given the current set of clues."""
        ...

    def get_all_words(self) -> set[str]:
        """Returns the set of all possible words."""
        ...

    def reset_clues(self):
        """Reset the clues that were received by the index."""
        ...
