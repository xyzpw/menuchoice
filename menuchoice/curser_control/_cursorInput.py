import curses
import re

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

def cursorArrowMenu(stdscr, menuString: str, menuArrow: str):
    curses.curs_set(0)
    currentLineIndex = 0
    stdscr.refresh()
    while True:
        stdscr.clear()
        stdscr.refresh()
        menuLines, menuMeta = getMenuComponents(menuString)
        rewrittenMenu = rewriteMenu(menuString, menuArrow, currentLineIndex)
        if menuMeta != None:
            stdscr.addstr("\n\n".join(menuMeta) + "\n\n")
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

def rewriteMultiselectMenu(menuString: str, currentMenuLine: int, selectedItems: list):
    menuLines = getMenuComponents(menuString)[0]
    for i in range(len(menuLines)):
        selectionStatusCharacter = "\u25cf" if i in selectedItems else "\u25cb"
        if i == len(menuLines) - 1:
            menuLines[i] = "  %s" % menuLines[i] if currentMenuLine != i else "* %s" % menuLines[i]
            continue
        if currentMenuLine != i:
            menuLines[i] = "  %s %s" % (selectionStatusCharacter, menuLines[i])
        elif currentMenuLine == i:
            menuLines[i] = "* %s %s" % (selectionStatusCharacter, menuLines[i])
    return "\n".join(menuLines)

def cursorArrowMultiselectMenu(stdscr, menuString: str, maxItemCount: int = None):
    curses.curs_set(0)
    currentLineIndex = 0
    selectedItems = []
    menuString += "Confirm Selection\n"
    stdscr.refresh()
    while True:
        stdscr.clear()
        menuLines, menuMeta = getMenuComponents(menuString)
        rewrittenMenu = rewriteMultiselectMenu(menuString, currentLineIndex, selectedItems)
        if menuMeta != None:
            stdscr.addstr("\n\n".join(menuMeta) + "\n\n")
        stdscr.addstr(rewrittenMenu, currentLineIndex)
        keyPressed = stdscr.getch()
        if keyPressed == curses.KEY_UP:
            nextLineIndex = currentLineIndex - 1
            currentLineIndex = int(nextLineIndex) if currentLineIndex > 0 else len(menuLines) - 1
        elif keyPressed == curses.KEY_DOWN:
            nextLineIndex = currentLineIndex + 1
            currentLineIndex = int(nextLineIndex) if currentLineIndex < len(menuLines) - 1 else 0
        elif keyPressed in [curses.KEY_ENTER, 10]:
            if currentLineIndex == len(menuLines) - 1:
                return selectedItems if bool(selectedItems) else None
            else:
                if currentLineIndex not in selectedItems and (maxItemCount <= len(selectedItems) if maxItemCount != None else False):
                    continue
                selectedItems.append(currentLineIndex) if not currentLineIndex in selectedItems else selectedItems.pop(selectedItems.index(currentLineIndex))

