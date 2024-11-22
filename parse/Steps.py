import json
import re
import spacy
from constants import DURATION_METHODS, NO_DURATION_METHODS, STEP_STOP_WORDS, REFERENCE_WORDS, NAMES, TOOLS
from .gadgets import get_gadgets_single
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
    prev_subjects = []
    
    doc_ptr = 0
    while doc_ptr < len(doc):
        token = doc[doc_ptr]
        if token.text.lower() in STEP_STOP_WORDS:
            doc_ptr += 1
            continue
        if token.tag_ == "VB" and (token.lemma_.lower() in DURATION_METHODS or token.lemma_.lower() in NO_DURATION_METHODS):
            # print("@@@@@@ ", token)
            print("found token", token)
            method = token.lemma_.lower()
            subjects = []
            duration = None
            until_condition = None

            # go through tokens until another verb or a period is found
            next_ptr = doc_ptr + 1
            stops = STEP_STOP_WORDS + REFERENCE_WORDS
            while(next_ptr < len(doc) and 
                  doc[next_ptr].tag_ != "VB" and 
                  doc[next_ptr].text != "." and 
                  doc[next_ptr].text.lower() not in stops):
                next_doc = doc[next_ptr]
                if next_doc.dep_ in ("dobj", "pobj", "nsubj", "appos"):
                    subjects.append(doc[next_ptr].text)
                    print("added subject", doc[next_ptr].text, doc[next_ptr].dep_)
                    # for conj in doc[next_ptr].conjuncts:
                    #     subjects.append(conj.text)
                next_ptr += 1
            doc_ptr = next_ptr
            if subjects: 
                prev_subjects = subjects
            subjects = prev_subjects
            print("subjects", subjects)

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
        doc_ptr += 1
    
    # for token in doc:
    #     if token.tag_ == "VB" and (token.lemma_.lower() in DURATION_METHODS or token.lemma_.lower() in NO_DURATION_METHODS):
    #         # print("@@@@@@ ", token)
    #         print("found token", token)
    #         method = token.lemma_.lower()
    #         subjects = []
    #         duration = None
    #         until_condition = None

    #         # go through tokens until another verb or a period is found
    #         for i in range(token.i+1, len(doc)):
    #             if doc[i].tag_ == "VB" or doc[i].text == ".":
    #                 break
    #             print("doc", doc[i], doc[i].dep_)
    #             if doc[i].dep_ in ("dobj", "pobj", "nsubj", "appos"):
    #                 subjects.append(doc[i].text)
    #                 for conj in doc[i].conjuncts:
    #                     subjects.append(conj.text)

    #         if subjects: 
    #             prev_subjects = subjects
    #         subjects = prev_subjects
    #         print("subjects", subjects)

    #         # Find duration
    #         if method in DURATION_METHODS:
    #             for ent in doc.ents:
    #                 if ent.label_ in ["TIME", "QUANTITY"] and ent.start > token.i:
    #                     duration = ent.text
    #                     break

    #         # Assign "until..." condition
    #         for until_start, until_text in until_phrases:
    #             if until_start > direction.lower().find(token.text.lower()):
    #                 until_condition = until_text
    #                 until_phrases.remove((until_start, until_text))  # Avoid reuse
    #                 break
    #         methods[method] = {
    #             "subject": subjects,
    #             "duration": duration,
    #             "until": until_condition
    #         }

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
        with open('../resFiles/recipe.json', 'r') as f:
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

    with open('../resFiles/parsed_steps.json', 'w') as f:
        json.dump(parsed_steps, f, indent=4)
    print("\nParsed steps have been saved to 'parsed_steps.json'.")

    
