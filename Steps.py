import json
import re
import spacy
from constants import TOOLS, DURATION_METHODS, NO_DURATION_METHODS
from gadgets import get_gadgets_single
nlp = spacy.load("en_core_web_trf")



def parse_step(step, ingredient_list):
    direction = step['direction']
    step_number = step['step']
    doc = nlp(direction)
    methods = {}
    ingredients = {}

    # Extract "until..." phrases
    until_phrases = []
    if "until" in direction.lower():
        until_start = direction.lower().find("until")
        until_phrase = re.search(r"until (.*?)([.,;]|$)", direction[until_start:], re.IGNORECASE)
        if until_phrase:
            until_phrases.append((until_start, until_phrase.group(1).strip()))

    # Extract tools
    gadgets = get_gadgets_single(direction)
    gadgets = [gadget.to_dict() for gadget in gadgets]
    # Extract methods and their details
    for token in doc:
        if token.tag_ == "VB" and (token.lemma_.lower() in DURATION_METHODS or token.lemma_.lower() in NO_DURATION_METHODS):
            # print("@@@@@@ ", token)
            method = token.lemma_.lower()
            subjects = []
            duration = None
            until_condition = None

            # Find the subject
            for child in token.children:
                if child.dep_ in ("dobj", "pobj", "nsubj"):
                    subjects.append(child.text)
                    for conj in child.conjuncts:
                        subjects.append(conj.text)

            # Find duration
            if method in DURATION_METHODS:
                for ent in doc.ents:
                    if ent.label_ in ["TIME", "QUANTITY"] and ent.start > token.i:
                        duration = ent.text
                        break

            # Assign "until..." condition
            for until_start, until_text in until_phrases:
                if until_start > direction.lower().find(token.text.lower()):
                    until_condition = until_text
                    until_phrases.remove((until_start, until_text))  # Avoid reuse
                    break

            methods[method] = {
                "subject": subjects,
                "duration": duration,
                "until": until_condition
            }

    for ing in ingredient_list:
        pattern = rf'(\d+\/?\d*\s?(?:cups?|teaspoons?|tablespoons?|grams?|ounces?|pounds?|cloves?|slices?|pinches?))?\s+{re.escape(ing["ingredient"].lower())}'
        match = re.search(pattern, direction.lower())
        if match:
            ingredients[ing["ingredient"]] = match.group(1) 

    return {
        "step_number": step_number,
        "direction": direction,
        "ingredients": ingredients,
        "tools": gadgets,
        "methods": methods
    }


def parse_and_save():
    try:
        with open('recipe.json', 'r') as f:
            recipe_data = json.load(f)
    except FileNotFoundError:
        print("Error: 'recipe.json' file not found. Please run the scraping script first to generate 'recipe.json'.")
        return

    ingredients = recipe_data.get('ingredients', [])

    # Parse each step
    parsed_steps = []
    # print("\n### Parsed Steps ###")
    for step in recipe_data.get('steps', []):
        parsed = parse_step(step, ingredients)
        parsed_steps.append(parsed)
        # print(f"\nStep {parsed['step_number']}: {parsed['direction']}")
        # print(f"  Ingredients: {parsed['ingredients']}")
        # print(f"  Tools: {parsed['tools']}")
        # print(f"  Methods: {parsed['methods']}")

    with open('parsed_steps.json', 'w') as f:
        json.dump(parsed_steps, f, indent=4)
    print("\nParsed steps have been saved to 'parsed_steps.json'.")

    
