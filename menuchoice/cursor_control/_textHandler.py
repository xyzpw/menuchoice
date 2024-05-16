from . import _cursorInput

def centerArrayItems(usrArray: list) -> list:
    lengthiestStr = 0
    for s in usrArray:
        lengthiestStr = len(s) if len(s) > lengthiestStr else lengthiestStr
    spacing = _cursorInput.getCenteredPos()[0] - lengthiestStr//2
    metaStr = [f"{spacing * ' '}{usrArray[i]}" for i in range(len(usrArray))]
    return metaStr

def getItemSpacing(usrArray: list) -> str:
    lengthiestStr = 0
    for s in usrArray:
        lengthiestStr = len(s) if len(s) > lengthiestStr else lengthiestStr
    spacing = _cursorInput.getCenteredPos()[0] - lengthiestStr//2
    return " "*spacing

def getCenteredNewlines(usrArray: list) -> str:
    lengthiestStr = 0
    for s in usrArray:
        lengthiestStr = len(s) if len(s) > lengthiestStr else lengthiestStr
    newlines = "\n" * (_cursorInput.getCenteredPos()[1]//2 - len(usrArray)//2)
    return newlines

