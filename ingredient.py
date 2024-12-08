from Test import ingredient_parser, get_recipe_page
import re
from quantity_converter import QuantityConverter

def get_ingredients(url, scale_factor=1.0, target_unit=None):
    try:
        recipe_page_content = get_recipe_page(url)
        if not recipe_page_content:
            raise ValueError("Unable to fetch recipe page content")
            
        raw_ingredients = ingredient_parser(recipe_page_content)
        formatted_ingredients = []
        converter = QuantityConverter()
        parser = IngredientParser()
        
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
    parser = IngredientParser()
    
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
    name = text
    if unit_match:
        name = re.sub(unit_match.group(), '', name)
    
    for desc in descriptors:
        name = name.replace(desc, '')
    
    name = re.sub(r'\([^)]*\)', '', name)
    if ',' in name:
        name = name.split(',')[0]
    
    # handle special cases
    if "reduced-fat" in name:
        name = "cream of chicken soup"
        descriptors.append("reduced-fat")
    
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
        self.converter = QuantityConverter()
        # expand the unit set
        self.units = set(self.converter.volume_conversions.keys() | 
                        self.converter.weight_conversions.keys() |
                        {'piece', 'pieces', 'slice', 'slices', 'package', 'pkg'})
        
        # add more descriptors
        self.adjectives = {
            'large', 'medium', 'small', 'fresh', 'dried', 'ground',
            'chopped', 'diced', 'minced', 'sliced', 'grated', 'crushed',
            'frozen', 'ripe', 'raw', 'cooked', 'cold', 'hot', 'warm',
            'softened', 'melted', 'beaten', 'peeled', 'cubed'
        }
        
        # add common words
        self.common_words = {'of', 'a', 'an', 'the'}
        
        # keep special phrase handling
        self.special_phrases = {
            'dash of': {'amount': '1', 'unit': 'dash'},
            'pinch of': {'amount': '1', 'unit': 'pinch'},
            'to taste': {'amount': '', 'unit': ''},
            'fluid ounce': {'unit': 'oz'},
            'fluid ounces': {'unit': 'oz'}
        }
        
        # fraction mapping
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
        
        # check special phrases
        for phrase, values in self.special_phrases.items():
            if phrase in main_part:
                name = main_part.replace(phrase, '').replace('a ', '').strip()
                return {
                    'amount': values['amount'],
                    'unit': values['unit'],
                    'name': name,
                    'adjectives': [],
                    'prep': preparations
                }
        
        # preprocess
        for word in self.common_words:
            main_part = main_part.replace(f' {word} ', ' ')
        
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
        
        # handle fluid ounces
        for phrase, values in self.special_phrases.items():
            if phrase in main_part and 'unit' in values:
                unit = values['unit']
                break
        
        return {
            'amount': amount,
            'unit': unit,
            'name': ' '.join(name_parts),
            'adjectives': adjectives,
            'prep': preparations
        }

# if __name__ == "__main__":
#     test_url = "https://www.allrecipes.com/recipe/260065/instant-pot-lasagna/"
    
#     def print_ingredients(ingredients, title):
#         print(f"\n{title}:")
#         for ing in ingredients:
#             print(ing)
    
#     try:
#         ingredients = get_ingredients(test_url)
#         if not ingredients:
#             print("Unable to get recipe")
#             exit()
            
#         print_ingredients(ingredients, "original recipe")
        
#         double_ingredients = get_ingredients(test_url, scale_factor=2.0)
#         print_ingredients(double_ingredients, "double portion")
        
#     except Exception as e:
#         print(f"Error: {e}")
