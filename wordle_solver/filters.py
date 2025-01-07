import numpy as np
import torch
from tqdm import tqdm


def filter_repeated_characters(words: set[str]) -> set[str]:
    """Filters out words that have repeated characters."""
    return {word for word in words if len(set(word)) == len(word)}


def _encode_words(words: list[str]) -> np.ndarray:
    """Encodes the words into a numpy array containing its multi-hot encoding."""
    print("Encoding words...")
    characters = list({character for word in words for character in word})
    encoding = np.zeros((len(words), len(characters)), dtype=np.float32)
    for index, word in enumerate(words):
        for character in word:
            encoding[index, characters.index(character)] = 1
    return encoding


def _compute_iou(multi_hot_encoding: np.ndarray, tolerance: float = 1e-6) -> np.ndarray:
    """Computes the intersection over union of a multi-hot-encoded array."""
    print("Computing IOU...")
    encoding = torch.tensor(multi_hot_encoding).to_sparse()
    intersection = torch.sparse.mm(encoding, encoding.T)
    dense_encoding = encoding.to_dense()
    union = dense_encoding.sum(dim=1)[None, :] + dense_encoding.sum(dim=1)[:, None] - intersection
    return (intersection.to_dense() / (union + tolerance)).numpy()


def group_by_overlapping_characters(
    words: list[str], max_groups: int, iou_threshold: float = 0.7
) -> dict[str, set[str]]:
    """Groups words by the characters that overlap with each other.

    This function selects `max_groups` number of groups to try out. Each of the groups has a key which is the word
    that is used to group the words. The value is the set of words that overlap with the key word the most.
    """
    word_encodings = _encode_words(words)
    overlaps = _compute_iou(word_encodings)
    groups = dict()
    for _ in tqdm(range(max_groups)):
        if len(overlaps) == 0:
            break
        most_overlaps_index = np.sum(overlaps, axis=1).argmax()
        overlapping_words = np.where(overlaps[most_overlaps_index] >= iou_threshold)
        groups[words[most_overlaps_index]] = {words[index] for index in overlapping_words[0]}
        overlaps = np.delete(overlaps, overlapping_words[0], axis=0)
        overlaps = np.delete(overlaps, overlapping_words[0], axis=1)
        words = [word for index, word in enumerate(words) if index not in overlapping_words[0]]

    for word in words:
        best_match = max(groups, key=lambda key: len(set(word) & set(key)))
        groups[best_match].add(word)

    return groups
