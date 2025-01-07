from dataclasses import dataclass


@dataclass
class Clue:
    """Represents a single clue for a wordle puzzle."""

    position: int
    character: str
    in_word: bool
    correct_position: bool
