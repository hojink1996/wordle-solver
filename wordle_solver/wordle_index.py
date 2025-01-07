from wordle_solver.clue import Clue
from wordle_solver.inverted_index import InvertedIndex
from wordle_solver.cache import Cache


class WordleIndex:
    """A class for indexing the words in the Wordle word list and get the list of currently valid words.

    Attributes:
        words:
            The list of valid words for the game.
        word_length:
            The length of the words in the list.
        cache:
            The cache to store the results of the clues.
    """

    def __init__(self, words: list[str], word_length: int, cache: Cache[Clue, set[str]]):
        # We create an inverted index for each of the characters in the word
        self.words = set(words)
        self.word_length = word_length
        self.cache = cache
        self._indices = [InvertedIndex[str, str]() for _ in range(word_length)]
        self._init_indices(words)
        self._clues = []
        self._solved_characters = set()
        self._candidate_characters = set()
        self._currently_valid_words = self.words

    def _add_word(self, word: str):
        """Adds the given word to the Inverted Indices."""
        for index, character in enumerate(word):
            self._indices[index].add(character, word)

    def _init_indices(self, words: list[str]):
        """Initializes the indices by adding the given words to the indices."""
        for word in words:
            self._add_word(word)

    def reset_clues(self):
        """Resets the clues."""
        self._clues = []
        self._solved_characters = set()
        self._candidate_characters = set()
        self._currently_valid_words = self.words

    def add_clue(self, clue: Clue):
        """Adds a clue to the index and updates the set of currently valid words."""

        # Check if the clue is unknown and the character is already solved or a candidate. If this is the case, custom
        # logic needs to be implemented to handle the case since the valid words are no longer the intersection of
        # the possible words for each character.
        unknown_clue_with_observed_character = (
            clue.character in self._solved_characters or clue.character in self._candidate_characters
        )

        # First check that the value is in the cache
        cache_hit = self.cache.get(clue)
        if cache_hit is not None and not unknown_clue_with_observed_character:
            self._currently_valid_words = set.intersection(self._currently_valid_words, cache_hit)
            if clue.correct_position:
                self._solved_characters.add(clue.character)
            elif clue.in_word:
                self._candidate_characters.add(clue.character)
            return

        # If the value is not in the cache, we need to calculate its possible words
        if clue.correct_position:
            valid_words = self._indices[clue.position].get(clue.character)
            self._solved_characters.add(clue.character)
        elif clue.in_word:
            valid_words = set()
            self._candidate_characters.add(clue.character)
            possible_indices = [index for index in range(self.word_length) if index != clue.position]
            for index in possible_indices:
                valid_words.update(self._indices[index].get(clue.character))
        else:
            valid_words = self.words
            if unknown_clue_with_observed_character:
                valid_words = set.intersection(
                    valid_words, self._indices[clue.position].get_does_not_contain([clue.character])
                )
            else:
                for index in self._indices:
                    valid_words = set.intersection(valid_words, index.get_does_not_contain([clue.character]))

        if not unknown_clue_with_observed_character:
            self.cache.set(clue, valid_words)
        self._currently_valid_words = set.intersection(self._currently_valid_words, valid_words)

    def add_clues(self, clues: list[Clue]):
        """Adds a set of clues to the index."""
        for clue in clues:
            self.add_clue(clue)

    def get_possible_words(self) -> set[str]:
        """Returns the set of possible words given the current set of clues."""
        return self._currently_valid_words

    def get_all_words(self) -> set[str]:
        """Returns the set of all possible words."""
        return self.words
