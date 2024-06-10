"""Command line menu selector."""

import curses
import re
from .cursor_control import _cursorInput
from .exceptions import *
from . import _validator

__version__ = "0.7"
__author__ = "xyzpw"
__description__ = "Command line menu selector."
__license__ = "MIT"

class MenuSelector:
    """Contains items which can be prompted via a menu selector."""
    def __init__(self, items: list | dict, title: str = None, description: str = None):
        self.items = items
        self.title = title
        self.description = description
    def createMenuString(self, num_sep: str = ")", align: bool = False) -> str:
        menu = ""
        if self.title != None: menu += self.title
        menu += "\n\n%s\n\n" % self.description if self.description != None else ("\n\n" if self.title != None else "")
        lengthiestItem = 0
        if align:
            for item in self.items:
                _length = len(str(item))
                if lengthiestItem < _length:
                    lengthiestItem = int(_length)
        makePadding = lambda itemStr: f"{' '*(lengthiestItem - len(itemStr))}" if lengthiestItem > 1 else ""
        for item in self.items:
            _index = list(self.items).index(item)
            menu += "%s%s %s" % (_index, num_sep, item)
            menu += f" - {makePadding(item)}{self.items.get(item)}\n" if isinstance(self.items, dict) else "\n"
        return menu
    def prompt_select(self, num_sep: str = ")", align: bool = False,
            max_items: tuple = (1, 1), clear: bool = False,
            allow_all: bool = False, center: bool = False) -> list[tuple]:
        """Prompts for an integer while displaying the values associated with that index.

        :param num_sep: separator between number and item, e.g. ) for N)
        :param align: aligns items by adding additional spaces between items and their descriptions
        :param max_items: a range of numbers which represent the number of items required to be selected
        :param clear: clears the screen prior to displaying the menu
        :param allow_all: adds a select all option to the item list
        :param center: positions the menu selector to the center of the terminal"""
        if allow_all:
            max_items = (max_items[0], len(self.items))
        if not _validator.validateMaxItemsRange(max_items):
            raise MenuItemError("allowed items range is invalid")
        menu = self.createMenuString(num_sep, align)
        if allow_all: menu += "%d%s Select All\n" % (len(self.items), num_sep)
        if clear:
            print("\x1b[H\x1b[2J\x1b[3J", end='') # using ansi codes to clear buffer and entirety of terminal screen
        if center: menu = cursor_control._cursorInput.makeStrCentered(menu, True)
        choiceIndexes = re.findall(r"(?P<index>\d+)(?:,\s?|\s|\Z)", input(menu + "> "))
        if allow_all and str(len(self.items)) in choiceIndexes: choiceIndexes = list(range(len(self.items)))
        if not _validator.validateItemSelectionCount(max_items, choiceIndexes):
            raise MenuItemError("number of items selected is out of range")
        return [(i, list(self.items)[int(i)]) for i in choiceIndexes]
    def arrow_select(self, num_sep: str = ")", align: bool = False,
            arrow: str = "=>", max_items: tuple = (1, 1),
            allow_all: bool = False, center: bool = False):
        """Allows the user to select options with the arrow keys.

        :param num_sep: separator between number and item, e.g. ) for N)
        :param align: aligns items by adding additional spaces between items and their descriptions
        :param arrow: the string which represents the arrow that points to the text which will be selected
        :param max_items: a range of numbers which represent the number of items required to be selected
        :param allow_all: adds a select all option to the item list
        :param center: positions the menu selector to the center of the terminal"""
        if allow_all:
            max_items = (max_items[0], len(self.items))
        if not _validator.validateMaxItemsRange(max_items):
            raise MenuItemError("allowed items range is invalid")
        menu = self.createMenuString(num_sep, align)
        if max_items[1] > 1 if max_items[1] != None else True:
            selectedIndexes = curses.wrapper(_cursorInput.cursorArrowMultiselectMenu, menu, max_items[1], allow_all, center)
            usrChoices = [(i, list(self.items)[i]) for i in selectedIndexes] if selectedIndexes != None else []
        else:
            selectedIndexes = curses.wrapper(_cursorInput.cursorArrowMenu, menu, arrow, center)
            usrChoices = [(selectedIndexes, list(self.items)[selectedIndexes])] if selectedIndexes != None else []
        if not _validator.validateItemSelectionCount(max_items, usrChoices) and bool(usrChoices):
            raise MenuItemError("number of items selected is out of range")
        return usrChoices
    def highlight_select(self, center: bool = False):
        """Highlights the options at the current line index.

        :param center: positions the menu selector to the center of the terminal"""
        menuComponents = self.items, self.title, self.description
        selectedIndex = curses.wrapper(_cursorInput.highlightSelectMenu, menuComponents, center)
        usrChoice = [(selectedIndex, list(self.items)[selectedIndex])] if selectedIndex != None else []
        return usrChoice
