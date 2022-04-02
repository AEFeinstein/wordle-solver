# wordle-solver
A Wordle-type game solver, written in Python.

## Usage

`wordle.py -g {GUESS_DICT} -s {SOLN_DICT} -n {NUM_PUZZLES}`

* `GUESS_DICT` - A text file containing all possible guesses to the game.
* `SOLN_DICT` - A text file containing all possible solutions to the game. This should be a subset of `GUESS_DICT` and may be the same file.
* `NUM_PUZZLES` - The number of simultaneous puzzles to solve. One for [Wordle](https://www.nytimes.com/games/wordle/index.html), four for [Quordle](https://www.quordle.com), eight for [Octordle](https://octordle.com), or thirty two for [Duotrigordle](https://duotrigordle.com/).

`wordle.py -l`

* The `-l` flag requires no arguments and will download a solution list specifically for the game Lewdle, which updates its word list with some frequency.

To play, type in the word that the program recommends, then type in the result using `o` for a letter in the write place, `-` for a valid letter in the wrong spot, and `x` for an invalid letter. When solving simultaneous puzzles, use a space between results, like `xxoo- x-ox-` etc. 

## Games

### Wordle

[`wordle-guesses.txt`](/wordle-guesses.txt) is a list of valid guesses for Wordle. They may not all be valid solutions.

[`wordle-solutions.txt`](/wordle-solutions.txt) is a list of valid guesses for Wordle. They may not all be valid solutions.

### Primel

[`primes.txt`](/primes.txt) is a list of five digit prime numbers to play [Primel](https://converged.yt/primel/).

### Lewdle

[`getLewdles.sh`](/getLewdles.sh) is a script to download the solution list for [Lewdle](https://www.lewdlegame.com/).

## Auto Solvers

Sometimes typing in results for N-ordles can get cumbersome. [Selenium](https://selenium-python.readthedocs.io/) can be used to automate reading results from and inputting text to a browser.

[Octordle](https://octordle.com) can be solved by running [`auto-octordle.py`](/auto-octordle.py).

[Duotrigordle](https://duotrigordle.com/) can be solved by running [`auto-duotrigordle.py`](/auto-duotrigordle.py).
