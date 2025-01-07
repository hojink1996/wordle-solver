import math

from tqdm import tqdm

from wordle_solver.candidates import CandidateLister
from wordle_solver.clue import Clue
from wordle_solver.search_space import SearchSpace


class WordleSolver:
    """A class that uses Entropy to solve Wordle.

    The algorithm works by calculating the expected entropy of each guess, and then selecting the guess that minimizes
    the expected entropy. This assumes that each valid word is equally likely to be the target word."""

    def __init__(self, candidate_lister: CandidateLister, search_space: SearchSpace, verbose: bool = True):
        self.candidate_lister = candidate_lister
        self.search_space = search_space
        self.verbose = verbose
        self._clues = []

    def _get_clues(self, guess: str, target: str) -> list[Clue]:
        """Get the clues for the given guess and target."""
        clues = []
        for index, character in enumerate(guess):
            if character == target[index]:
                clues.append(Clue(character=character, position=index, correct_position=True, in_word=True))
            elif character in target:
                clues.append(Clue(character=character, position=index, correct_position=False, in_word=True))
            else:
                clues.append(Clue(character=character, position=index, correct_position=False, in_word=False))

        return clues

    def _calculate_entropy(self, candidate_guess: str, all_possible_words: set[str]) -> float:
        """Calculates the average entropy of a candidate guess.

        This is the average of the entropy of the candidate guess assuming that the correct word is each of the
        possible words.

        Args:
            candidate_guess:
                The candidate guess for which we want to calculate the entropy.
            all_possible_words:
                The set of all possible words that we are considering.

        Returns:
            The average entropy of the candidate guess.
        """
        entropies = []
        for possible_word in all_possible_words:
            self.candidate_lister.reset_clues()
            self.candidate_lister.add_clues(self._clues)
            self.candidate_lister.add_clues(self._get_clues(candidate_guess, possible_word))
            try:
                entropy = math.log2(len(self.candidate_lister.get_possible_words()))
                entropies.append(entropy)
            except ValueError:
                print("Error in entropy calculation.")

        return sum(entropies) / len(entropies)

    def add_clues(self, clues: list[Clue]):
        """Adds a set of clues to the solver."""
        self._clues.extend(clues)
        self.candidate_lister.add_clues(clues)

    def get_best_candidate(self, candidates: set[str], possible_words: set[str]) -> str:
        """Evaluate the candidates against the possible words to get the best candidate.

        Args:
            candidates:
                A set of candidates to evaluate.
            possible_words:
                The set of possible words to still remaining, which we evaluate the candidates against.

        Returns:
            A tuple containing the best candidate and the entropy of that candidate.
        """
        best_candidate = ""
        min_entropy = float("inf")
        iterable = tqdm(candidates) if self.verbose else candidates
        for candidate in iterable:
            entropy = self._calculate_entropy(candidate, possible_words)
            if entropy < min_entropy:
                min_entropy = entropy
                best_candidate = candidate
        return best_candidate

    def get_next_word(self) -> str:
        """Returns the next word that should be guessed. This is the word that minimizes the expected entropy of the
        possible words."""
        self.candidate_lister.reset_clues()
        self.candidate_lister.add_clues(self._clues)

        # Possible words are those that are valid given the current clues
        possible_words = self.candidate_lister.get_possible_words()
        current_search_size = len(possible_words)
        candidates = self.search_space.get_initial_candidates(current_search_size)

        # Do two loops of evaluation to get the best candidate. The first loop uses a smaller search space to narrow
        # down the candidates.
        best_candidate = self.get_best_candidate(candidates, possible_words)
        follow_up_candidates = self.search_space.get_follow_up_candidates(best_candidate, current_search_size)

        return self.get_best_candidate(follow_up_candidates, possible_words)

    def get_possible_words(self) -> set[str]:
        """Get the set of all possible words given the current set of clues."""
        self.candidate_lister.reset_clues()
        self.candidate_lister.add_clues(self._clues)
        return self.candidate_lister.get_possible_words()
