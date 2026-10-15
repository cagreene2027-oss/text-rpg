# ============================================================
# style.py
# Colors and text styles for the terminal.
#
# How to use it:
#   from game.style import styled, printStyled, printHeader, printDivider
#
#   printStyled("Travel", "blue", "bold", "italic")    # prints it
#   printStyled("You found 12 Gilden!", "gold")
#   printStyled("A custom color", "#8A2BE2", "bold")   # hex color codes work too
#
#   # styled() gives back the styled text instead of printing it,
#   # so you can build one line out of several colors:
#   print(styled("HP 80", "red") + "  " + styled("12 Gilden", "gold"))
# ============================================================
import os

# Older Windows terminals don't understand color codes until this runs.
# It does nothing on Mac or Linux.
if os.name == "nt":
    os.system("")

# Ends a style, so the color doesn't leak into the next text you print.
RESET = "\033[0m"


# Turns a hex color like "#FFA500" into the code the terminal understands.
def hexToCode(hexColor):
    hexColor = hexColor.lstrip("#")
    try:
        red = int(hexColor[0:2], 16)
        green = int(hexColor[2:4], 16)
        blue = int(hexColor[4:6], 16)
    except ValueError:
        raise ValueError(f"'#{hexColor}' isn't a hex color. Use 6 digits, like '#FFA500'.")
    if len(hexColor) != 6:
        raise ValueError(f"'#{hexColor}' isn't a hex color. Use 6 digits, like '#FFA500'.")
    return f"38;2;{red};{green};{blue}"


# Color names you can use. Add your own here, like "frost": hexToCode("#A8E6FF").
COLORS = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    "gray": "90",
    "grey": "90",
    "bright red": "91",
    "bright green": "92",
    "bright yellow": "93",
    "bright blue": "94",
    "bright magenta": "95",
    "bright cyan": "96",
    "orange": hexToCode("#FFA500"),
    "gold": hexToCode("#FFD700"),
    "purple": hexToCode("#9B59B6"),
    "brown": hexToCode("#A0522D"),
}

# Effects you can use. You can stack as many as you want.
EFFECTS = {
    "bold": "1",
    "dim": "2",
    "italic": "3",
    "underline": "4",
    "strike": "9",
}


# Finds the code for a color name or a hex color.
def getColorCode(color):
    if color.startswith("#"):
        return hexToCode(color)

    name = color.lower()
    if name not in COLORS:
        raise ValueError(f"Unknown color '{color}'. Choose from: {', '.join(COLORS)}, or a hex code like '#FFA500'.")
    return COLORS[name]


# Returns the text with a color and any number of effects added.
# color can be None if you only want effects, like styled("Hi", None, "bold").
def styled(text, color=None, *effects):
    codes = []

    if color:
        codes.append(getColorCode(color))

    for effect in effects:
        name = effect.lower()
        if name not in EFFECTS:
            raise ValueError(f"Unknown effect '{effect}'. Choose from: {', '.join(EFFECTS)}.")
        codes.append(EFFECTS[name])

    # str() lets you style numbers too, like styled(80, "red")
    if not codes:
        return str(text)
    return f"\033[{';'.join(codes)}m{text}{RESET}"


# The same as styled(), but prints the text right away.
def printStyled(text, color=None, *effects):
    print(styled(text, color, *effects))


# A bold, underlined title, like the name of a place or a menu.
def printHeader(text, color="cyan"):
    print()
    printStyled(text, color, "bold", "underline")


# A line to separate one turn from the next.
def printDivider(color="gray", length=50):
    printStyled("─" * length, color)
