import json
import re
import sys
from constants import (
    SOUTH_ASIAN_PROTEIN_SUBSTITUTIONS,
    SOUTH_ASIAN_CHEESE_SUBSTITUTIONS,
    SOUTH_ASIAN_BINDER_SUBSTITUTIONS,
    SOUTH_ASIAN_OIL_SUBSTITUTIONS,
    HERB_SPICE_MAP,
    SOUTH_ASIAN_CONDIMENT_SUBSTITUTIONS
)

SOUTH_ASIAN_SUBSTITUTIONS = {
    **SOUTH_ASIAN_PROTEIN_SUBSTITUTIONS,
    **SOUTH_ASIAN_CHEESE_SUBSTITUTIONS,
    **SOUTH_ASIAN_BINDER_SUBSTITUTIONS,
    **HERB_SPICE_MAP,
    **SOUTH_ASIAN_OIL_SUBSTITUTIONS,
    **SOUTH_ASIAN_CONDIMENT_SUBSTITUTIONS
}


def load_parsed_steps(filename="parsed_steps.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def to_south_asian_ingredient(ingredient_name):
    ing_lower = ingredient_name.lower()
    for original, substitute in SOUTH_ASIAN_SUBSTITUTIONS.items():
        if original in ing_lower:
            return substitute
    return ingredient_name

def transform_ingredients(ingredients_dict):
    transformed = {}
    for ing, amt in ingredients_dict.items():
        new_ing = to_south_asian_ingredient(ing)
        transformed[new_ing] = amt
    return transformed

def transform_substeps(substeps):
    transformed_substeps = []
    all_keys = sorted(SOUTH_ASIAN_SUBSTITUTIONS.keys(), key=len, reverse=True)
    for substep in substeps:
        transformed_substep = substep
        for original in all_keys:
            pattern = re.compile(r"\b" + re.escape(original) + r"\b", re.IGNORECASE)
            substitute = SOUTH_ASIAN_SUBSTITUTIONS[original]
            transformed_substep = pattern.sub(substitute, transformed_substep)
        transformed_substeps.append(transformed_substep)
    return transformed_substeps

def transform_methods(methods_dict):
    for method, details in methods_dict.items():
        if 'subject' in details and isinstance(details['subject'], list):
            transformed_subjects = []
            for subj in details['subject']:
                transformed_subjects.append(to_south_asian_ingredient(subj))
            details['subject'] = transformed_subjects
    return methods_dict


def transform_parsed_steps(parsed_steps):
    transformed = []
    for step in parsed_steps:
        transformed_ingredients = transform_ingredients(step.get("ingredients", {}))
        transformed_methods = transform_methods(step.get("methods", {}))

        transformed_substeps = transform_substeps(step.get("substeps", []))

        transformed_direction = '. '.join(transformed_substeps)
        if not transformed_direction.endswith('.'):
            transformed_direction += '.'

        new_step = {
            "step_number": step["step_number"],
            "direction": transformed_direction,
            "ingredients": transformed_ingredients,
            "tools": step["tools"],
            "methods": transformed_methods,
            "substeps": transformed_substeps
        }
        transformed.append(new_step)
    return transformed

def save_transformed_steps(transformed_steps, filename="south_asian_transform_parsed_steps.json"):
    with open(filename, 'w') as f:
        json.dump(transformed_steps, f, indent=4)

def transform_cuisine_sa():
    parsed_steps = load_parsed_steps("parsed_steps.json")
    transformed_steps = transform_parsed_steps(parsed_steps)
    save_transformed_steps(transformed_steps, "south_asian_parsed_steps.json")
    print("Transformed recipe steps have been saved to 'south_asian_parsed_steps.json'.")

if __name__ == "__main__":
    parsed_steps = load_parsed_steps("parsed_steps.json")
    transformed_steps = transform_parsed_steps(parsed_steps)
    save_transformed_steps(transformed_steps, "south_asian_parsed_steps.json")
    print("Transformed recipe steps have been saved to 'south_asian_parsed_steps.json'.")
