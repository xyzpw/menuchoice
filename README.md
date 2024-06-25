# menuchoice
![Pepy Total Downlods](https://img.shields.io/pepy/dt/menuchoice)
![GitHub repo size](https://img.shields.io/github/repo-size/xyzpw/menuchoice)
![PyPi - Version](https://img.shields.io/pypi/v/menuchoice)

Command line menu selector.

![menuchoice-demo2](https://github.com/xyzpw/menuchoice/assets/76017734/c3ca060d-0c39-47be-9173-fa0d415a20b9)

## Usage
Creating a selection menu:
```python
import menuchoice
myMenu = menuchoice.MenuSelector(items=[
    "Hip-hop",
    "Rock",
    "Pop",
    "Country",
    "EDM",
], title="Most Streamed Music USA", description="Select a genre of music.")
```
> [!TIP]
> items can be given brief descriptions if they are type dictionary: `{"option": "brief description"}`

Selecting an option:
```python
myMenu.prompt_select() # basic user-input method
myMenu.arrow_select()
```
Output:
```python
[(4, "EDM")]
```
Additionally, multiple options can be selected
```python
# no less than 2, no more than 3
myMenu.arrow_select(max_items=(2, 3))
# Adds an option to select all items
myMenu.arrow_select(allow_all=True)
```
Output:
```python
[(4, "EDM"), (1, "Rock")]
```

**Highlight menu**<br>

Highlight menus introduce the ability to have multiple pages (this is optional):
```python
myMenu.highlight_select(pages=[[0, 1, 2], [3, 4]])
```

The above code will create two pages, the first page contains the first three options, the second contains the last two options.<br>
To switch between these pages, use the left/right arrow keys.<br>

The highlight menu can also disable options:
```python
myMenu.highlight_select(disabled_items=[3])
```
This code above will prevent to user from selecting index 3 of the menus items (the fourth option).