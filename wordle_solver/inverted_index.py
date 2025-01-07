from collections import defaultdict
from typing import Generic, TypeVar

D = TypeVar("D")
W = TypeVar("W")


class InvertedIndex(Generic[W, D]):
    """Implementation for a Generic Inverted Index.

    We use the terminology of words and documents for the sake of clarity, but the implementation is generic. Words
    can be of any type (denoted by `W`) and documents can be of any type (denoted by `D`)."""

    def __init__(self):
        self._index: dict[W, set[D]] = defaultdict(set)

    def add(self, word: W, document: D):
        """Adds a word-document pair to the index."""
        self._index[word].add(document)

    def get(self, word: W) -> set[D]:
        """Returns the set of documents that contain the given word."""
        return self._index.get(word, set())

    def get_contains(self, words: list[W]) -> set[D]:
        """Returns the set of documents that contain one of the given words."""
        if not words:
            return set()
        return set.union(*[self._index.get(word, set()) for word in words])

    def get_does_not_contain(self, words: list[W]) -> set[D]:
        """Returns the set of documents that do not contain the given words."""
        searchable_words = [word for word in self._index.keys() if word not in words]
        filtered_documents = set.union(*[self._index[word] for word in searchable_words])

        return filtered_documents

    def get_possible_words(self) -> set[W]:
        """Returns the set of all words that are in the index."""
        return set(self._index.keys())
