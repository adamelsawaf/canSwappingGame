from random import choice
from sys    import exit
from time   import time

CLEAR_CONSOLE                           : str = "\033c\033[3J"
NORMAL_TEXT                             : str = "\033[0m"
BOLD_TEXT                               : str = "\033[1m"
ITALIC_TEXT                             : str = "\033[3m"
UNDERLINE_TEXT                          : str = "\033[4m"
RED_TEXT                                : str = "\033[38;2;255;0;0m"
GREEN_TEXT                              : str = "\033[38;2;0;255;0m"
HYPERLINK_TEXT                          : str = f"{UNDERLINE_TEXT}\033[38;2;51;102;204m"
RESTART_MESSAGE                         : str = f"{BOLD_TEXT}Restarting game...{NORMAL_TEXT}\n\n\n\n\n"
EXIT_MESSAGE                            : str = f"\n{BOLD_TEXT}Goodbye! Come play again sometime ;)\n{NORMAL_TEXT}{RED_TEXT}{ITALIC_TEXT}Exiting game...{NORMAL_TEXT}"

HELP_MESSAGE                            : str = f'''{UNDERLINE_TEXT}At any time{NORMAL_TEXT}:
Enter {BOLD_TEXT}/exit{NORMAL_TEXT} or press {BOLD_TEXT}ctrl + d{NORMAL_TEXT}, {BOLD_TEXT}ctrl + c{NORMAL_TEXT}, or {BOLD_TEXT}ctrl + z{NORMAL_TEXT} to exit the game.
Enter {BOLD_TEXT}/clear{NORMAL_TEXT} to clear the text off your screen (and show your list of cans again, if it's set up).
Capitalization and beginning/ending spaces of your inputs don't matter.
Short example video of real-life gameplay of this game (which inspired this program): {HYPERLINK_TEXT}https://www.youtube.com/shorts/TqLawfXbG9E{NORMAL_TEXT}
Enter {BOLD_TEXT}/restart{NORMAL_TEXT} to restart the game and show this message again.
Enter {BOLD_TEXT}/help{NORMAL_TEXT} to show this message again.'''

DEFAULT_NUMBER_OF_CANS                  : int = 7
DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS: int = 1



def canWithoutColor(can: str) -> str:
    return can[can.index("m") + 1: can.index("\033", 13)]


def initialCansList(length: int) -> list[str]:
    currentResultItem             : str       = chr(ord("A") - 1)
    currentColor                  : list[int] = [255, 0, 0]  #  RGB, starts out as red (ends with blue)
    currentColorIndex             : int       = 1
    currentColorIncrementDirection: int       = 1
    colorIncrementSpeed           : int       = (1020 // length) if(length != 0) else 0   #  (1020 = 4 * 255, bc 4 color changes are needed to create the full nice spectrum)
    resultCans                    : list[str] = []
    currentColor[currentColorIndex] -= currentColorIncrementDirection * colorIncrementSpeed

    for i in range(length):
        #  calculate the next can name
        j: int = len(currentResultItem) - 1
        while(currentResultItem[j:j+1] == "Z"):
            currentResultItem = currentResultItem[:j] + "A" + currentResultItem[j+1:]
            j -= 1
            if(j < 0):
                currentResultItem = "A" + currentResultItem
                break
        else:
            currentResultItem = currentResultItem[:j] + chr(ord(currentResultItem[j]) + 1) + currentResultItem[j+1:]

        #  calculate the next can color
        currentColor[currentColorIndex] += currentColorIncrementDirection * colorIncrementSpeed
        if(currentColor[currentColorIndex] >= 255):
            currentColor[currentColorIndex] = 255
            currentColorIndex = (currentColorIndex - 1) % 3
            currentColorIncrementDirection *= -1
        elif((currentColor[currentColorIndex] <= 0) and (i != 0)):
            currentColor[currentColorIndex] = 0
            currentColorIndex = (currentColorIndex - 1) % 3
            currentColorIncrementDirection *= -1
        
        resultCans.append(f"\033[38;2;{currentColor[0]};{currentColor[1]};{currentColor[2]}m{currentResultItem}{NORMAL_TEXT}")
    
    return resultCans


def printCansState_horizontal(cans: list[str]) -> None:
    #  The number of characters in the largest (final) index is necessarily at least as large as the number of characters in the longest can name,
    #  because it's base ten (indices) vs base twenty-six (can names), where the indices start at 1 and the can names start at "zero"
    #  (the difference of 1 isn't enough to make a difference for this).
    maxItemLength: int = len(str(len(cans)))

    print(f"{BOLD_TEXT}Position:{NORMAL_TEXT}  ", end="")
    for i in range(len(cans)):
        print(i+1, (maxItemLength - len(str(i+1)) + 2) * " ", sep="", end="")
    
    print(f"\n{BOLD_TEXT}Can     :{NORMAL_TEXT}  ", end="")
    for can in cans:
        print(can, (maxItemLength - len(canWithoutColor(can)) + 2) * " ", sep="", end="")
    
    print(NORMAL_TEXT)


def printCansState_vertical(cans: list[str]) -> None:
    #  The number of characters in the largest (final) index is necessarily at least as large as the number of characters in the longest can name,
    #  because it's base ten (indices) vs base twenty-six (can names), where the indices start at 1 and the can names start at "zero"
    #  (the difference of 1 isn't enough to make a difference for this).
    maxItemLength: int = len(str(len(cans)))
    
    print(f"{(maxItemLength - len("Position")) * " "}{BOLD_TEXT}Position  Can{NORMAL_TEXT}  ")
    for i in range(len(cans)):
        print((max(maxItemLength, len("Position")) - len(str(i+1))) * " ", i+1, "  ", cans[i], sep="")


def main() -> None:
    while(True):
        print(f"{BOLD_TEXT}{GREEN_TEXT}------------------------------------------------- Welcome to the Can Swapping Game! -------------------------------------------------{NORMAL_TEXT}\n{HELP_MESSAGE}\n\n")



        #  Collect the game parameters from the user:

        restart: bool = False

        try:
            numberOfCans: int = input(f"How many total cans would you like in the line? (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
        while(True):
            print(NORMAL_TEXT, end="")
            match numberOfCans:
                case "":
                    numberOfCans = DEFAULT_NUMBER_OF_CANS
                    break
                case "/clear":
                    print(f"Clearing console...{CLEAR_CONSOLE}", end="")
                    try:
                        numberOfCans = input(f"How many total cans would you like in the line? (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/restart":
                    print(RESTART_MESSAGE)
                    restart = True
                    break
                case "/exit":
                    exit(EXIT_MESSAGE)
                case "/help":
                    try:
                        numberOfCans = input(f"\n{HELP_MESSAGE}\n\nHow many total cans would you like in the line? (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/cindy":
                    try:
                        numberOfCans = input(f"{RED_TEXT}❤{NORMAL_TEXT}\nHow many total cans would you like in the line? (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/cancel":
                    try:
                        numberOfCans = input(f"There's nothing to cancel right now! Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nHow many total cans would you like in the line? (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "clear" | "restart" | "exit" | "help" | "cindy" | "cancel":
                    try:
                        numberOfCans = input(f"All commands must begin with a forward slash (\"/\"). Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nHow many total cans would you like in the line? (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
            if(numberOfCans[0] == "/"):
                try:
                    numberOfCans = input(f"Invalid command. Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nHow many total cans would you like in the line? (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                continue
            try:
                if((float((numberOfCans)) != int(float(numberOfCans))) or ((numberOfCans := int(float(numberOfCans))) < 0)):
                    numberOfCans = input(f"You must enter a non-negative whole number, please try again (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                    continue
                else:
                    break
            except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
            except ValueError:
                try:
                    numberOfCans = input(f"You must enter a non-negative whole number, please try again (default {DEFAULT_NUMBER_OF_CANS}): {BOLD_TEXT}").strip().lower()
                except(EOFError, KeyboardInterrupt):
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                continue
        if(restart):
            continue


        try:
            numberOfInitiallyCorrectCans: int = input(f"Great! How many cans would you like to be initially in their correct positions? (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
        while(True):
            print(NORMAL_TEXT, end="")
            match numberOfInitiallyCorrectCans:
                case "":
                    if(DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS > numberOfCans):
                        try:
                            numberOfInitiallyCorrectCans = input(f"You can't have more initially correct cans than total cans, please try again (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    elif(DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS == numberOfCans - 1):
                        try:
                            numberOfInitiallyCorrectCans = input(f"You can't have just one can in the wrong place, please try again (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    else:
                        numberOfInitiallyCorrectCans = DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS
                        break
                case "/clear":
                    print(f"Clearing console...{CLEAR_CONSOLE}", end="")
                    try:
                        numberOfInitiallyCorrectCans = input(f"How many cans would you like to be initially in their correct positions? (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/restart":
                    print(RESTART_MESSAGE)
                    restart = True
                    break
                case "/exit":
                    exit(EXIT_MESSAGE)
                case "/help":
                    try:
                        numberOfInitiallyCorrectCans = input(f"\n{HELP_MESSAGE}\n\nHow many cans would you like to be initially in their correct positions? (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/cindy":
                    try:
                        numberOfInitiallyCorrectCans = input(f"{RED_TEXT}❤{NORMAL_TEXT}\nHow many cans would you like to be initially in their correct positions? (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/cancel":
                    try:
                        numberOfInitiallyCorrectCans = input(f"There's nothing to cancel right now! Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nHow many cans would you like to be initially in their correct positions? (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "clear" | "restart" | "exit" | "help" | "cindy" | "cancel":
                    try:
                        numberOfInitiallyCorrectCans = input(f"All commands must begin with a forward slash (\"/\"). Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nHow many cans would you like to be initially in their correct positions? (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
            if(numberOfInitiallyCorrectCans[0] == "/"):
                try:
                    numberOfInitiallyCorrectCans = input(f"Invalid command. Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nHow many cans would you like to be initially in their correct positions? (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                continue
            try:
                if((float(numberOfInitiallyCorrectCans) != int(float(numberOfInitiallyCorrectCans))) or (int(float(numberOfInitiallyCorrectCans)) < 0)):
                    numberOfInitiallyCorrectCans = input(f"You must enter a non-negative whole number, please try again (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    continue
                elif(int(float(numberOfInitiallyCorrectCans)) > numberOfCans):
                    numberOfInitiallyCorrectCans = input(f"You can't have more initially correct cans than total cans, please try again (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    continue
                elif(int(float(numberOfInitiallyCorrectCans)) == numberOfCans - 1):
                    numberOfInitiallyCorrectCans = input(f"You can't have just one can in the wrong place, please try again (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                    continue
                else:
                    numberOfInitiallyCorrectCans = int(float(numberOfInitiallyCorrectCans))
                    break
            except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
            except ValueError:
                try:
                    numberOfInitiallyCorrectCans = input(f"You must enter a non-negative whole number, please try again (default {DEFAULT_NUMBER_OF_INITIALLY_CORRECT_CANS}): {BOLD_TEXT}").strip().lower()
                except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                continue
        if(restart):
            continue


        try:
            cansListPrinter = input(f"Great! Would you like your list of cans displayed vertically (recommended when you have a lot of cans)? (default - no [horizontal]): {BOLD_TEXT}").strip().lower()
        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
        while(True):
            print(NORMAL_TEXT, end="")
            match cansListPrinter:
                case "/clear":
                    print(f"Clearing console...{CLEAR_CONSOLE}", end="")
                    try:
                        cansListPrinter = input(f"Would you like your list of cans displayed vertically (recommended when you have a lot of cans)? (default - no [horizontal]): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/restart":
                    restart = True
                    print(RESTART_MESSAGE)
                    break
                case "/exit":
                    exit(EXIT_MESSAGE)
                case "/help":
                    try:
                        cansListPrinter = input(f"\n{HELP_MESSAGE}\n\nWould you like your list of cans displayed vertically (recommended when you have a lot of cans)? (default - no [horizontal]): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/cindy":
                    try:
                        cansListPrinter = input(f"{RED_TEXT}❤{NORMAL_TEXT}\nWould you like your list of cans displayed vertically (recommended when you have a lot of cans)? (default - no [horizontal]): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "/cancel":
                    try:
                        cansListPrinter = input(f"There's nothing to cancel right now! Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWould you like your list of cans displayed vertically (recommended when you have a lot of cans)? (default - no [horizontal]): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "clear" | "restart" | "exit" | "help" | "cindy" | "cancel":
                    try:
                        cansListPrinter = input(f"All commands must begin with a forward slash (\"/\"). Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWould you like your list of cans displayed vertically (recommended when you have a lot of cans)? (default - no [horizontal]): {BOLD_TEXT}").strip().lower()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                case "" | "no" | "n" | "horizontal" | "horizontally":
                    cansListPrinter = printCansState_horizontal
                    break
                case "yes" | "y" | "vertical" | "vertically":
                    cansListPrinter = printCansState_vertical
                    break
            if(cansListPrinter[0] == "/"):
                try:
                    cansListPrinter = input(f"Invalid command. Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWould you like your list of cans displayed vertically (recommended when you have a lot of cans)? (default - no [horizontal]): {BOLD_TEXT}").strip().lower()
                except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                continue
            else:
                try:
                    cansListPrinter = input(f"You must enter yes or no (or, y or n). Please try again: {BOLD_TEXT}").strip().lower()
                except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
        if(restart):
            continue


        #  Set up the game:
        
        print("Great! Setting up your game...\n")

        indicesTemp      : list[int] = list(range(numberOfCans))
        cansListReference: list[str] = initialCansList(numberOfCans)
        correctCansList  : list[str] = ["."] * numberOfCans

        for _i in range(numberOfInitiallyCorrectCans):
            randomIndex: int = choice(indicesTemp)
            indicesTemp.remove(randomIndex)
            correctCansList[randomIndex] = cansListReference[randomIndex]
        for i in range(numberOfCans - 2):
            if(len(indicesTemp) <= 2):  #  bc the last 2 elements could make it impossible to mismatch both (it would "get stuck" and throw an error)
                break
            if(correctCansList[i] != "."):
                continue
            else:
                randomIndex = choice([index for index in indicesTemp if(index != i)])
                indicesTemp.remove(randomIndex)
                correctCansList[i] = cansListReference[randomIndex]
        if(len(indicesTemp) == 2):
            i1: int = correctCansList.index(".")
            i2: int = correctCansList[i1 + 1:].index(".") + i1 + 1
            if(i1 in indicesTemp):
                correctCansList[i2] = cansListReference[i1]
                indicesTemp.remove(i1)
            elif(i2 in indicesTemp):
                correctCansList[i1] = cansListReference[i2]
                indicesTemp.remove(i2)
            else:
                randomIndex = choice(indicesTemp)
                correctCansList[i1] = cansListReference[randomIndex]
                indicesTemp.remove(randomIndex)
        if(len(indicesTemp) > 0):
            correctCansList[correctCansList.index(".")] = cansListReference[indicesTemp[0]]


        #  Main gameplay loop:
        
        currentCansList           : list[str] = cansListReference[:]
        currentNumberOfCorrectCans: int       = numberOfInitiallyCorrectCans
        swapCount                 : int       = 0
        print("Let's play!\n")
        print(f"{UNDERLINE_TEXT}Current cans state{NORMAL_TEXT}")
        cansListPrinter(currentCansList)
        if((numberOfCans == 0) and (cansListPrinter == printCansState_vertical)):
            print()
        print(f"Current number of correct cans: {BOLD_TEXT}{currentNumberOfCorrectCans}{NORMAL_TEXT} out of {numberOfCans}")
        gameStartTime: float = time()
        
        while(currentNumberOfCorrectCans != numberOfCans):
            currentCansList_colorless: list[str] = [canWithoutColor(can) for can in currentCansList]
            cancel                   : bool      = False
            try:
                can1: str | int = input(f"\nWhat is one can that you would like to swap? (Enter the can's name or position): {BOLD_TEXT}").strip().upper()
            except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
            while(True):
                print(NORMAL_TEXT, end="")
                match can1:
                    case "/CLEAR":
                        print(f"Clearing console...{CLEAR_CONSOLE}", end="")
                        print(f"{UNDERLINE_TEXT}Current cans state{NORMAL_TEXT}")
                        cansListPrinter(currentCansList)
                        print(f"Current number of correct cans: {BOLD_TEXT}{currentNumberOfCorrectCans}{NORMAL_TEXT} out of {numberOfCans}")
                        try:
                            can1 = input(f"\nWhat is one can that you would like to swap? (Enter the can's name or position): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    case "/RESTART":
                        restart = True
                        print(RESTART_MESSAGE)
                        break
                    case "/EXIT":
                        exit(EXIT_MESSAGE)
                    case "/HELP":
                        try:
                            can1 = input(f"\n{HELP_MESSAGE}\n\nWhat is one can that you would like to swap? (Enter the can's name or position): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    case "/CINDY":
                        try:
                            can1 = input(f"{RED_TEXT}❤{NORMAL_TEXT}\nWhat is one can that you would like to swap? (Enter the can's name or position): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    case "/CANCEL":
                        try:
                            can1 = input(f"There's nothing to cancel right now! Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWhat is one can that you would like to swap? (Enter the can's name or position): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                if(can1[:1] == "/"):
                    try:
                        can1 = input(f"Invalid command. Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWhat is one can that you would like to swap? (Enter the can's name or position): {BOLD_TEXT}").strip().upper()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                elif(can1 in currentCansList_colorless):
                    break
                elif(can1 in ["CLEAR", "RESTART", "EXIT", "HELP", "CINDY", "CANCEL"]):
                    try:
                        can1 = input(f"All commands must begin with a forward slash (\"/\"). Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWhat is one can that you would like to swap? (Enter the can's name or position): {BOLD_TEXT}").strip().upper()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                try:  #  can1 is an index, or invalid
                    if( (float(can1) == int(float(can1))) and ((can1 := int(float(can1)) - 1) in range(numberOfCans)) ):
                        break
                    else:
                        can1 = input(f"You must enter a valid can (the can's name or index) to swap, please try again: {BOLD_TEXT}").strip().upper()
                except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                except ValueError:
                    try:
                        can1 = input(f"You must enter a valid can (the can's name or index) to swap, please try again: {BOLD_TEXT}").strip().upper()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
            if(restart):
                break
            

            try:
                can2: str | int = input(f"Great! What is the other can that you would like to swap? (Enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
            except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
            while(True):
                print(NORMAL_TEXT, end="")
                match can2:
                    case "/CLEAR":
                        print(f"Clearing console...{CLEAR_CONSOLE}", end="")
                        print(f"{UNDERLINE_TEXT}Current cans state{NORMAL_TEXT}")
                        cansListPrinter(currentCansList)
                        print(f"Current number of correct cans: {BOLD_TEXT}{currentNumberOfCorrectCans}{NORMAL_TEXT} out of {numberOfCans}")
                        try:
                            can2 = input(f"\nWhat is the other can that you would like to swap? (Enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    case "/CANCEL":
                        cancel = True
                        print(f"\n{UNDERLINE_TEXT}Current cans state{NORMAL_TEXT}")
                        cansListPrinter(currentCansList)
                        print(f"Current number of correct cans: {BOLD_TEXT}{currentNumberOfCorrectCans}{NORMAL_TEXT} out of {numberOfCans}")
                        break
                    case "/RESTART":
                        restart = True
                        print(RESTART_MESSAGE)
                        break
                    case "/EXIT":
                        exit(EXIT_MESSAGE)
                    case "/HELP":
                        try:
                            can2 = input(f"\n{HELP_MESSAGE}\n\nWhat is the other can that you would like to swap? (Enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    case "/CINDY":
                        try:
                            can2 = input(f"{RED_TEXT}❤{NORMAL_TEXT}\nWhat is the other can that you would like to swap? (Enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                if(can2[:1] == "/"):
                    try:
                        can2 = input(f"Invalid command. Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWhat is the other can that you would like to swap? (Enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                if(can2 in currentCansList_colorless):
                    if((can2 == can1)):
                        try:
                            can2 = input(f"You must enter a different can than the one you entered just before (can {currentCansList[currentCansList_colorless.index(can2)]} at position {currentCansList_colorless.index(can2) + 1}), please try again\n(enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    elif((type(can1) == int) and (can2 == currentCansList_colorless[can1])):
                        try:
                            can2 = input(f"You must enter a different can than the one you entered just before (can {currentCansList[can1]} at position {can1 + 1}), please try again\n(enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                        except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                            exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                        continue
                    else:
                        break
                elif(can2 in ["CLEAR", "RESTART", "EXIT", "HELP", "CINDY", "CANCEL"]):
                    try:
                        can2 = input(f"All commands must begin with a forward slash (\"/\"). Enter {BOLD_TEXT}/help{NORMAL_TEXT} to view the list of valid commands.\nWhat is the other can that you would like to swap? (Enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                try:  #  can2 is an index, or invalid
                    if( (float(can2) == int(float(can2))) and ((can2 := int(float(can2)) - 1) in range(numberOfCans)) ):
                        if(can2 == can1):  #  can1 is also an index
                            can2 = input(f"You must enter a different can than the one you entered just before (can {currentCansList[can2]} at position {can2 + 1}), please try again\n(enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                            continue
                        elif(currentCansList_colorless[can2] == can1):  #  can1 is a can name
                            can2 = input(f"You must enter a different can than the one you entered just before (can {currentCansList[can2]} at position {currentCansList_colorless.index(can1) + 1}),\nplease try again (enter the can's name or position, or {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                            continue
                        else:
                            break
                    else:
                        can2 = input(f"You must enter a valid can (the can's name or position) to swap, please try again (or enter {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                        continue
                except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                    exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                except ValueError:
                    try:
                        can2 = input(f"You must enter a valid can (the can's name or position) to swap, please try again (or enter {BOLD_TEXT}/cancel{NORMAL_TEXT} to cancel your previous can): {BOLD_TEXT}").strip().upper()
                    except(EOFError, KeyboardInterrupt):  #  catches ctrl+d or ctrl+c
                        exit(f"{NORMAL_TEXT}\n{EXIT_MESSAGE}")
                    continue
                break
            if(cancel):
                continue
            if(restart):
                break

            #  perform the can swap
            if(type(can1) == str):
                can1 = currentCansList_colorless.index(can1)
            if(type(can2) == str):
                can2 = currentCansList_colorless.index(can2)
            currentCansList[can1], currentCansList[can2] = currentCansList[can2], currentCansList[can1]
            swapCount += 1
            print(f"\nSwapped cans {currentCansList[can2]} ({can1 + 1}) and {currentCansList[can1]} ({can2 + 1}).\n")

            currentNumberOfCorrectCans = sum([1 if(currentCansList[i] == correctCansList[i]) else 0 for i in range(numberOfCans)])
            print(f"{UNDERLINE_TEXT}Current cans state{NORMAL_TEXT}")
            cansListPrinter(currentCansList)
            print(f"Current number of correct cans: {BOLD_TEXT}{currentNumberOfCorrectCans}{NORMAL_TEXT} out of {numberOfCans}")

            if(currentNumberOfCorrectCans != numberOfCans):
                print("\nNext swap.", end="")

        gameEndTime: float = time()
        if(not restart):
            break


    print(f'''{BOLD_TEXT}{GREEN_TEXT}\nAll cans are in their correct spots. Congratulations, you win! 🙌
You made a total of {UNDERLINE_TEXT}{swapCount} swaps{NORMAL_TEXT}.
{BOLD_TEXT}{GREEN_TEXT}You took a total of {UNDERLINE_TEXT}{"{:f}".format(gameEndTime - gameStartTime)} seconds{NORMAL_TEXT}.
{ITALIC_TEXT}Thanks for playing!
Screenshot or copy-paste the above text to save and share your results with others!
Play again to try to beat your high score? :D{NORMAL_TEXT}''')




if __name__ == "__main__":
    main()
