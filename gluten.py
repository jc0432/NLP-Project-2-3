# transforms a list of ingredients to gluten free
from constants import GLUTEN_SUBSTITUTIONS
import json
def gluten_free(ingredient_list):
    for i in range(len(ingredient_list)):
        for start in range(len(ingredient_list[i])):
            found = False
            for end in range(len(ingredient_list[i]), start, -1):
                if ingredient_list[i][start:end].lower() in GLUTEN_SUBSTITUTIONS:
                    ingredient_list[i] = GLUTEN_SUBSTITUTIONS[ingredient_list[i][start:end].lower()]
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
    print(ingredients)
    
    gluten_free_ingredients = gluten_free(ingredients)
    print(gluten_free_ingredients)
    
if __name__ == '__main__':
    main()