DURATION_METHODS = [
    "preheat", "cook", "bake", "boil", "broil", "poach", 
    "sauté", "simmer", "roast", "toast", "chill", "freeze", 
    "marinate", "grill", "steam", "blanch", "fry", "knead",
    "boil", "reduce", "heat"
]
NO_DURATION_METHODS = [
    "drain", "transfer", "mix", "chop", "grate", "cut", 
    "stir", "gather", "mash", "add", "sprinkle", "serve",
    "whisk", "dice", "slice", "fold", "pour", "peel", 
    "crack", "press", "spread", "combine", "coat", 
    "layer", "shape", "melt", "place"
]

STEP_STOP_WORDS = [
    "in", "on", "at", "to", "with", "by", "for", "of", "from", "over", "into", "between", "through", "until", "about", "after", "before", "during", "under", "against", "up", "down", "off", "out", "around", "throughout", "upon", "along", "across", "toward", "away", "behind", "beneath", "beside", "inside", "onto", "underneath", "within", "without", "above", "below", "among", "around", "before", "behind", "beneath", "beside", "between", "inside", "outside", "throughout", "underneath", "where", "when", "how", "why", "what", "who", "which", "whom", "whose", "whether", "whenever"
]

REFERENCE_WORDS = [
    "them", "it"
]
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
    "baking pan",
    "casserole dish",
    "wok",
    "dutch oven",
    "grill pan",
    "roasting pan",
    "pie dish",
    "loaf pan",
    "muffin tin",
    "pizza stone",
    "ramekin",
    "stockpot",
    "custard cup",
    "brotform"
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
    "pastry cutter",
    "mandoline slicer",
    "kitchen shears",
    "garlic press",
    "zester",
    "juicer",
    "meat tenderizer",
    "pastry brush",
    "bench scraper",
    "can opener",
    "bottle opener",
    "melon baller",
    "ice cream scoop",
    "mortar and pestle",
    "slotted spoon",
    "offset spatula",
    "pastry bag",
    "candy thermometer",
    "kitchen blowtorch",
    "egg slicer",
    "toaster",
    "blender",
    "food processor",
    "immersion blender",
    "electric mixer",
    "rice cooker",
    "pressure cooker",
    "sous-vide machine",
    "griddle",
    "tea strainer",
    "coffee grinder",
    "cheesecloth",
    "pizza cutter",
    "grill press",
    "baster",
    "splatter guard",
    "tamper",
    "spätzle maker"
]

HEALTHY_SUBSTITUTIONS = {
    # Proteins
    "ground beef": "lean ground turkey",
    "beef chuck": "lean beef round",
    "pork sausage": "turkey sausage",
    "pancetta": "lean turkey ham",
    "bacon": "turkey bacon",
    "chorizo": "chicken sausage",
    "lamb shank": "lean lamb shoulder",
    "hot dogs": "chicken sausages",
    "bologna": "lean turkey",
    "pepperoni": "turkey pepperoni",
    "pork tenderloin": "extra-lean pork tenderloin",

    # Dairy & Eggs
    "whole milk": "skim milk",
    "milk": "skim milk",
    "cream": "low-fat milk",
    "heavy cream": "evaporated skim milk",
    "sour cream": "low-fat Greek yogurt",
    "mayonnaise": "low-fat Greek yogurt",
    "cream cheese": "neufchâtel cheese",
    "butter": "olive oil",
    "salted butter": "unsalted butter",
    "margarine": "olive oil",
    "egg": "egg whites",
    "eggs": "egg whites",
    "egg yolks": "egg whites or cholesterol-free egg substitute",
    "ice cream": "frozen Greek yogurt",
    "whipped cream": "coconut whipped cream",

    # Oils & Fats
    "vegetable oil": "olive oil",
    "corn oil": "avocado oil",
    "canola oil": "avocado oil",
    "lard": "olive oil",

    # Sweeteners
    "brown sugar": "honey or coconut sugar",
    "white sugar": "erythritol or monk fruit sweetener",
    "granulated sugar": "erythritol or monk fruit sweetener",
    "refined sugar": "coconut sugar or date sugar",
    "powdered sugar": "monk fruit powdered sweetener",
    "maple syrup": "sugar-free maple syrup",
    "corn syrup": "sugar-free maple syrup",
    "molasses": "date syrup",

    # Flours & Grains
    "all-purpose flour": "whole wheat flour",
    "white flour": "whole wheat flour",
    "pastry flour": "whole wheat pastry flour",
    "bread crumbs": "whole wheat bread crumbs",
    "panko bread crumbs": "whole wheat panko bread crumbs",
    "white pasta": "whole wheat pasta",
    "white rice": "brown rice",
    "arborio rice": "brown rice or pearled barley",
    "pie shell": "whole wheat pie crust (or nut-based crust with no added sugar)",
    "spaghetti": "whole wheat spaghetti",
    "linguine": "whole wheat spaghetti",
    # Starches & Vegetables
    "french fries": "baked sweet potato fries",
    "potato chips": "baked veggie chips",

    # Baking & Desserts
    "chocolate chips": "dark chocolate chips (70%+ cacao)",
    "cocoa powder": "unsweetened cocoa powder",
    "cake frosting": "Greek yogurt-based frosting with fruit sweetener",

    # Nuts & Legumes
    "pecans": "walnuts",

    "salt": "himalayan seasalt",
    "thyme": "organic thyme (no change needed)",
    "sage leaves": "organic sage (no change needed)",
    "rosemary": "organic rosemary (no change needed)",

    # Other Ingredients
    "rum": "reduced-sugar rum flavoring or omit alcohol",
    "lemon, zested": "lemon zest (no change needed)",
    "fruit preserves": "no-sugar-added fruit preserves",

    # Toppings and spreads
    "barbecue sauce": "low-sugar barbecue sauce",
}



SUGAR_FREE_INGREDIENTS = [
    "chocolate chips",
    "chocolate syrup",
    "cocoa powder",
    "jam",
    "jelly",
    "ketchup",
    "maple syrup",
    "syrup",
    "pancake syrup",
    "marshmallows",
    "fudge",
    "candy",
    "caramel",
    "molasses",
    "agave nectar",
    "honey",
    "fruit preserves",
    "gelatin desserts",
    "cake frosting",
    "icing",
    "pie filling",
    "whipping cream",

]




SOUTH_ASIAN_PROTEIN_SUBSTITUTIONS = {
    # Red meats to leaner or regionally common meats
    "beef": "lamb",
    "pork": "chicken",
    "veal": "goat",
    "bacon": "turkey bacon",
    "prosciutto": "chicken",
    "ham": "turkey ham",
    "pancetta": "chicken",

    "salmon": "pomfret or rohu",
    "cod": "tilapia",
    "shrimp": "prawns",
    "lobster": "crab",

    "pepperoni": "spicy chicken sausage",
    "chorizo": "spicy chicken sausage",
    "bratwurst": "mutton sausage",
    "hot dogs": "chicken franks",

    "duck": "chicken",
    "turkey": "chicken",
    "cornish hen": "quail",

    "rabbit": "chicken",
    "venison": "goat"
}

SOUTH_ASIAN_CHEESE_SUBSTITUTIONS = {
    "parmesan cheese": "paneer",
    "Parmigiano-Reggiano": "paneer",
    "mozzarella": "paneer",
    "ricotta": "hung curd (strained yogurt)",
    "mascarpone": "malai (clotted cream)",
    "cream cheese": "paneer blended with yogurt",
    "feta": "paneer with a dash of lemon juice",
    "goat cheese": "crumbled paneer with mild vinegar",
    "blue cheese": "mild paneer",
    "cheddar": "mild paneer",
    "cream": "malai or coconut cream",
    "whipped cream": "whipped malai",
    "sour cream": "hung yogurt",
    "buttermilk": "thin lassi (salted)",
    "butter": "ghee"
}

# Eggs & Dairy
SOUTH_ASIAN_EGG_SUBSTITUTIONS = {
    "eggs": "beaten yogurt thickened with besan",
    "egg whites": "yogurt + water mixture",
    "whole milk": "coconut milk",
    "skim milk": "diluted buffalo milk",
}


SOUTH_ASIAN_BINDER_SUBSTITUTIONS = {
    "bread crumbs": "chickpea flour",
    "panko breadcrumbs": "chickpea flour",
    "italian bread crumbs": "roasted besan",
    "cornstarch": "arrowroot powder",
    "wheat flour": "atta",
    "all-purpose flour": "atta",
    "pastry flour": "maida",
    "cake flour": "maida + corn flour blend",
    "pasta": "basmati rice",
    "focaccia": "naan",
    "ciabatta": "tandoori roti",
    "baguette": "tawa roti ",
    "gnocchi": "idli",
    "couscous": "dalia (broken wheat)",
    "polenta": "upma (semolina)",
    "risotto rice": "gobindobhog rice",
    "tortillas": "rotis",
    "spaghetti": "sevai (rice vermicelli)",
    "rice noodles": "sevai (rice vermicelli)",
    "udon noodles": "wheat noodles"
}


HERB_SPICE_MAP = {
    "basil": "coriander",
    "oregano": "cumin",
    "thyme": "turmeric",
    "rosemary": "ginger",
    "parsley": "fresh cilantro",
    "sage": "cardamom",
    "marjoram": "garam masala"
}
SOUTH_ASIAN_OIL_SUBSTITUTIONS = {
    "olive oil": "ghee",
    "sunflower oil": "mustard oil",
    "peanut oil": "groundnut oil",
    "sesame oil": "gingelly oil",
    "butter": "ghee",
    "lard": "ghee",
    "shortening": "solidified ghee"
}

SOUTH_ASIAN_CONDIMENT_SUBSTITUTIONS = {
    "ketchup": "tomato chutney",
    "mayonnaise": "hung curd dip",
    "mustard": "kashundi (Bengali mustard sauce)",
    "soy sauce": "tamari",
    "worcestershire sauce": "imli (tamarind)",
    "balsamic vinegar": "tamarind pulp",
    "red wine vinegar": "cane vinegar",
    "white wine vinegar": "lemon juice",
    "white wine": "coconut vinegar",
    "red wine": "cane vinegar",
    "tabasco": "Naga chili sauce",
    "pesto": "mint-coriander chutney",
    "harissa": "red chili-garlic chutney",
    "salsa": "kachumber (tomato-onion) salad"
}

GLUTEN_SUBSTITUTIONS = {
    "bread crumbs": "gluten-free bread crumbs",
    "breadcrumbs": "gluten-free bread crumbs",
    "panko": "gluten-free panko",
    "flour": "rice flour",
    "roll": "gluten-free rolls",
    "pasta": "gluten-free pasta",
    "noodels": "gluten-free noodles",
    "spaghetti": "gluten-free spaghetti",
    "bread": "gluten-free bread",
    "crouton": "gluten-free croutons",
    "beer": "gluten-free beer",
    "torilla": "corn tortilla",
    "soy sauce": "tamari",
    "teriyaki sauce": "gluten-free teriyaki sauce",
}