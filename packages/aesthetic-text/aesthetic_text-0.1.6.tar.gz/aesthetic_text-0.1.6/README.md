# Aesthetic TEXT

Give a beautiful look of your text in the terminal.

**link to access to the pypi page :** https://pypi.org/project/aesthetic-text/0.1.0/

## Installation

```zsh
$ pip install aesthetic_text
```

### Usage

```python
from aesthetic_text import aesthetic_text as aesthetic

# print a text with a style
# style: bold, italic, underline, strikethrough, reverse, conceal, crossed
print(f"{aesthetic.style.bold}{aesthetic.style.underline}" + "Hello World" + f"{aesthetic.reset}")

# print a text with a color
# colors: black, red, green, yellow, blue, magenta, cyan, white...
print(f"{aesthetic.color.red}" + "Hello World" + f"{aesthetic.reset}")

# print a text with style and color
print(f"{aesthetic.style.bold}{aesthetic.color.red}" + "Hello World" + f"{aesthetic.reset}"
