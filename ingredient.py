from Test import ingredient_parser, get_recipe_page
import re

class Ingredient:
    def __init__(self, name, quantity='', unit='', descriptor='', preparation=''):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.descriptor = descriptor
        self.preparation = preparation
    
    def __str__(self):
        parts = []
        if self.quantity:
            parts.append(str(self.quantity))
        if self.unit:
            parts.append(self.unit)
        if self.descriptor:
            parts.append(self.descriptor)
        parts.append(self.name)
        if self.preparation:
            parts.append(f"({self.preparation})")
        return " ".join(parts)

def get_ingredients(url: str) -> str:
   # parse recipe url and return formatted ingredient list string
    try:
        unit_pattern = r'\b(cup|cups|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|tsp|pound|pounds|ounce|ounces|oz|gram|grams|g|pinch|pinches|dash|dashes|piece|pieces|slice|slices|whole|package|pkg|can|cans)\b'
        descriptor_pattern = r'\b(fresh|dried|chopped|minced|sliced|diced|grated|crushed|ground|whole|frozen|large|medium|small|ripe|raw|cooked|cold|hot|warm|softened|melted)\b'
        
        soup = get_recipe_page(url)
        raw_ingredients = ingredient_parser(soup)
        
        result = ["ingredients："]
        for ing in raw_ingredients:
            quantity = ing.amount.strip()
            ingredient_text = ing.ingredient.lower()
            
            unit_match = re.search(unit_pattern, ingredient_text)
            unit = unit_match.group(1) if unit_match else ''
            
            descriptors = re.findall(descriptor_pattern, ingredient_text)
            descriptor = ', '.join(descriptors)
            
            name = ingredient_text
            if unit:
                name = re.sub(unit_pattern, '', name)
            if descriptor:
                name = re.sub(descriptor_pattern, '', name)
            
            name = re.sub(r'\s+', ' ', name).strip()
            
            ingredient = Ingredient(
                name=name,
                quantity=quantity,
                unit=unit,
                descriptor=descriptor,
                preparation=ing.preparation.strip() if ing.preparation else ''
            )
            result.append(f"- {ingredient}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error parsing ingredients: {e}"


# test code
# if __name__ == "__main__":
#     test_urls = [
#         'https://www.allrecipes.com/recipe/256288/chef-johns-creamy-corn-pudding/',
#         'https://www.allrecipes.com/recipe/18379/best-green-bean-casserole/',
#         'https://www.allrecipes.com/recipe/217149/americano-cocktail/'
#     ]
 
#     for url in test_urls:
#         try:
#             print(f"\nrecipe: {url.split('/')[-2].replace('-', ' ').title()}")
#             print(get_ingredients(url))
#             print("\n" + "-"*50)
#         except Exception as e:
#             print(f"Error parsing ingredients: {e}")
