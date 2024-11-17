import re
# Gets all the gadgets needed from a list of directions
# Each gadget has a:
# size (medium, 9x16-inch, etc)
# name (pan, baking dish, etc)

class Gadget:
    def __init__(self, size=None, name=None):
        self.size = size
        self.name = name
    
    def __repr__(self):
        return f"{self.size} {self.name}".strip()
    
    def __str__(self):
        return f"{self.size} {self.name}".strip()
    
    def __eq__(self, other):
        return self.size == other.size and self.name == other.name
    
    def __hash__(self):
        return hash((self.size, self.name))

NAMES = [
    "bowl",
    "pan",
    "dish",
    "pot",
    "skillet",
    "tray",
    "baking sheet",
    "baking dish",
    "saucepan",
    "oven",
    "baking pan"
]

TOOLS = [
    "knife",
    "spoon",
    "fork",
    "whisk",
    "tongs",
    "spatula",
    "grater",
    "peeler",
    "ladle",
    "rolling pin",
    "measuring cup",
    "measuring spoon",
    "mixing bowl",
    "cutting board",
    "colander",
    "strainer",
    "sifter",
    "timer",
    "thermometer",
    "scale",
    "oven mitt",
    "pot holder",
    "baking rack",
    "baking paper",
    "parchment paper",
    "aluminum foil",
    "plastic wrap",
    "wax paper",
    "tinfoil",
    "towel",
    "paper towel",
    "dish towel",
    "dish cloth",
    "pastry cutter"
]
    
def clean_directions(directions: list) -> list:
    directions = [direction.lower() for direction in directions]
    directions = [direction.strip() for direction in directions]
    return directions

def get_gadgets(directions):
    gadgets = set()
    directions = clean_directions(directions)
    
    # sort by length to prioritize longer matches
    combined_gadgets = sorted(NAMES + TOOLS, key=len, reverse=True)
    
    # regex for sizes and dimensions
    size_pattern = r"(small|medium|large)"
    dimension_pattern = r"(\d+x\d+-inch)"
    
    for d in directions:
        print(d)
        print()
        
        for gadget in combined_gadgets:
            regex = rf"(?:{size_pattern}|{dimension_pattern})?\s*{re.escape(gadget)}\b"
            match = re.search(regex, d)
            if match:
                size_or_dimension = match.group(1) or match.group(2)
                gadgets.add(Gadget(size=size_or_dimension, name=gadget))

    return gadgets