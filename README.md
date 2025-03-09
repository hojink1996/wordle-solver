# Wordle Solver

Wordle is a web game that gained widespread popularity during 2021-2022.
The objective of the game is to guess a hidden five-letter word in six tries or less
by guessing words and getting feedback in the form of clues that indicate
whether the each letter appears in the hidden word and its respective position.

Its popularity has spawned a variety of different "Wordle Variations" such as
Squardle, Semantle, Squabble, etc; and was even bought by The New York Times
in February 2022.

Wordle is an interesting study case for Information Theory. The optimal guess
is not necessarily one that is valid (i.e. meets the conditions for
all of the clues available), but rather a guess that gives the most
_information_.

## Methodology

To determine the word that gives the most _information_, first we need to
explain how we measure information.

To measure _information_ we are going to use _Entropy_, which is a measure
of uncertainty of a Random Variable. We can consider the distribution of
words that are available as our Random Variable $X$ and measure the _Entropy_
for each of our guesses.

If we call the set of words that are valid given the currently available
clues $V$, and its cardinality as $\lvert V \rvert = n$, we can say that
for each element $v \in V$, $P(v | C) = \frac{1}{n}$. Here $C$ denotes the
set of currently availables clues.

Given that we don't know the actual target word $t$, we cannot compute the
probability after a new guess, since we do not know the new set of clues
$\tilde{C}$. However, since we know that $t \in V$ we can get the expected
probability after the guess as:

$$\mathbb{E}(P(v | \tilde{C})) = \frac{1}{n} \sum_{\hat{t} \in V} P(v | \hat{C})$$

Where $\hat{C}$ is the set of clues given the that $\hat{t}$ is the target
word. In this way, we can estimate the _Entropy_ after the guess as:

$$H(\mathbb{E}(P(v | \tilde{C})))$$

Note that this is a Random Variable over $v$, since the expectation is over the
target words (and thus the clues, $\tilde{C}$).

In this way, we can select the next optimal guess by selecting the word that
reduces the most reduces the entropy after its guess.

## Implementation details

As a slight optimization, since the probabilities for each words at the start
(i.e. when there's not clues yet) is always the same, the optimal starting
word is always the same. Because of this, we pre-compute the optimal starts
for each language and add them to the `static/optimal_starts.json` file
so that they are not computed every time.

Additionally, note that at each step it's possible to guess all words in the
vocabulary since not only valid words can be optimal. To reduce the search
space in each step we group similar words together, and use those groups
to determine the words to evaluate in each iteration. These words are stored
in `static/groups_{LANGUAGE}.pickle` files as dictionaries mapping from the
keys (used to determine which subset of words to search over) to values
which are sets of similar words to the keys.

## Using the solver

To run the solver you can simply run:

```console
python main.py
```

This will prompt you with instructions about how to use the solver.
