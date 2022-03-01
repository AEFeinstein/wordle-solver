# wordle-solver
A Wordle-type game solver, written in Python.

## Usage

`wordle.py -g {GUESS_DICT} -s {SOLN_DICT}`

* `GUESS_DICT` - A text file containing all possible guesses to the game.
* `SOLN_DICT` - A text file containing all possible solutions to the game. This should be a subset of `GUESS_DICT` and may be the same file.

`wordle.py -l`

* The `-l` flag requires no arguments and will download a solution list specifically for the game Lewdle, which updates its word list with some frequency.

## Games

### Wordle

[`wordle-guesses.txt`](/wordle-guesses.txt) is a list of valid guesses for Wordle. They may not all be valid solutions.

[`wordle-solutions.txt`](/wordle-solutions.txt) is a list of valid guesses for Wordle. They may not all be valid solutions.

### Primel

[`primes.txt`](/primes.txt) is a list of five digit prime numbers to play [Primel](https://converged.yt/primel/).

### Lewdle

[`getLewdles.sh`](/getLewdles.sh) is a script to download the solution list for [Lewdle](https://www.lewdlegame.com/).