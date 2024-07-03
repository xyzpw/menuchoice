import curses
import re
import shutil
from . import _textHandler

KEYS_QUIT = [ord("q"), ord("Q")]
KEYS_SELECT = [curses.KEY_ENTER, 10]

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
        elif keyPressed in KEYS_SELECT:
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
        stdscr.refresh()
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
        elif keyPressed in KEYS_SELECT:
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


def highlightSelectMenu(stdscr, menuComponents: tuple, center: bool = False, disabled_options: list[int] = []):
    curses.curs_set(0)
    curses.use_default_colors()
    menuLines: list = menuComponents[0]
    menuTitle, menuDescription = menuComponents[1], menuComponents[2]
    centerSpacing = _textHandler.getItemSpacing(menuLines)
    enabledMenuLines = [i for i in menuLines if menuLines.index(i) not in disabled_options]
    enabledOptions = [i for i in range(len(menuLines)) if i not in disabled_options]
    currentLineIndex = min(enabledOptions)
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
            currentLineIndex = min([i for i in enabledOptions if i > currentLineIndex]) if currentLineIndex != max(enabledOptions) else min(enabledOptions)
        elif keyPressed == curses.KEY_UP:
            currentLineIndex = max([i for i in enabledOptions if i < currentLineIndex]) if currentLineIndex != min(enabledOptions) else max(enabledOptions)
        elif keyPressed in KEYS_SELECT:
            return currentLineIndex
        elif keyPressed in KEYS_QUIT:
            return

def highlightMultiPageSelectMenu(stdscr, menuComponents: tuple, center: bool = False,
                                 disabled_options: list[int] = [], pages: list[list] = []):
    curses.curs_set(0)
    curses.use_default_colors()
    menuLines = menuComponents[0]
    menuTitle = menuComponents[1]
    menuDescription = menuComponents[2]
    currentPageNumber, currentPageIndex = 1, 0
    enabledOptions = [i for i in range(len(menuLines)) if i not in disabled_options]
    enabledPageOptions = []
    for p in pages:
        enabledPageOptions.append([i for i in p if i in enabledOptions])
    currentLineIndex = min(enabledOptions)
    while True:
        stdscr.erase()
        stdscr.refresh()
        pageDisplayText = f"Page {currentPageNumber} of {len(pages)}"
        if center: stdscr.addstr(_textHandler.getItemSpacing([pageDisplayText]))
        stdscr.addstr(pageDisplayText + "\n\n")
        if menuTitle != None:
            if center: stdscr.addstr(_textHandler.getItemSpacing([menuTitle]))
            stdscr.addstr(menuTitle + "\n\n")
        if menuDescription != None:
            if center: stdscr.addstr(_textHandler.getItemSpacing([menuDescription]))
            stdscr.addstr(menuDescription + "\n\n")
        for l in pages[currentPageIndex]:
            _strToAdd = "%s\n" % menuLines[l]
            if center: stdscr.addstr(_textHandler.getItemSpacing(_strToAdd))
            stdscr.addstr(_strToAdd) if currentLineIndex != l else stdscr.addstr(_strToAdd, curses.A_REVERSE)
        pressedKey = stdscr.getch()
        workingEnabledPageOptions = enabledPageOptions[currentPageIndex]
        if pressedKey == curses.KEY_DOWN:
            currentLineIndex = min([i for i in workingEnabledPageOptions if i > currentLineIndex]) if currentLineIndex != max(workingEnabledPageOptions) else min(workingEnabledPageOptions)
        elif pressedKey == curses.KEY_UP:
            currentLineIndex = max([i for i in range(min(workingEnabledPageOptions), currentLineIndex)]) if currentLineIndex != min(workingEnabledPageOptions) else max(workingEnabledPageOptions)
        elif pressedKey == curses.KEY_RIGHT:
            currentPageIndex = (currentPageIndex + 1) if currentPageIndex != len(pages)-1 else 0
            currentPageNumber = currentPageIndex + 1
            currentLineIndex = min(enabledPageOptions[currentPageIndex])
        elif pressedKey == curses.KEY_LEFT:
            currentPageIndex = (currentPageIndex - 1) if currentPageIndex != 0 else len(pages)-1
            currentPageNumber = currentPageIndex + 1
            currentLineIndex = min(enabledPageOptions[currentPageIndex])
        elif pressedKey in KEYS_SELECT:
            return currentLineIndex
        elif pressedKey in KEYS_QUIT:
            return

def editableMenu(stdscr, menuComponents: dict, center: bool = False, options: list[tuple] = [], disabled_options: list[int] = []):
    menuItems, menuTitle, menuDescription = menuComponents[0], menuComponents[1], menuComponents[2]
    enabledIndexes = [i for i in range(len(menuItems)) if not i in disabled_options]
    currentLineIndex = min(enabledIndexes)
    checkItemModifiable = lambda _itemIndex: _itemIndex in [i[0] for i in options]
    getItemOptionCount = lambda _itemIndex: len([i for i in options if i[0] == _itemIndex][0]) # don't subtract 1 to account for default value
    modifiableItems = {}
    for i in menuItems:
        if checkItemModifiable(menuItems.index(i)):
            # Creating a dictionary — named `modifiableItems` — containing info for each modifiable item:
                # key is the index out of all items in the menu selector
                # key value is the index to the options value tuple value which contains the menu item string
                # option list example:
                    # [(0, "second selectable item text"), (1, "second selectable item text for second menu item")]
            modifiableItems[menuItems.index(i)] = 0
    curses.curs_set(0)
    curses.use_default_colors()
    while True:
        stdscr.refresh()
        stdscr.erase()
        if menuTitle != None:
            if center: stdscr.addstr(_textHandler.getItemSpacing([menuTitle]))
            stdscr.addstr("%s\n\n" % menuTitle)
        if menuDescription != None:
            if center: stdscr.addstr(_textHandler.getItemSpacing([menuDescription]))
            stdscr.addstr("%s\n\n" % menuDescription)
        for i in menuItems:
            if checkItemModifiable(menuItems.index(i)):
                _currentModifiableStringIndex = modifiableItems[menuItems.index(i)]
                #NOTE: displayed option is default if the index is 0
                if _currentModifiableStringIndex != 0:
                    _currentModifiableString = [o[_currentModifiableStringIndex] for o in options if o[0] == menuItems.index(i)][0]
                else:
                    _currentModifiableString = str(i)
                _strToAdd = "< %s >\n" % _currentModifiableString
            else:
                _strToAdd = "%s\n" % i
            if center: stdscr.addstr(_textHandler.getItemSpacing([i]))
            stdscr.addstr(_strToAdd) if currentLineIndex != menuItems.index(i) else stdscr.addstr(_strToAdd, curses.A_REVERSE)
        pressedKey = stdscr.getch()
        if pressedKey == curses.KEY_DOWN:
            currentLineIndex = min([i for i in range(currentLineIndex+1, len(menuItems)) if not i in disabled_options]) if currentLineIndex != max(enabledIndexes) else min(enabledIndexes)
        elif pressedKey == curses.KEY_UP:
            currentLineIndex = max([i for i in range(currentLineIndex) if not i in disabled_options]) if currentLineIndex != min(enabledIndexes) else max(enabledIndexes)
        elif pressedKey == curses.KEY_RIGHT:
            if not checkItemModifiable(currentLineIndex): continue
            if modifiableItems[currentLineIndex] + 1 > getItemOptionCount(currentLineIndex) - 1:
                modifiableItems[currentLineIndex] = 0
                continue
            modifiableItems[currentLineIndex] += 1
        elif pressedKey == curses.KEY_LEFT:
            if not checkItemModifiable(currentLineIndex): continue
            if modifiableItems[currentLineIndex] - 1 < 0:
                modifiableItems[currentLineIndex] = getItemOptionCount(currentLineIndex) - 1
                continue
            modifiableItems[currentLineIndex] -= 1
        elif pressedKey in KEYS_SELECT:
            if checkItemModifiable(currentLineIndex):
                _currentModifiableString = [i[modifiableItems[currentLineIndex]] for i in options if i[0] == currentLineIndex][0]
                if modifiableItems[currentLineIndex] == 0: _currentModifiableString = menuItems[currentLineIndex]
                return [(currentLineIndex, _currentModifiableString)]
            else:
                return [(currentLineIndex, menuItems[currentLineIndex])]
        elif pressedKey in KEYS_QUIT:
            return
