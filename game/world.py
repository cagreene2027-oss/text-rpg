# ============================================================
# world.py
# The map: loads regions.json, finds locations, and handles travel.
# ============================================================
import json
from pathlib import Path

from game.events import tryEvent

# Path(__file__) is this file (game/world.py). The first .parent is the
# game/ folder, and the second .parent is text-rpg/. This way the game
# always finds the data/ folder, no matter which folder you run it from.
DATA_FOLDER = Path(__file__).parent.parent / "data"

with open(DATA_FOLDER / "regions.json", encoding="utf-8") as file:
    Regions = json.load(file)


# Locations are stored inside their regions, so this searches every
# region for a location with the given name and returns its data.
def findLocation(name):
    for regionName, locations in Regions.items():
        if name in locations:
            return locations[name]
    return None


# The same search, but it returns the name of the region instead.
# Events need this, because which events can happen depends on the region.
def findRegion(name):
    for regionName, locations in Regions.items():
        if name in locations:
            return regionName
    return None


# The distance between two locations. Right now each location has one
# number. When you switch to (x, y) coordinates, only this function changes.
def getDistance(fromLocation, toLocation):
    return abs(toLocation["coordinates"] - fromLocation["coordinates"])


# Prints the region and description of where the player is.
def look(playerData):
    location = findLocation(playerData["location"])
    region = findRegion(playerData["location"])
    print(f"[{region}] {location['description']}")


# Lists the neighboring locations, lets the player pick one, and moves them.
def travel(playerData):
    current = findLocation(playerData["location"])
    neighbors = current["neighbors"]

    # Show each neighbor with a number next to it, starting at 1
    print("Where do you want to go?")
    for number, place in enumerate(neighbors, start=1):
        print(f"  {number}. {place}")

    choice = input("> ").strip()

    # Only accept a number that matches one of the listed places
    if choice.isdigit() and 1 <= int(choice) <= len(neighbors):
        destinationName = neighbors[int(choice) - 1]
        destination = findLocation(destinationName)
        distance = getDistance(current, destination)

        print(f"You travel {distance} units.")

        # Something might happen on the road before you arrive
        tryEvent(findRegion(destinationName), playerData)

        playerData["location"] = destinationName
        playerData["Coordinates"] = destination["coordinates"]
        print(destination["description"])
    else:
        print("That's not a valid choice.")
