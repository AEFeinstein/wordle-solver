from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import re

from wordle import wordleSolver

ws = wordleSolver("wordle-solutions.txt", "wordle-guesses.txt", 8, False)

driver = webdriver.Firefox()
driver.get("https://octordle.com/daily")
puzzleTables: "list[str]" = [
    "board-1",
    "board-2",
    "board-3",
    "board-4",
    "board-5",
    "board-6",
    "board-7",
    "board-8",
]

rowToRead: int = 0

bodyElem: WebElement = driver.find_element("tag name", "body")

while not ws.wordleSolved:
    # Try the next word
    bodyElem.send_keys(ws.getNextWord())
    bodyElem.send_keys(Keys.RETURN)

    # Read the result from the page
    tableElem: "WebElement"
    rowElem: "WebElement"
    letterElem: "WebElement"
    resultStr: "str" = ""
    # For each puzzle table
    for tableName in puzzleTables:
        rowIdx: int = 0
        tableElem = driver.find_element("id", tableName)
        # For each row
        for rowElem in tableElem.find_elements("class name", "board-row"):
            # If this is the row to read
            if rowIdx == rowToRead:
                # For each letter
                for letterElem in rowElem.find_elements("class name", "letter"):
                    # Get the letter and style
                    _class: "str" = letterElem.get_attribute("class")
                    letter: "str" = letterElem.text

                    if letter == '':
                        resultStr = resultStr + "o"
                    elif "exact-match" in _class:
                        resultStr = resultStr + "o"
                    elif "word-match" in _class:
                        resultStr = resultStr + "-"
                    else:
                        resultStr = resultStr + "x"
                break
            # Move to the next row
            rowIdx = rowIdx + 1
        # Move to the next table
        resultStr = resultStr + " "

    # Move down one row, globally
    rowToRead = rowToRead + 1
    # Feed the results to the solver
    ws.inputResult(resultStr[:len(resultStr)-1])

# Copy scores or whatever
print("All solved. Press enter to exit.")
input()

# All done
driver.close()
