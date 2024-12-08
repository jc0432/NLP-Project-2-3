import json
import re
from constants import HEALTHY_SUBSTITUTIONS,SUGAR_FREE_INGREDIENTS

INVERSE_HEALTHY_SUBSTITUTIONS = {v: k for k, v in HEALTHY_SUBSTITUTIONS.items()}

def load_parsed_steps(filename="parsed_steps.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def apply_healthy_substitution(ingredient_name):

    ing_lower = ingredient_name.lower()
    for original, substitute in HEALTHY_SUBSTITUTIONS.items():
        if original in ing_lower:
            return substitute
    return ingredient_name

def apply_sugar_free_prefix(ingredient_name):
    normalized = ingredient_name.lower()
    for sugar_item in SUGAR_FREE_INGREDIENTS:
        if sugar_item in normalized:
            return "sugar-free " + ingredient_name
    return ingredient_name

def apply_unhealthy_substitution(ingredient_name):
    # Attempt to revert from a healthy substitution back to the original
    ing_lower = ingredient_name.lower()
    for healthy_ing, original in INVERSE_HEALTHY_SUBSTITUTIONS.items():
        if healthy_ing.lower() in ing_lower:
            return original
    return ingredient_name

def remove_sugar_free_prefix(ingredient_name):
    # If sugar-free prefix is present, remove it
    if ingredient_name.lower().startswith("sugar-free "):
        return ingredient_name[11:].strip()
    return ingredient_name
def transform_ingredients(ingredients_dict, to_healthy=True):
    transformed = {}
    for ing, amt in ingredients_dict.items():
        if to_healthy:
            new_ing = apply_healthy_substitution(ing)
            new_ing = apply_sugar_free_prefix(new_ing)
        else:
            # Reverse transformation
            new_ing = remove_sugar_free_prefix(ing)
            new_ing = apply_unhealthy_substitution(new_ing)
        transformed[new_ing] = amt
    return transformed

def transform_substeps(substeps, to_healthy=True):
    transformed_substeps = []

    if to_healthy:
        healthy_keys = sorted(HEALTHY_SUBSTITUTIONS.keys(), key=len, reverse=True)
        for substep in substeps:
            transformed_substep = substep
            # Apply healthy substitutions
            for original in healthy_keys:
                pattern = re.compile(r"\b" + re.escape(original) + r"\b", re.IGNORECASE)
                substitute = HEALTHY_SUBSTITUTIONS[original]
                transformed_substep = pattern.sub(substitute, transformed_substep)

            # Apply sugar-free
            for sugar_item in sorted(SUGAR_FREE_INGREDIENTS, key=len, reverse=True):
                pattern = re.compile(r"\b" + re.escape(sugar_item) + r"\b", re.IGNORECASE)
                transformed_substep = pattern.sub("sugar-free " + sugar_item, transformed_substep)

            transformed_substeps.append(transformed_substep)
    else:
 
        for substep in substeps:
            transformed_substep = substep
            for sugar_item in sorted(SUGAR_FREE_INGREDIENTS, key=len, reverse=True):
                pattern = re.compile(r"\bsugar-free\s+" + re.escape(sugar_item) + r"\b", re.IGNORECASE)
                transformed_substep = pattern.sub(sugar_item, transformed_substep)

            inverse_keys = sorted(INVERSE_HEALTHY_SUBSTITUTIONS.keys(), key=len, reverse=True)
            for healthy_ing in inverse_keys:
                pattern = re.compile(r"\b" + re.escape(healthy_ing) + r"\b", re.IGNORECASE)
                original = INVERSE_HEALTHY_SUBSTITUTIONS[healthy_ing]
                transformed_substep = pattern.sub(original, transformed_substep)

            transformed_substeps.append(transformed_substep)

    return transformed_substeps

def transform_methods(methods_dict, to_healthy=True):
    return methods_dict

def transform_parsed_steps(parsed_steps, to_healthy=True):
    transformed = []
    for step in parsed_steps:
        transformed_ingredients = transform_ingredients(step.get("ingredients", {}), to_healthy=to_healthy)
        transformed_methods = transform_methods(step.get("methods", {}), to_healthy=to_healthy)
        transformed_substeps = transform_substeps(step.get("substeps", []), to_healthy=to_healthy)

        # Update direction from transformed_substeps
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

def save_transformed_steps(transformed_steps, filename="healthy_transformed_parsed_steps.json"):
    with open(filename, 'w') as f:
        json.dump(transformed_steps, f, indent=4)


def transform_healthy(to_healthy = True):
    parsed_steps = load_parsed_steps("parsed_steps.json")
    healthier_steps = transform_parsed_steps(parsed_steps, to_healthy= to_healthy)
    if to_healthy: save_transformed_steps(healthier_steps, "healthier_parsed_steps.json")
    else: save_transformed_steps(healthier_steps, "unhealthier_parsed_steps.json")

    print(f"Transformed recipe steps have been saved.")

if __name__ == "__main__":
    parsed_steps = load_parsed_steps("parsed_steps.json")

    healthier_steps = transform_parsed_steps(parsed_steps)

    save_transformed_steps(healthier_steps, "healthier_parsed_steps.json")

    print(f"Transformed recipe steps have been saved.")
