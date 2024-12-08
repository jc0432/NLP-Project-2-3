from constants import LACTOSE_SUBSTITUTIONS
import json

def lactose_free(ingredient_list):
    for i in range(len(ingredient_list)):
        for start in range(len(ingredient_list[i])):
            found = False
            for end in range(len(ingredient_list[i]), start, -1):
                if ingredient_list[i][start:end].lower() in LACTOSE_SUBSTITUTIONS and ingredient_list[i] != LACTOSE_SUBSTITUTIONS[ingredient_list[i][start:end].lower()]:
                    print(ingredient_list[i] + " contains lactose, substituting it with " + LACTOSE_SUBSTITUTIONS[ingredient_list[i][start:end].lower()] + "!")
                    ingredient_list[i] = LACTOSE_SUBSTITUTIONS[ingredient_list[i][start:end].lower()]
                    found = True
                    break
            if found: break
    return ingredient_list

def main():
    # load recipe json
    recipe = None
    with open('recipe.json') as f:
        recipe = json.load(f)
    
    ingredients = recipe.get('ingredients', [])
    ingredients = [ingredient['ingredient'] for ingredient in ingredients]    
    lactose_free_ingredients = lactose_free(ingredients)

    # overwrite the ingredients in the recipe
    for i in range(len(ingredients)):
        recipe['ingredients'][i]['ingredient'] = lactose_free_ingredients[i]
    
    # save the recipe
    with open('recipe.json', 'w') as f:
        json.dump(recipe, f, indent=4)
    print("Lactose free ingredients saved to recipe.json")
        
if __name__ == '__main__':
    main()