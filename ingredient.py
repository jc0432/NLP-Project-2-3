from Test import ingredient_parser, get_recipe_page
import re
from quantity_converter import QuantityConverter, IngredientParser as QCIngredientParser

def get_ingredients(url, scale_factor=1.0, target_unit=None):
    try:
        print(f"Debug - Attempting to fetch URL: {url}")
        recipe_page_content = get_recipe_page(url)
        
        if recipe_page_content is None:
            print("Error: Unable to fetch recipe page content")
            return []
            
        raw_ingredients = ingredient_parser(recipe_page_content)
        
        formatted_ingredients = []
        converter = QuantityConverter()
        
        for ing in raw_ingredients:
            try:
                # separate the amount and ingredient
                amount_str = ing.amount.strip() if hasattr(ing, 'amount') else ""
                ingredient = ing.ingredient.strip() if hasattr(ing, 'ingredient') else ""
                
                # handle special fraction characters in the amount
                amount = amount_str
                unit = ""
                
                # separate the unit from the amount
                if ' ' in amount_str:
                    parts = amount_str.split(' ', 1)
                    amount = parts[0]
                    unit = parts[1] if len(parts) > 1 else ""
                
                # check if the ingredient name contains special fraction characters
                for fraction_char, fraction_value in converter.fraction_map.items():
                    if fraction_char in amount:
                        amount = fraction_value
                    if fraction_char in ingredient:
                        if not amount:
                            amount = fraction_value
                        ingredient = ingredient.replace(fraction_char, '').strip()
                
                # standardize the unit format
                if unit.lower() in ['cup', 'cups']:
                    unit = 'cup'
                elif unit.lower() in ['tablespoon', 'tablespoons', 'tbsp']:
                    unit = 'tablespoon'
                elif unit.lower() in ['teaspoon', 'teaspoons', 'tsp']:
                    unit = 'teaspoon'
                
                formatted_ing = {
                    'amount': amount,
                    'unit': unit,
                    'name': ingredient,
                    'prep': ing.preparation if hasattr(ing, 'preparation') else ''
                }
                
                formatted_ingredients.append(formatted_ing)
                
            except Exception as e:
                print(f"Debug - Error processing ingredient: {e}")
                continue
        
        # use QuantityConverter to convert
        if scale_factor != 1.0:
            try:
                converted = converter.convert_recipe_quantity(
                    formatted_ingredients, 
                    scale_factor=scale_factor,
                    target_unit=target_unit
                )
                return converted
            except Exception as e:
                print(f"Debug - Error converting quantities: {e}")
                return formatted_ingredients
            
        return formatted_ingredients
        
    except Exception as e:
        print(f"Error fetching recipe: {str(e)}")
        return []


def transform_recipe_quantity(recipe_ingredients, scale_factor=1.0):
    # Transform recipe quantities for health transformations
    converter = QuantityConverter()
    parser = QCIngredientParser()
    
    transformed_ingredients = []
    for ing in recipe_ingredients:
        try:
            # ensure the input format is correct
            if isinstance(ing, str):
                parsed = parser.parse_single_ingredient(ing)
            else:
                parsed = ing
            
            # use quantity_converter to convert
            converted = converter.convert_recipe_quantity(
                [parsed], 
                scale_factor=scale_factor
            )
            transformed_ingredients.extend(converted)
            
        except Exception as e:
            print(f"Debug - Error transforming ingredient: {e}")
            transformed_ingredients.append(ing)
    
    return transformed_ingredients

def clean_ingredient_name(text, unit_match, descriptors):
    # clean and format the ingredient name
    name = text
    
    # remove the unit
    if unit_match:
        name = re.sub(unit_match.group(), '', name)
    
    # remove the descriptors
    for desc in descriptors:
        name = name.replace(desc, '')
    
    # remove the content in the parentheses and the content after the comma
    name = re.sub(r'\([^)]*\)', '', name)
    if ',' in name:
        name = name.split(',')[0]
    
    # handle special cases
    if "reduced-fat" in name:
        name = "cream of chicken soup"
        descriptors.append("reduced-fat")
    
    # clean and return
    return re.sub(r'\s+', ' ', name).strip()

def extract_preparation(text, descriptors):
    # extract the preparation method
    prep_parts = []
    
    # extract the preparation method from the descriptors
    prep_descriptors = [d for d in descriptors if d in [
        "chopped", "minced", "sliced", "diced", "grated", 
        "shredded", "crushed", "ground", "beaten", "peeled", "cubed"
    ]]
    if prep_descriptors:
        prep_parts.extend(prep_descriptors)
    
    # extract other preparation methods
    if ',' in text:
        prep_text = text.split(',', 1)[1].strip()
        if prep_text and prep_text not in prep_parts:
            prep_parts.append(prep_text)
    
    return ", ".join(prep_parts)

class IngredientParser:
    def __init__(self):
        self.quantity_converter = QuantityConverter()
        self.units = set(self.quantity_converter.volume_conversions.keys() | 
                        self.quantity_converter.weight_conversions.keys() | 
                        self.quantity_converter.non_convertible_units)
        
        # add common adjectives
        self.adjectives = {
            'large', 'medium', 'small', 'fresh', 'dried',
            'ground', 'chopped', 'diced', 'minced', 'sliced',
            'grated', 'crushed'
        }
        
        self.fraction_map = {
            '½': '1/2',
            '¼': '1/4', 
            '¾': '3/4',
            '⅓': '1/3',
            '⅔': '2/3',
            '⅛': '1/8',
            '⅜': '3/8',
            '⅝': '5/8',
            '⅞': '7/8',
        }

    def parse_single_ingredient(self, text):
        text = text.lower().strip()
        
        # separate the preparation method
        parts = [p.strip() for p in text.split(',')]
        main_part = parts[0]
        preparations = parts[1:] if len(parts) > 1 else []
        
        # handle the "a dash of" pattern
        if 'a dash of' in main_part:
            return {
                'amount': '1',
                'unit': 'dash',
                'name': main_part.replace('a dash of', '').strip(),
                'adjectives': [],
                'prep': preparations
            }
        
        # handle the quantity
        amount_match = re.search(r'^((?:\d+\s+)?\d+/\d+|\d+(?:\.\d+)?(?:\s*-\s*\d+)?)', main_part)
        amount = amount_match.group(1) if amount_match else ""
        main_part = main_part[len(amount):].strip() if amount else main_part
        
        # handle the unit and name
        words = main_part.split()
        unit = ''
        name_parts = []
        adjectives = []
        
        for word in words:
            if word in self.units and not unit:
                unit = word
            elif word in self.adjectives:
                adjectives.append(word)
            else:
                name_parts.append(word)
        
        return {
            'amount': amount,
            'unit': unit,
            'name': ' '.join(name_parts),
            'adjectives': adjectives,
            'prep': preparations
        }

if __name__ == "__main__":
    test_url = "https://www.allrecipes.com/recipe/273864/greek-chicken-skewers/"
    
    try:
        print("\nTesting webpage parsing:")
        ingredients = get_ingredients(test_url)
        if ingredients:
            print(f"\nRetrieved ingredients:")
            for ing in ingredients:
                print(ing)
            
            print("\nDouble portion:")
            double_ingredients = get_ingredients(test_url, scale_factor=2.0)
            if double_ingredients:
                for ing in double_ingredients:
                    print(ing)
            else:
                print("Unable to get double portion ingredients")
        else:
            print("Unable to get ingredient list")
            print("Please check the debug information above for specific reasons")
    except Exception as e:
        print(f"Error testing URL: {str(e)}")
