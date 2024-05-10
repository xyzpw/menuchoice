# menuchoice
Command line menu selector

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
> [!HINT]
> items can be given brief descriptions if they are type dictionary.
> `{"option": "brief description"}`

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
```
Output:
```python
[(4, "EDM"), (1, "Rock")]
```