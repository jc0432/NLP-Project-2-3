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
