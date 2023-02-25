from string import ascii_lowercase
from string import digits
import getopt, sys
import os
import json

###############################################################################


class wordleChar:
    def __init__(self, location: "int", char: "str"):
        """TODO

        Args:
            location (int): _description_
            char (str): _description_
        """
        self.ch = char
        self.loc = location

    def __eq__(self, __o: object) -> bool:
        """TODO

        Args:
            __o (object): _description_

        Returns:
            bool: _description_
        """
        return (self.ch == __o.ch) and (self.loc == __o.loc)


class wordlePuzzle:
    def __init__(self, solutions: "list[str]", guesses: "list[str]", isAlpha: "bool"):
        """TODO

        Args:
            solutions (list[str]): _description_
            guesses (list[str]): _description_
            isAlpha (bool): _description_
        """
        self.wordleSolns: "list[str]" = solutions.copy()
        self.wordleGuesses: "list[str]" = guesses.copy()
        self.isAlpha: "bool" = isAlpha

        # Data from the results of guesses
        self.okChars: "list[wordleChar]" = []
        self.badChars: "list[str]" = []
        self.placedChars: "list[wordleChar]" = []

        self.isSolved: "bool" = False

    def processResult(self, wordleGuessed: "str", result: "str") -> "None":
        """TODO

        Args:
            wordleGuessed (str): _description_
            result (str): _description_
        """

        if "ooooo" == result:
            self.isSolved = True
            return

        # Append the input to the known data
        for resIdx in range(len(result)):
            if "x" == result[resIdx]:
                chIsOk = False
                for okc in self.okChars:
                    if okc.ch == wordleGuessed[resIdx]:
                        chIsOk = True
                for pc in self.placedChars:
                    if pc.ch == wordleGuessed[resIdx] and pc.loc == resIdx:
                        chIsOk = True
                if not chIsOk:
                    # This char definitely isn't in the word
                    if wordleGuessed[resIdx] not in self.badChars:
                        self.badChars.append(wordleGuessed[resIdx])
                        list.sort(self.badChars)
            elif "-" == result[resIdx]:
                # This char is in the word... somewhere...
                wc: "wordleChar" = wordleChar(resIdx, wordleGuessed[resIdx])
                if(wc not in self.okChars):
                    self.okChars.append(wc)
            elif "o" == result[resIdx]:
                # This char is in the right place!
                wc: "wordleChar" = wordleChar(resIdx, wordleGuessed[resIdx])
                if wc not in self.placedChars:
                    self.placedChars.append(wc)
                # Make sure that placed chars are removed from the 'ok' list
                for okc in list(self.okChars):
                    if okc.ch == wordleGuessed[resIdx]:
                        self.okChars.remove(okc)

        # Find all valid remaining words
        self.wordleSolns = trimWordleDict(
            self.wordleSolns, self.badChars, self.okChars, self.placedChars
        )
        self.wordleGuesses = trimWordleDict(
            self.wordleGuesses, self.badChars, self.okChars, self.placedChars
        )


###############################################################################


def validateInput(numWordles: "int", input: "str") -> "bool":
    """Validates user input by making sure its a string of length 5 with xo- chars

    Also quits the program if the word is solved

    Args:
        numWordles (int): The number of wordle puzzles
        input (str): The user input

    Returns:
        bool: True if valid, False otherwise
    """

    # Validate length
    if ((5 * numWordles) + (numWordles - 1)) != len(input):
        return False, False

    # Validate chars
    allSolved: "bool" = True
    for i in range(len(input)):
        if (
            (input[i] != "x")
            and (input[i] != "o")
            and (input[i] != "-")
            and (input[i] != " ")
        ):
            return False, False
        elif (input[i] == "x") or (input[i] == "-"):
            allSolved = False

    # Input is valid
    return True, allSolved


def histogramFromPuzzles(puzzles: "list[wordlePuzzle]") -> "dict[float]":
    """Create a histogram of letter occurrences in words

    Args:
        setOfWords (list[str]): A set of words to create a histogram of

    Returns:
        list[charProb]: A list of chars and their probability of occuring in a
                        word
    """

    # Initialize the histogram
    totalHistogram: "dict[float]" = {}
    if puzzles[0].isAlpha:
        for ch in ascii_lowercase:
            totalHistogram[ch] = 0.0
    else:
        for ch in digits:
            totalHistogram[ch] = 0.0

    # For each word
    totalNumWords: "int" = 0
    puzzle: "wordlePuzzle"
    for puzzle in puzzles:
        for word in puzzle.wordleSolns:
            # Make a histogram of the chars in that word
            wordHistogram = {}
            for i in range(len(word)):
                wordHistogram[word[i]] = True
            # For each unique char in the word
            for ch in wordHistogram.keys():
                if wordHistogram[ch]:
                    # Add one to the total histogram
                    totalHistogram[ch] = totalHistogram[ch] + 1
        totalNumWords = totalNumWords + len(puzzle.wordleSolns)

    # Normalize
    for key in totalHistogram.keys():
        totalHistogram[key] = totalHistogram[key] / totalNumWords

    return totalHistogram


def wordValue(word: "str", histogram: "dict[int]") -> "int":
    """Compute the value of a word by summing the values of the chars from a
    probability histogram. A lower number means the word better bisects the set
    of remaining words

    Args:
        word (str): The word to find a value for
        histogram (list[charProb]): The histogram with values per-char

    Returns:
        int: The value of the word
    """
    guessedLetters: "list[str]" = []
    val: "int" = 0
    for ch in word:
        # Ignore letters that are already known one way or the other
        if 0 != histogram[ch] and 1 != histogram[ch]:
            # If a letter was guessed in the word already, treat it as a 1
            # (bad guess)
            if ch in guessedLetters:
                val = val + 1
            else:
                # Score each letter by how close it is to 0.5 probability
                val = val + abs(0.5 - histogram[ch])
                guessedLetters.append(ch)

    return val


def wordContainsUniqueLetters(word: "str", dictIsAlpha: "bool") -> "bool":
    """Check if a word contains only unique letters

    Args:
        word (str): The word to check for letter uniqueness

    Returns:
        bool: True if the word contains unique letters, False otherwise
    """
    if dictIsAlpha:
        lettersInWord: "list[int]" = [0] * len(ascii_lowercase)
    else:
        lettersInWord: "list[int]" = [0] * len(digits)

    for char in word:
        if dictIsAlpha:
            idx: "int" = ord(char) - ord("a")
        else:
            idx: "int" = ord(char) - ord("0")
        lettersInWord[idx] = lettersInWord[idx] + 1
    for charCount in lettersInWord:
        if charCount > 1:
            return False
    return True


def trimWordleDict(
    wordles: "list[str]",
    badChars: "list[str]",
    okChars: "list[wordleChar]",
    placedChars: "list[wordleChar]",
) -> "list[str]":
    """Trim a dictionary given a list of chars not in the word, chars somewhere
    in the word, and chars definitely in a given location

    Args:
        wordles (list[str]): The list of wordles to trim
        badChars (list[str]): A list of chars which do not appear in the solution
        okChars (list[wordleChar]): A list of chars that appear in the solution
        not at the given index
        placedChars (list[wordleChar]): A list of chars that appear in the
        solution at the given index
    """
    validWordles: "list[str]" = []
    word: "str"
    for word in wordles:
        valid: "bool" = True

        # Make sure the word doesn't contain these chars, unless already placed
        for badc in badChars:
            wordIdx = 0
            # For each char in the word
            for wordc in word:
                # If the bad character is in the word
                if badc == wordc:
                    # Check if the bad character is already a placed character
                    isPlaced = False
                    for plc in placedChars:
                        if plc.ch == badc and plc.loc == wordIdx:
                            isPlaced = True
                    if not isPlaced:
                        valid = False
                wordIdx = wordIdx + 1
        if not valid:
            continue

        # Make sure the word does contain these chars NOT in their location
        for okc in okChars:
            if (okc.ch not in word) or (word[okc.loc] == okc.ch):
                valid = False
        if not valid:
            continue

        # Make sure the word contains these chars in their location
        for plc in placedChars:
            if word[plc.loc] != plc.ch:
                valid = False
        if not valid:
            continue

        # Found a valid word, add it to the list
        if valid:
            validWordles.append(word)

    # Replace old wordles with only valid words
    return validWordles


###############################################################################

class wordleSolver:
    def __init__(self, solnDictFileName: "str", guessDictFileName: "str", numWordles: "int", downloadLewdles: "bool") -> None:
        """TODO

        Args:
            solnDictFileName (str): _description_
            guessDictFileName (str): _description_
            numWordles (int): _description_
            downloadLewdles (bool): _description_
        """

        self.numWordles: "int" = numWordles
        self.solnLines: "list[str]"
        self.guessLines: "list[str]"
        if downloadLewdles:
            solnLines = json.loads(os.popen("bash .\getLewdles.sh").read())["data"][
                "listDicts"
            ]["items"][0]["LewdWords"][0].split(",")
            guessLines = solnLines
        else:
            with open(solnDictFileName) as f:
                solnLines = f.readlines()
            with open(guessDictFileName) as f:
                guessLines = f.readlines()

        # Get a list of five letter words
        self.initWordleSolns: "list[str]" = []
        self.initWordleGuesses: "list[str]" = []
        line: "str"
        for line in solnLines:
            line = line.strip().lower()
            if 5 == len(line):
                self.initWordleSolns.append(line)
        for line in guessLines:
            line = line.strip().lower()
            if 5 == len(line):
                self.initWordleGuesses.append(line)

        # Make sure all solutions are in the guesses list too
        for word in self.initWordleSolns:
            if word not in self.initWordleGuesses:
                self.initWordleGuesses.append(word)

        # Check if we should use digits or chars
        self.dictIsAlpha: "bool" = True
        if self.initWordleSolns[0].isnumeric():
            self.dictIsAlpha = False

        # Create an array of wordle puzzles
        self.puzzles: "list[wordlePuzzle]" = []
        for i in range(numWordles):
            self.puzzles.append(wordlePuzzle(self.initWordleSolns, self.initWordleSolns, self.dictIsAlpha))

        # Find the best starting word
        charHist: "dict[float]" = histogramFromPuzzles(self.puzzles)

        # for key in charHist.keys():
        #     print(key + " " + str(charHist.get(key)))

        self.initWordleGuesses.sort(key=lambda word: wordValue(word, charHist))
        self.bestStarter: "str" = self.initWordleGuesses[0].lower()

        # Track the last guessed word
        self.wordleGuessed: "str" = self.bestStarter

        # Iterate until the word is guessed
        self.wordleSolved: "bool" = False
        self.round: "int" = 0
        self.puzzleFocus: "int" = 0

    def getNextWord(self) -> "str":
        """TODO

        Returns:
            str: _description_
        """
        return self.wordleGuessed

    def inputResult(self, allResults: "str"):
        """TODO

        Args:
            allResults (str): _description_
        """
        # Get input from the user
        resultIsValid: "bool" = False
        while not resultIsValid:
            
            (resultIsValid, self.wordleSolved) = validateInput(self.numWordles, allResults)
            if not resultIsValid:
                print(
                    "String must be the right length, made up of 'x', 'o', '-', and ' '"
                )

        # If the puzzle is solved, return
        if(self.wordleSolved):
            return

        # Process each puzzle's result
        resIdx: "int" = 0
        puzzle: "wordlePuzzle"
        smallestSolutionsSet: "int" = 1000000
        for puzzle in self.puzzles:
            # Get this puzzle's result from the total string
            result: "str" = allResults[resIdx : resIdx + 5]
            resIdx = resIdx + 6
            # Process the result
            if not puzzle.isSolved:
                puzzle.processResult(self.wordleGuessed, result)

                # TODO this sequential strategy works pretty well
                # if puzzle.isSolved:
                #     self.puzzleFocus = self.puzzleFocus + 1

            # TODO this focused strategy works less good
            # Save the puzzle with the smallest number of possible solutions to focus on
            if (not puzzle.isSolved) and (0 < len(puzzle.wordleSolns)) and (len(puzzle.wordleSolns) < smallestSolutionsSet):
                smallestSolutionsSet = len(puzzle.wordleSolns)
                self.puzzleFocus = self.puzzles.index(puzzle)

        # If this is the first two rounds, pick from all possible guesses
        # For round 3 and later, only pick from the possible solutions
        wordlesToPickFrom: "list[str]"
        if self.round < 1:
            # Calculate a histogram of letters in valid wordles in the focused puzzle
            charHistogram: "dict[int]" = histogramFromPuzzles([self.puzzles[self.puzzleFocus]])

            # Debug print all character probabilites
            # for ch in charHistogram.keys():
            #     print(str(ch) + " - " + str(charHistogram[ch]))

            # Sort all valid wordles by how well they bisect the set
            self.puzzles[self.puzzleFocus].wordleGuesses.sort(
                key=lambda word: wordValue(word, charHistogram)
            )
            wordlesToPickFrom = self.puzzles[self.puzzleFocus].wordleGuesses

        else:
            # Calculate a histogram of letters in valid wordles in the focused puzzle
            charHistogram: "dict[int]" = histogramFromPuzzles([self.puzzles[self.puzzleFocus]])

            # Sort all valid wordles by how well they bisect the set
            self.puzzles[self.puzzleFocus].wordleSolns.sort(
                key=lambda word: wordValue(word, charHistogram)
            )
            wordlesToPickFrom = self.puzzles[self.puzzleFocus].wordleSolns

        # Try guessing the word that best bisects the remaining set
        wordlePicked: "bool" = False
        for word in wordlesToPickFrom:
            if wordContainsUniqueLetters(word, self.dictIsAlpha):
                self.wordleGuessed = word.lower()
                wordlePicked = True
                break

        # Gotta pick a word with non-unique characters
        if not wordlePicked:
            self.wordleGuessed = wordlesToPickFrom[0].lower()

        # Make sure to not guess this again
        puzzle: "wordlePuzzle"
        for puzzle in self.puzzles:
            if self.wordleGuessed in puzzle.wordleSolns:
                puzzle.wordleSolns.remove(self.wordleGuessed)
            if self.wordleGuessed in puzzle.wordleGuesses:
                puzzle.wordleGuesses.remove(self.wordleGuessed)

        # Move to the next round
        self.round = self.round + 1

###############################################################################

def main():
    """TODO
    """
    # Assume the ospd4 dictionary by default
    solnDictFileName: "str" = "wordle-solutions.txt"
    guessDictFileName: "str" = "wordle-guesses.txt"
    downloadLewdles: "bool" = False
    numWordles: "int" = 1

    # Read the arguments to see if a different dictionary should be used
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "s:g:n:l", ["solutions", "guesses", "numPuzzles", "lewdle"]
        )
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for o, a in opts:
        if o in ("-s", "--solutions"):
            solnDictFileName = a
        elif o in ("-g", "--guesses"):
            guessDictFileName = a
        elif o in ("-n", "--numPuzzles"):
            numWordles = int(a)
        elif o in ("-l", "--lewdle"):
            downloadLewdles = True
        else:
            assert False, "unhandled option"

    print("Start with the given word. What was the result? Use 'o' for a")
    print("letter in the right spot, '-' for a letter in the wrong spot, and")
    print("'x' for a bad letter")

    ws = wordleSolver(solnDictFileName, guessDictFileName, numWordles, downloadLewdles)
    while not ws.wordleSolved:
        print("Try " + ws.getNextWord())
        ws.inputResult(input())


if __name__ == "__main__":
    main()
