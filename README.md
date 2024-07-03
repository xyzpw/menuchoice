# menuchoice
![Pepy Total Downlods](https://img.shields.io/pepy/dt/menuchoice)
![GitHub repo size](https://img.shields.io/github/repo-size/xyzpw/menuchoice)
![PyPi - Version](https://img.shields.io/pypi/v/menuchoice)

**menuchoice** is a terminal-based menu selector with different menu styles and features.

![menuchoice-demo2](https://github.com/xyzpw/menuchoice/assets/76017734/c3ca060d-0c39-47be-9173-fa0d415a20b9)

## Usage
Creating a selection menu:
```python
import menuchoice
menu = menuchoice.MenuSelector(items=[
    "Hip-hop",
    "Rock",
    "Pop",
    "Country",
    "EDM",
], title="Most Streamed Music USA", description="Select a genre of music.")
```
> [!TIP]
> items can be given brief descriptions if they are type dictionary: `{"option": "brief description"}`

### Arrow Selection
Arrow select will display an arrow which can be moved up/down with the arrow keys:
```python
menu.arrow_select()
```
Output upon selection:
```python
[(4, "EDM")]
```

Additionally, multiple options can be selected:
```python
# no less than 2, no more than 3
menu.arrow_select(max_items=(2, 3))
# Adds an option to select all items
menu.arrow_select(allow_all=True)
```
Output:
```python
[(4, "EDM"), (1, "Rock")]
```

### Highlight Selecting
Highlight menus introduce the ability to have multiple pages (this is optional):
```python
menu.highlight_select(pages=[[0, 1, 2], [3, 4]])
```

The above code will create two pages, the first page contains the first three options, the second contains the last two options.<br>
To switch between these pages, use the left/right arrow keys.

The highlight menu can also disable options:
```python
menu.highlight_select(disabled_items=[3])
```
This code above will prevent the user from selecting index 3 of the menus items (the fourth option).

### Modifying Options
Menu selector items can have multiple options which can be navigated through with left/right arrow keys.

```python
menu.modify_select(options=[(0, "second option", "third option")])
```
This will allow the user to use left/right arrow keys to navigate through 3 different options for a single item's line.
