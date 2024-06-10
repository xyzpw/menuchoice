import curses
import re
import shutil
from . import _textHandler

KEYS_QUIT = [ord("q"), ord("Q")]

def getMenuComponents(menuString: str):
    menuLines = menuString.splitlines()
    for l in range(len(menuLines)):
        if re.search(r"^0.\s.*?(?=$|\s)", menuLines[l]) != None:
            meta = menuLines[:l] if l != 0 else None
            menuLines = menuLines[l:]
            break
    if meta != None:
        for i in range(meta.count("")):
            meta.pop(meta.index(""))
    return menuLines, meta

def rewriteMenu(menuString: str, menuArrow: str, currentMenuLine: int):
    menuLines = getMenuComponents(menuString)[0]
    menuLines[currentMenuLine] = "%s %s" % (menuArrow, menuLines[currentMenuLine])
    for i in range(len(menuLines)):
        if i != currentMenuLine:
            menuLines[i] = str(len(menuArrow) * " ") + " %s" % menuLines[i]
    return "\n".join(menuLines)

def cursorArrowMenu(stdscr, menuString: str, menuArrow: str, center: bool = False):
    curses.curs_set(0)
    curses.use_default_colors()
    currentLineIndex = 0
    stdscr.refresh()
    while True:
        stdscr.erase()
        stdscr.refresh()
        menuLines, menuMeta = getMenuComponents(menuString)
        rewrittenMenu = rewriteMenu(menuString, menuArrow, currentLineIndex)
        if menuMeta != None:
            if center:
                menuMeta = _textHandler.centerArrayItems(menuMeta)
            stdscr.addstr("\n\n".join(menuMeta) + "\n\n")
        if center: rewrittenMenu = makeStrCentered(rewrittenMenu, True)
        stdscr.addstr(rewrittenMenu, currentLineIndex)
        keyPressed = stdscr.getch()
        if keyPressed == curses.KEY_UP:
            nextLineIndex = currentLineIndex - 1
            currentLineIndex = nextLineIndex if currentLineIndex > 0 else len(menuLines) - 1
        elif keyPressed == curses.KEY_DOWN:
            nextLineIndex = currentLineIndex + 1
            currentLineIndex = nextLineIndex if currentLineIndex < len(menuLines) - 1 else 0
        elif keyPressed in [curses.KEY_ENTER, 10]:
            return currentLineIndex
        elif keyPressed in KEYS_QUIT:
            return

def rewriteMultiselectMenu(menuString: str, currentMenuLine: int, selectedItems: list, allowAll: bool = False):
    menuLines = getMenuComponents(menuString)[0]
    for i in range(len(menuLines)):
        selectionStatusCharacter = "\u25cf" if i in selectedItems else "\u25cb"
        if i == len(menuLines) - 1:
            menuLines[i] = "  %s" % menuLines[i] if currentMenuLine != i else "* %s" % menuLines[i]
            continue
        # Index for "Select All" option
        elif i == len(menuLines) - 2 and allowAll:
            menuLines[i] = "  %s" % menuLines[i] if currentMenuLine != i else "* %s" % menuLines[i]
            continue
        if currentMenuLine != i:
            menuLines[i] = "  %s %s" % (selectionStatusCharacter, menuLines[i])
        elif currentMenuLine == i:
            menuLines[i] = "* %s %s" % (selectionStatusCharacter, menuLines[i])
    return "\n".join(menuLines)

def getCenteredPos():
    return int(shutil.get_terminal_size().columns)//2, int(shutil.get_terminal_size().lines)//2

def makeStrCentered(targetStr: str, eachLine: bool = False) -> str:
    pos = getCenteredPos()
    if eachLine:
        targetStrLines = targetStr.splitlines()
        lengthiestString = 0
        for s in targetStrLines:
            if len(s) > lengthiestString:
                lengthiestString = len(s)
        spacing = " " * (pos[0] - lengthiestString//2)
        centeredStr = "\n" * (pos[1]//2 - len(targetStrLines)//2)
        for l in targetStrLines:
            centeredStr += f"{spacing}{l}\n"
        # centeredStr += "\n" * (pos[1]//2 + len(targetStrLines)//2) # Adds additional spacing (arbitrary)
    else:
        centeredStr = f"{chr(10)*pos[1]}{' '*pos[0]}{targetStr}"
    return centeredStr

def cursorArrowMultiselectMenu(stdscr, menuString: str, maxItemCount: int = None, allowAll: bool = False, center: bool = False):
    curses.curs_set(0)
    curses.use_default_colors()
    currentLineIndex = 0
    selectedItems = []
    if allowAll:
        menuString += "Select All\n"
    menuString += "Confirm Selection\n"
    stdscr.refresh()
    while True:
        stdscr.erase()
        menuLines, menuMeta = getMenuComponents(menuString)
        rewrittenMenu = rewriteMultiselectMenu(menuString, currentLineIndex, selectedItems, allowAll)
        if menuMeta != None:
            if center:
                menuMeta = _textHandler.centerArrayItems(menuMeta)
            stdscr.addstr("\n\n".join(menuMeta) + "\n\n")
        if center: rewrittenMenu = makeStrCentered(rewrittenMenu, True)
        stdscr.addstr(rewrittenMenu, currentLineIndex)
        keyPressed = stdscr.getch()
        if keyPressed == curses.KEY_UP:
            nextLineIndex = currentLineIndex - 1
            currentLineIndex = int(nextLineIndex) if currentLineIndex > 0 else len(menuLines) - 1
        elif keyPressed == curses.KEY_DOWN:
            nextLineIndex = currentLineIndex + 1
            currentLineIndex = int(nextLineIndex) if currentLineIndex < len(menuLines) - 1 else 0
        elif keyPressed in [curses.KEY_ENTER, 10]:
            if currentLineIndex == len(menuLines) - 2 and allowAll:
                selectedItems = list(range(len(menuLines) - 2)) if selectedItems != list(range(len(menuLines) - 2)) else []
                continue
            if currentLineIndex == len(menuLines) - 1:
                return selectedItems if bool(selectedItems) else None
            else:
                if currentLineIndex not in selectedItems and (maxItemCount <= len(selectedItems) if maxItemCount != None else False):
                    continue
                selectedItems.append(currentLineIndex) if not currentLineIndex in selectedItems else selectedItems.pop(selectedItems.index(currentLineIndex))
        elif keyPressed in KEYS_QUIT:
            return


def highlightSelectMenu(stdscr, menuComponents: tuple, center: bool = False):
    curses.curs_set(0)
    curses.use_default_colors()
    currentLineIndex = 0
    menuLines: list = menuComponents[0]
    menuTitle, menuDescription = menuComponents[1], menuComponents[2]
    centerSpacing = _textHandler.getItemSpacing(menuLines)
    while True:
        stdscr.erase()
        stdscr.refresh()
        if menuTitle != None:
            if center: stdscr.addstr(_textHandler.getItemSpacing([menuTitle]))
            stdscr.addstr(menuTitle + "\n\n")
        if menuDescription != None:
            if center: stdscr.addstr(_textHandler.getItemSpacing([menuDescription]))
            stdscr.addstr(menuDescription + "\n\n")
        if center: stdscr.addstr(_textHandler.getCenteredNewlines(menuLines))
        for l in menuLines:
            _strToAdd = "%s\n" % l
            if center: stdscr.addstr(centerSpacing)
            stdscr.addstr(_strToAdd) if menuLines.index(l) != currentLineIndex else stdscr.addstr(_strToAdd, curses.A_REVERSE)
            del _strToAdd
        keyPressed = stdscr.getch()
        if keyPressed == curses.KEY_DOWN:
            currentLineIndex = currentLineIndex + 1 if currentLineIndex != len(menuLines) - 1 else 0
        elif keyPressed == curses.KEY_UP:
            currentLineIndex = currentLineIndex - 1 if currentLineIndex != 0 else len(menuLines) - 1
        elif keyPressed in [curses.KEY_ENTER, 10]:
            return currentLineIndex
        elif keyPressed in KEYS_QUIT:
            return
