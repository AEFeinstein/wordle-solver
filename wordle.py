from string import ascii_lowercase
from string import digits
import getopt, sys
import os
import json

###############################################################################


class wordleChar:
    def __init__(self, location: "int", char: "str"):
        self.ch = char
        self.loc = location


###############################################################################


def validateInput(input: "str") -> bool:
    """Validates user input by making sure its a string of length 5 with xo- chars

    Also quits the program if the word is solved

    Args:
        input (str): The user input

    Returns:
        bool: True if valid, False otherwise
    """

    # Validate length
    if 5 != len(input):
        return False

    # Validate chars
    for i in range(len(input)):
        if (input[i] != "x") and (input[i] != "o") and (input[i] != "-"):
            return False

    # Check for a solve
    if "ooooo" == input:
        print("Got it!")
        exit()

    # Input is valid
    return True


def histogramFromSet(setOfWords: "list[str]", dictIsAlpha: "bool") -> "dict[float]":
    """Create a histogram of letter occurrences in words

    Args:
        setOfWords (list[str]): A set of words to create a histogram of

    Returns:
        list[charProb]: A list of chars and their probability of occuring in a
                        word
    """

    # Initialize the histogram
    totalHistogram: "dict[float]" = {}
    if dictIsAlpha:
        for ch in ascii_lowercase:
            totalHistogram[ch] = 0.0
    else:
        for ch in digits:
            totalHistogram[ch] = 0.0

    # For each word
    for word in setOfWords:
        # Make a histogram of the chars in that word
        wordHistogram = {}
        for i in range(len(word)):
            wordHistogram[word[i]] = True
        # For each unique char in the word
        for ch in wordHistogram.keys():
            if wordHistogram[ch]:
                # Add one to the total histogram
                totalHistogram[ch] = totalHistogram[ch] + 1

    # Normalize
    for key in totalHistogram.keys():
        totalHistogram[key] = totalHistogram[key] / len(setOfWords)

    return totalHistogram


def wordValue(word: "str", histogram: "dict[int]") -> int:
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


def wordContainsUniqueLetters(word: "str", dictIsAlpha: "bool") -> bool:
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
    badChars: "str",
    okChars: "list[wordleChar]",
    placedChars: "list[wordleChar]",
) -> None:
    """Trim a dictionary given a list of chars not in the word, chars somewhere
    in the word, and chars definitely in a given location

    Args:
        wordles (list[str]): The list of wordles to trim
        badChars (str): A list of chars which do not appear in the solution
        okChars (list[wordleChar]): A list of chars that appear in the solution
        not at the given index
        placedChars (list[wordleChar]): A list of chars that appear in the
        solution at the given index
    """
    validWordles: "list[str]" = []
    word: "str"
    for word in wordles:
        valid: "bool" = True

        # Make sure the word doesn't contain these chars
        for badc in badChars:
            if badc in word:
                valid = False
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
    wordles.clear()
    wordles.extend(validWordles)


###############################################################################


def main():
    # Assume the ospd4 dictionary by default
    solnDictFileName: "str" = "wordle-solutions.txt"
    guessDictFileName: "str" = "wordle-guesses.txt"
    downloadLewdles: "bool" = False

    # Read the arguments to see if a different dictionary should be used
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], ":s:g:l", ["solutions", "guesses", "lewdle"]
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
        elif o in ("-l", "--lewdle"):
            downloadLewdles = True
        else:
            assert False, "unhandled option"

    solnLines: "list[str]"
    guessLines: "list[str]"
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
    wordleSolns: "list[str]" = []
    wordleGuesses: "list[str]" = []
    line: "str"
    for line in solnLines:
        line = line.strip().lower()
        if 5 == len(line):
            wordleSolns.append(line)
    for line in guessLines:
        line = line.strip().lower()
        if 5 == len(line):
            wordleGuesses.append(line)

    # Check if we should use digits or chars
    dictIsAlpha: "bool" = True
    if wordleSolns[0].isnumeric():
        dictIsAlpha = False

    # Find the best starting word
    charHist: "dict[float]" = histogramFromSet(wordleSolns, dictIsAlpha)

    # for key in charHist.keys():
    #     print(key + " " + str(charHist.get(key)))

    wordleGuesses.sort(key=lambda word: wordValue(word, charHist))
    bestStarter: "str" = wordleGuesses[0].lower()

    # Tell the player how to start
    print("Start with " + bestStarter + ". What was the result? Use 'o' for a")
    print("letter in the right spot, '-' for a letter in the wrong spot, and")
    print("'x' for a bad letter")

    wordleGuessed: "str" = bestStarter

    # Data from the results of guesses
    okChars: "list[wordleChar]" = []
    badChars: "str" = []
    placedChars: "list[wordleChar]" = []

    # Iterate until the word is guessed
    wordleSolved: "bool" = False
    round: "int" = 1
    while not wordleSolved:

        # Get input from the user
        resultIsValid: "bool" = False
        while not resultIsValid:
            result: "str" = input()
            resultIsValid = validateInput(result)
            if not resultIsValid:
                print("String must be length 5, made up of 'x', 'o', and '-'")

        # Append the input to the known data
        for resIdx in range(len(result)):
            if "x" == result[resIdx]:
                chIsOk = False
                for okc in okChars:
                    if okc.ch == wordleGuessed[resIdx]:
                        chIsOk = True
                for pc in placedChars:
                    if pc.ch == wordleGuessed[resIdx]:
                        chIsOk = True
                if not chIsOk:
                    # This char definitely isn't in the word
                    badChars.append(wordleGuessed[resIdx])
            elif "-" == result[resIdx]:
                # This char is in the word... somewhere...
                okChars.append(wordleChar(resIdx, wordleGuessed[resIdx]))
            elif "o" == result[resIdx]:
                # This char is in the right place!
                placedChars.append(wordleChar(resIdx, wordleGuessed[resIdx]))
                # Make sure that placed chars are removed from the 'ok' list
                for okc in list(okChars):
                    if okc.ch == wordleGuessed[resIdx]:
                        okChars.remove(okc)

        # Find all valid remaining words
        trimWordleDict(wordleSolns, badChars, okChars, placedChars)
        trimWordleDict(wordleGuesses, badChars, okChars, placedChars)

        # Calculate a histogram of letters in valid wordles
        charHistogram: "dict[int]" = histogramFromSet(wordleSolns, dictIsAlpha)

        # Debug print all character probabilites
        # for ch in charHistogram.keys():
        #     print(str(ch) + " - " + str(charHistogram[ch]))

        # Sort all valid wordles by how well they bisect the set
        wordleSolns.sort(key=lambda word: wordValue(word, charHistogram))
        wordleGuesses.sort(key=lambda word: wordValue(word, charHistogram))

        # If this is the first two rounds, pick from all possible guesses
        # For round 3 and later, only pick from the possible solutions
        wordlesToPickFrom: "list[str]"
        if round < 2:
            wordlesToPickFrom = wordleGuesses
            print("Guessing from guesses")
        else:
            wordlesToPickFrom = wordleSolns
            print("Guessing from solutions")

        # Debug print all potential words
        # for word in wordles:
        #     print(" ? " + word)

        # Try guessing the word that best bisects the remaining set
        wordlePicked: "bool" = False
        for word in wordlesToPickFrom:
            if wordContainsUniqueLetters(word, dictIsAlpha):
                print("Try " + word.upper())
                wordleGuessed = word
                wordlePicked = True
                break
        # Gotta pick a word with non-unique characters
        if not wordlePicked:
            print("Try " + wordlesToPickFrom[0].upper())
            wordleGuessed = wordlesToPickFrom[0]

        # Make sure to not guess this again
        if wordleGuessed in wordleSolns:
            wordleSolns.remove(wordleGuessed)
        if wordleGuessed in wordleGuesses:
            wordleGuesses.remove(wordleGuessed)

        round = round + 1


if __name__ == "__main__":
    main()
