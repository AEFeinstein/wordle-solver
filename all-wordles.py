from operator import contains
from unittest import result
from wordle import wordleSolver

debug: bool = True

totalNumGuesses: float = 0
totalNumPuzzles: float = 0

# with open('wordle-solutions.txt') as f:
with open('unsolveables.txt') as f:
    solnLines = f.readlines()

for soln in solnLines:
    soln = soln.strip()
    ws = wordleSolver("wordle-solutions.txt", "wordle-guesses.txt", 1, False)
    numGuesses: int = 0

    if debug:
        print(soln)

    while not ws.wordleSolved:
        # Get the next guess
        guess: str = ws.getNextWord()
        numGuesses = numGuesses + 1
        # Compare it to the solution, build a result string
        resultStr: str = ''
        for resIdx in range(len(soln)):
            if guess[resIdx] == soln[resIdx]:
                resultStr = resultStr + 'o'
            elif guess[resIdx] in soln:
                resultStr = resultStr + '-'
            else:
                resultStr = resultStr + 'x'

        if debug:
            print(guess + " " + resultStr)
        
        # Input the result string
        ws.inputResult(resultStr)

    if debug:
        print(soln + "\t" + str(numGuesses))

    # if numGuesses > 6:
    #     print("Unsolveable: " + soln)
    
    totalNumGuesses = totalNumGuesses + numGuesses
    totalNumPuzzles = totalNumPuzzles + 1

    # print(str(totalNumPuzzles) + ": " + str(totalNumGuesses / totalNumPuzzles))

    print('')