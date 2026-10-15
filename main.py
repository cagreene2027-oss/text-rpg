# ============================================================
# TEXT RPG ROADMAP
# Mark items done by changing [ ] to [x]
# ============================================================
#
# MILESTONE 1: Core game (Lindmark only)
#   [ ] Game loop: show location, read a command, update game
#   [ ] Commands: look, go <direction>, help, quit
#   [ ] Rooms: Hollin, The Linden Wood, Brannoc's Watch
#   [ ] Player and Enemy classes (HP, attack, defense)
#   [ ] Turn-based fight with dice rolls (attack / flee)
#   [ ] Load enemies from data/enemies.json
#   [ ] First test: check that damage math works (pytest)
#
# MILESTONE 2: The world
#   [ ] Load all 7 regions + 21 locations from regions.json
#   [ ] Travel between neighboring regions
#   [ ] Use BFS to find how far each region is from Nihtgard
#   [ ] Random encounters while traveling
#
# MILESTONE 3: Items and money
#   [ ] Inventory: pick up, drop, use, equip
#   [ ] Load items from data/items.json
#   [ ] Gilden: earn from fights, spend at shops
#   [ ] A shop in Hollin
#   [ ] Loot tables with rare drops
#   [ ] Tests for inventory and buying/selling
#
# MILESTONE 4: Growth
#   [ ] XP and leveling up
#   [ ] Skills and spells the player unlocks
#   [ ] Mini-boss at Brannoc's Watch
#   [ ] Lock later regions until the player is strong enough
#
# MILESTONE 5: Saving
#   [ ] Save and load the game (JSON file first)
#   [ ] Switch saves to a SQLite database
#   [ ] Player accounts with hashed passwords
#
# MILESTONE 6: AI NPCs
#   [ ] One AI NPC: the old mage in Hollin
#   [ ] AI replies in JSON: dialogue line + action
#   [ ] Game checks the action is allowed before running it
#   [ ] NPC remembers past conversations (saved in database)
#   [ ] Scripted fallback lines if the AI fails
#
# MILESTONE 7: Endgame
#   [ ] Enemies and quests for every region
#   [ ] Final boss fight at the Dusk Throne
#   [ ] Ending scene
#
# MILESTONE 8: Online
#   [ ] FastAPI server that runs the game
#   [ ] Simple web page so anyone can play from a link
#   [ ] Leaderboard
#   [ ] README with a gameplay GIF
#
# STRETCH GOALS
#   [ ] Discord bot version
#   [ ] Music that changes with location and combat
#   [ ] Lockpicking minigame
# ============================================================

from game.world import Regions, look, travel
from game.style import styled, printStyled, printHeader, printDivider

playerData = {
    # Where you are
    "name": "Player",
    "location": "Hollin",
    "Coordinates": 0,

    # Leveling
    "level": 1,
    "xp": 0,
    "points": 3,        # unspent attribute points

    # Attributes (locked in once you spend points)
    "strength": 3,
    "vitality": 3,
    "intellect": 3,
    "agility": 3,

    # Health and survival
    "hp": 35,
    "maxHp": 35,
    "mana": 20,
    "energy": 100,      # 100 = fully rested, 0 = exhausted
    "hunger": 100,      # 100 = full, 0 = starving

    # Belongings
    "gilden": 20,
    "inventory": []
}

def findLocation(name):
    for regionName, locations in Regions.items():
        if name in locations:
            return locations[name]
    return None

def showStatus():
    p = playerData
    printDivider()
    print(styled(p["location"], None, "bold") + "  |  "
          + styled(f"HP {p['hp']}/{p['maxHp']}", "red") + "  "
          + styled(f"Energy {p['energy']}", "blue") + "  "
          + styled(f"Hunger {p['hunger']}", "green") + "  "
          + styled(f"{p['gilden']} Gilden", "gold"))

def getOptions():
    location = findLocation(playerData["location"])
    options = ["explore", "travel", "inventory"]
    if location["type"] == "town":
        options += ["shop", "rest", "talk"]
    else:
        options += ["hunt", "camp"]
    options.append("quit")
    return options

def showOptions(options):
    for number, option in enumerate(options, start=1):
        print("  " + styled(number, "cyan", "bold") + ". " + option)

def performCommand(command, options):
    if command == "":
        return True

    if command not in options:
        printStyled("You can't do that here. Pick a number from the list.", "red")
        return True

    if command == "travel":
        travel(playerData)
    elif command == "quit":
        printStyled("Farewell, traveler.", "cyan", "italic")
        return False
    else:
        printStyled(f"'{command}' isn't built yet.", "gray", "italic")

    return True




def main():
    running = True
    while running:
        options = getOptions()
        showStatus()
        showOptions(options)
        choice = input("> ").strip().lower()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            choice = options[int(choice) - 1]
        running = performCommand(choice, options)

if __name__ == "__main__":
    main()