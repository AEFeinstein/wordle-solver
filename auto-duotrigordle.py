from math import ceil
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import re

from wordle import wordleSolver

ws = wordleSolver("wordle-solutions.txt", "wordle-guesses.txt", 32, False)

driver = webdriver.Firefox()
driver.get("https://duotrigordle.com/")

rowToRead: int = 0

bodyElem: WebElement = driver.find_element_by_tag_name("body")

while not ws.wordleSolved:
    # Try the next word
    bodyElem.send_keys(ws.getNextWord())
    bodyElem.send_keys(Keys.RETURN)

    # Read the result from the page
    tableElem: "WebElement"
    rowElem: "WebElement"
    cellElem: "WebElement"
    resultStr: "str" = ""
    # For each puzzle table
    for tableElem in driver.find_elements_by_class_name("board"):
        rowIdx: int = 0
        cellIdx: int = 0
        # For each cell
        for cellElem in tableElem.find_elements_by_class_name("cell"):
            # If this is the row to read
            if (rowToRead == rowIdx):
                # Read out the colors
                if '' == cellElem.text:
                    resultStr = resultStr + 'o'
                elif "yellow" in cellElem.get_attribute("class"):
                    resultStr = resultStr + '-'
                elif "green" in cellElem.get_attribute("class"):
                    resultStr = resultStr + 'o'
                else:
                    resultStr = resultStr + 'x'

            # Count cells
            cellIdx = cellIdx + 1
            # Every five cells is a row
            if (5 == cellIdx):
                if (rowToRead == rowIdx):
                    # Move to the next table
                    resultStr = resultStr + " "
                    break
                else:
                    cellIdx = 0
                    rowIdx = rowIdx + 1

    # Move down one row, globally
    rowToRead = rowToRead + 1
    # Feed the results to the solver
    ws.inputResult(resultStr[:len(resultStr)-1])

# Copy scores or whatever
print("All solved. Press enter to exit.")
input()

# All done
driver.close()
