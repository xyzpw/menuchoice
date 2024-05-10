def validateMaxItemsRange(maxItems: tuple[int]):
    least = maxItems[0] if maxItems[0] != None else 0
    greatest = maxItems[1]
    return True if (True if (greatest==None and least >= 0) else False)==True else (True if least <= greatest and least >= 0 else False)==True

def validateItemSelectionCount(maxItems: tuple, selectedItems: int):
    least = maxItems[0] if maxItems[0] != None else 0
    greatest = maxItems[1]
    itemCount = len(selectedItems)
    if itemCount in range(least, greatest + 1) if greatest != None else (True if greatest==None and least >= 0 and itemCount >= least else False):
        return True
    return False
