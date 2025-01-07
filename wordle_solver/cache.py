from abc import ABC, abstractmethod
from typing import Generic, Optional, Protocol, TypeVar

from wordle_solver.clue import Clue

KT = TypeVar("KT", contravariant=True)
VT = TypeVar("VT")


class Cache(Protocol[KT, VT]):
    """Interface for a generic cache."""

    def set(self, key: KT, value: VT):
        """Sets a value in the cache."""
        ...

    def get(self, key: KT) -> Optional[VT]:
        """Gets a value from the cache."""
        ...


class InMemoryCache(ABC, Generic[KT, VT]):
    """Implementation for a cache that stored the values in memory."""

    def __init__(self):
        self._cache = dict()

    @abstractmethod
    def _encode(self, key: KT) -> str:
        """Encodes the key to a string that will be used to store in the cache."""
        raise NotImplementedError("The `_encode` method must be implemented in the cache.")

    def set(self, key: KT, value: VT):
        """Sets a value in the cache."""
        self._cache[self._encode(key)] = value

    def get(self, key: KT) -> Optional[VT]:
        """Gets a value from the cache."""
        return self._cache.get(self._encode(key), None)


class WordleCache(InMemoryCache[Clue, set[str]]):
    """Cache implementation to store results from the Wordle clues."""

    def _encode(self, key: Clue) -> str:
        """Encodes the clue to a string that will be used to store in the cache."""
        color = "G" if key.correct_position else "Y" if key.in_word else "R"
        return f"{key.position}{key.character}{color}"
