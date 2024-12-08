import json
import re
import spacy 
import warnings
warnings.filterwarnings("ignore")
nlp = spacy.load("en_core_web_trf")


# Open and load the JSON file
with open('recipe.json', 'r') as file:
    data = json.load(file)
    
def split_into_substeps(direction):
    substeps = []
    for step in direction['direction'].split('. '):
        if step.strip():  # Ensure the step is not empty
            # Add a period only if the step doesn't already end with one
            formatted_step = step.strip()
            if not formatted_step.endswith('.'):
                formatted_step += '.'
            substeps.append(formatted_step)
    return substeps

# Transform the steps to include substeps
for step in data['steps']:
    step['substeps'] = split_into_substeps(step)


# Regex patterns for non-vegetarian foods 
fish_regex = r"(?:\w+\s+)*\b(salmon|tuna|cod|trout|mackerel|sardines|haddock|halibut|snapper|sole|bass|herring|tilapia|swordfish|grouper)(?:\s+\w+)*\b"

meat_regex = r"(?:\w+\s+)*\b(steak|beef|roast beef|ground beef|ham|pork|bacon|ribs|bacon|ham|sausage|pork chops|loin|lamb chops|leg of lamb|ground lamb|veal cutlets|veal roast|venison|bison|elk|boar)(?:\s+\w+)*\b"

poultry_regex = r"(?:\w+\s+)*\b(chicken|breast|thighs|drumsticks|wings|turkey|ground turkey|duck|goose|quail|pheasant)(?:\s+\w+)*\b"

other = r"(?:\w+\s+)*\b(eel|unagi|monkfish|skate|ray wings|roe|caviar|tobiko|whelk|periwinkles|sea urchin|uni|abalone|geoduck|scallops|cuttlefish|barracuda|anchovies|grouper|lamprey|sweetbreads|tripe|oxtail|offal|liver|kidney|heart|tongue|bone marrow|black pudding|blood sausage|lardo|snails|escargot|kangaroo|alligator|crocodile|rabbit|hare|guinea pig|cuy|frog legs|horse meat|turtle|boar|elk|antelope|snake|rattlesnake|squab|capon|guinea fowl|emu|ostrich|partridge|pigeon|ptarmigan|pheasant|woodcock|snipe|grouse|peacock|turkey tails)(?:\s+\w+)*\b"


# Common substitions 
vegetarian_whole_items_regex = r"\b(tofu|tempeh|seitan|jackfruit|beyond meat|impossible burger|veggie burger|cauliflower steak|eggplant|paneer)\b"
vegetarian_piece_items_regex = r"\b(mushrooms|lentils|black beans|chickpeas|quinoa|textured vegetable protein|soy curls|nuts|walnuts|cashews|rice)\b"

cooking_verbs_regex = r"\b(roast|baste|smoke|carve|spit-roast|butterfly|truss|barbecue|broil|sear|spatchcock|score|dry-brine|cure|rest)\b"


def verb_type(sentence, food): 
    doc = nlp(sentence) 
    for token in doc:
        if token.pos_ == 'VERB' and token.dep_== 'ROOT':
            if re.search(cooking_verbs_regex, token.text, re.IGNORECASE):
                if re.search('meat', sentence):
                    substition = 'beyond meat'
                if re.search('burger', sentence, re.IGNORECASE):
                    substition = 'veggie burger'
                if re.search('steak', sentence, re.IGNORECASE):
                    substition = 'cauliflower steak'
                else:
                    substition = 'eggplant'
        if re.search('broth', food, re.IGNORECASE):
            substition = 'vegetarian broth'
        else:
            substition = 'tofu'
    new_sentence = re.sub(food, substition, sentence)
    return (new_sentence, sentence, substition)
    

def identify_non_veg_items(recipe):
    vegetarian_flags = {'Fish': [], "Poultry": [], "Meat": [], 'Other': []}
    recipe_ingredients = recipe['ingredients']
    for item in recipe_ingredients: 
        ingredient = item['ingredient']
        if re.search(fish_regex, ingredient, re.IGNORECASE):
            match = re.search(fish_regex, ingredient, re.IGNORECASE)
            vegetarian_flags['Fish'].append(match.group(1))
        if re.search(poultry_regex, ingredient, re.IGNORECASE):
            match = re.search(poultry_regex, ingredient, re.IGNORECASE)
            vegetarian_flags['Poultry'].append(match.group(1))
        if re.search(meat_regex, ingredient, re.IGNORECASE):
            match = re.search(meat_regex, ingredient, re.IGNORECASE)
            vegetarian_flags['Meat'].append(match.group(1))
        if re.search(other, ingredient, re.IGNORECASE):
            match = re.search(other, ingredient, re.IGNORECASE)
            vegetarian_flags['Other'].append(match.group(1))
    return vegetarian_flags

def adjust_steps(new_sentence, original_sentence, substeps):
    updated_substeps = [
        substep.replace(original_sentence, new_sentence) if original_sentence in substep else substep
        for substep in substeps
    ]
    return updated_substeps

def adjust_information(recipe, food, substitution): 
    # pattern = fr"\b(?:{re.escape(food.split()[0])}\s+)?{re.escape(substitution)}\b"
    for item in recipe['ingredients']:
        if re.search(food, item['ingredient'], re.IGNORECASE):
            item['ingredient'] = substitution
    if re.search(food, recipe['title'], re.IGNORECASE):
        recipe['title'] = re.sub(food, substitution, recipe['title'], flags=re.IGNORECASE)
        # print(recipe['title'])
    # print(recipe)

def find_replacement(recipe, flagged_food):
    for key in flagged_food:
        if flagged_food[key] != None: 
            for food in flagged_food[key]:
                for step in recipe['steps']: 
                    for i, substep in enumerate(step['substeps']):  
                        new_sentence, original_sentence, substitution =  verb_type(substep, food)
                        if new_sentence != original_sentence:
                            step['substeps'][i] = new_sentence
                    step['direction'] = " ".join(step['substeps'])
                    adjust_information(recipe, food, substitution)               

def main(): 
    recipe = data 
    dict_of_flags = identify_non_veg_items(recipe)
    find_replacement(recipe, dict_of_flags)
    return recipe

returned = main()
print(returned)