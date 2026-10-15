# ============================================================
# events.py
# Random things that can happen while traveling.
# These are simple scripted samples. Later, the AI can write new
# events, and this list becomes the backup if the AI fails.
# ============================================================
import random

# The chance an event happens each time you travel (0.3 = 30%)
EVENT_CHANCE = 0.3

# Each event has:
#   text:    what the player reads
#   regions: where it can happen ("any" means every region)
#   weight:  how common it is (higher = more common)
#   effect:  "hp", "gilden", "item", or "none"
#   amount:  how much HP or Gilden changes (negative means you lose some)
#   item:    the item's name, for "item" events (must match items.json)
Events = [
    # ---------- Any region ----------
    {
        "text": "You find a small pouch of coins half-buried by the road.",
        "regions": ["any"],
        "weight": 2,
        "effect": "gilden",
        "amount": 10,
    },
    {
        "text": "You step on a loose stone and twist your ankle.",
        "regions": ["any"],
        "weight": 2,
        "effect": "hp",
        "amount": -5,
    },
    {
        "text": "You rest beside a clear stream and drink until you feel steady again.",
        "regions": ["any"],
        "weight": 2,
        "effect": "hp",
        "amount": 10,
    },
    {
        "text": "An old traveler walks beside you for a while, telling stories of a hero who lived eighty years ago.",
        "regions": ["any"],
        "weight": 2,
        "effect": "none",
    },

    # ---------- One for each region ----------
    {
        "text": "Near the path, you spot a patch of healing herbs and pick a handful.",
        "regions": ["Lindmark"],
        "weight": 3,
        "effect": "item",
        "item": "Healing Herb",
    },
    {
        "text": "A boy bumps into you and runs off. Your coin pouch feels lighter.",
        "regions": ["Elsmere"],
        "weight": 3,
        "effect": "gilden",
        "amount": -8,
    },
    {
        "text": "A student's practice spell goes wide and singes your arm.",
        "regions": ["Calvaren"],
        "weight": 3,
        "effect": "hp",
        "amount": -8,
    },
    {
        "text": "Pale lights drift over the burial mounds. When you step toward them, they vanish.",
        "regions": ["The Dunmoor"],
        "weight": 3,
        "effect": "none",
    },
    {
        "text": "Rocks tumble down the cliff above you. You dive aside, but not fast enough.",
        "regions": ["Vael Ridge"],
        "weight": 3,
        "effect": "hp",
        "amount": -10,
    },
    {
        "text": "Something glints in the snow. You dig out a crystal of ice that won't melt.",
        "regions": ["The Pale Reach"],
        "weight": 3,
        "effect": "item",
        "item": "Frost Crystal",
    },
    {
        "text": "Falling ash fills the air, and every breath burns your throat.",
        "regions": ["Nocthollow"],
        "weight": 3,
        "effect": "hp",
        "amount": -12,
    },
]


# Rolls a random number from 0 to 1. Returns True if an event should happen.
def rollForEvent():
    return random.random() < EVENT_CHANCE


# Returns every event that can happen in this region.
def getPossibleEvents(regionName):
    possible = []
    for event in Events:
        if "any" in event["regions"] or regionName in event["regions"]:
            possible.append(event)
    return possible


# Picks one event at random. Events with a higher weight get picked more often.
def pickEvent(possibleEvents):
    weights = []
    for event in possibleEvents:
        weights.append(event["weight"])

    # random.choices returns a list, so [0] grabs the one event inside it
    return random.choices(possibleEvents, weights=weights)[0]


# Prints the event and applies its effect to the player.
def runEvent(event, playerData):
    print()
    print(event["text"])

    effect = event["effect"]

    if effect == "hp":
        oldHp = playerData["hp"]
        # min() stops healing from going above max HP.
        # max() stops events from dropping you below 1 HP, so a random
        # event can hurt you but never end your game.
        newHp = max(1, min(oldHp + event["amount"], playerData["maxHp"]))
        playerData["hp"] = newHp

        change = newHp - oldHp
        if change > 0:
            print(f"You recover {change} HP.")
        elif change < 0:
            print(f"You lose {-change} HP.")
        print(f"HP: {newHp}/{playerData['maxHp']}")

    elif effect == "gilden":
        oldGilden = playerData["gilden"]
        # max() stops Gilden from going below 0
        newGilden = max(0, oldGilden + event["amount"])
        playerData["gilden"] = newGilden

        change = newGilden - oldGilden
        if change > 0:
            print(f"You gain {change} Gilden.")
        elif change < 0:
            print(f"You lose {-change} Gilden.")
        print(f"Gilden: {newGilden}")

    elif effect == "item":
        playerData["inventory"].append(event["item"])
        print(f"You got: {event['item']}")

    print()


# The one function other files call. It rolls for an event and, if one
# happens, picks one that fits the region and runs it.
def tryEvent(regionName, playerData):
    if not rollForEvent():
        return

    possible = getPossibleEvents(regionName)
    if len(possible) == 0:
        return

    event = pickEvent(possible)
    runEvent(event, playerData)
