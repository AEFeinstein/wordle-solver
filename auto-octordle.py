from ast import arg
from operator import le
from numpy import empty
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import re
import subprocess

from wordle import wordleSolver

ws = wordleSolver("wordle-solutions.txt", "wordle-guesses.txt", 8, False)

driver = webdriver.Firefox()
driver.get("https://octordle.com/?mode=daily")
puzzleTables: "list[str]" = [
    "box-holder-1",
    "box-holder-2",
    "box-holder-3",
    "box-holder-4",
    "box-holder-5",
    "box-holder-6",
    "box-holder-7",
    "box-holder-8",
]

rowToRead: int = 0

bodyElem: WebElement = driver.find_element_by_tag_name("body")

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
        tableElem = driver.find_element_by_id(tableName)
        # For each row
        for rowElem in tableElem.find_elements_by_tag_name("tr"):
            # If this is the row to read
            if rowIdx == rowToRead:
                # For each letter
                for letterElem in rowElem.find_elements_by_tag_name("td"):
                    # Get the letter and style
                    style: "str" = letterElem.get_attribute("style")
                    letter: "str" = letterElem.text
                    
                    # extract RGB
                    m = re.search( "color: [A-Za-z]+; background-color: rgb\((\d+), (\d+), (\d+)\);", style)
                    r: "int" = int(m.group(1))
                    g: "int" = int(m.group(2))
                    b: "int" = int(m.group(3))

                    # Turn RGB into the result string
                    if letter == '':
                        resultStr = resultStr + "o"
                    elif r == 24 and g == 26 and b == 27:
                        resultStr = resultStr + "x"
                    elif r == 255 and g == 204 and b == 0:
                        resultStr = resultStr + "-"
                    elif r == 0 and g == 204 and b == 136:
                        resultStr = resultStr + "o"
                    else:
                        print("Real problem")
                        exit()
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
