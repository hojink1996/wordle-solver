import json
import os
import pickle as pkl

from wordle_solver.cache import WordleCache
from wordle_solver.clue import Clue
from wordle_solver.filters import group_by_overlapping_characters
from wordle_solver.search_space import SearchSpace
from wordle_solver.solver import WordleSolver
from wordle_solver.wordle_index import WordleIndex

LANGUAGE = "es"
MAX_GROUPS = 100
WORD_LENGTH = 5


def main():
    with open("static/optimal_starts.json", "r") as file:
        optimal_start = json.load(file)[LANGUAGE]
    with open(f"static/wordlist_{LANGUAGE}.txt", "r") as file:
        words = file.read().splitlines()
    if os.path.exists(f"static/groups_{LANGUAGE}.pickle"):
        with open(f"static/groups_{LANGUAGE}.pickle", "rb") as file:
            groups = pkl.load(file)
    else:
        groups = group_by_overlapping_characters(words, max_groups=MAX_GROUPS)
        with open(f"static/groups_{LANGUAGE}.pickle", "wb") as file:
            pkl.dump(groups, file)
    search_space = SearchSpace(all_words=set(words), groups=groups)
    wordle_cache = WordleCache()
    wordle_index = WordleIndex(words=words, word_length=WORD_LENGTH, cache=wordle_cache)
    wordle_solver = WordleSolver(candidate_lister=wordle_index, search_space=search_space)

    print(f'Start by guessing the following word: "{optimal_start}" or any other word you like.')
    while True:
        print("=====================================")
        print("Add the word you guessed:")
        word = input("Word: ")
        print(
            "Add the clues you got. Use 'g' to denote a grey, 'y' to denote a yellow and 'c' to denote a correct clue."
        )
        print(
            "For example, you could get 'ygggc' as a clue if you got the first character rigth but position wrong, and the last character with its position correctly."
        )
        clue = input("Clue: ")

        # Check that the word and clue have the correct length
        if len(word) != WORD_LENGTH:
            raise ValueError(f"The word must have {WORD_LENGTH} characters.")
        if len(clue) != WORD_LENGTH:
            raise ValueError(f"The clue must have {WORD_LENGTH} characters.")

        # Parse the clue
        clues = [
            Clue(
                position=index,
                character=character,
                in_word=clue_character in ["y", "c"],
                correct_position=clue_character in ["c"],
            )
            for index, (character, clue_character) in enumerate(zip(word, clue))
        ]
        wordle_solver.add_clues(clues)
        possible_words = wordle_solver.get_possible_words()
        if len(possible_words) == 1:
            print("Congratulations! You solved the wordle puzzle.")
            print("The word is: ", possible_words.pop().strip())
            break
        print("Possible words: ", possible_words)
        print("Total possible words: ", len(possible_words))
        word_to_guess = wordle_solver.get_next_word()
        print("Guess the following word: ", word_to_guess)


if __name__ == "__main__":
    main()
