"""
Quantity Converter Usage:

1. Parse ingredients:
ingredients = parser.parse_ingredients(recipe_text)

2. Convert quantities:
- Scale adjustment: parser.convert_recipe(ingredients, scale=2)  # 2 times
- Unit conversion: parser.convert_recipe(ingredients, unit='ml')  # unit conversion
- Combined usage: parser.convert_recipe(ingredients, scale=2, unit='ml')

3. Quick single ingredient parsing:
result = get_ingredient("2 cups flour, sifted")                    # basic parsing
result = get_ingredient("2 cups flour, sifted", scale_factor=2)    # scale up
result = get_ingredient("2 cups flour, sifted", target_unit='ml')  # convert unit
"""

import re  # add import statement

# directly define IngredientParser class
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
            'fluid ounce': {'unit': 'oz'},  # add
            'fluid ounces': {'unit': 'oz'}  # add
        }

    # Enhanced ingredient parsing
    def parse_single_ingredient(self, ingredient_str):
        parts = ingredient_str.split(',', 1)
        main_info = parts[0].strip().lower()
        prep_info = parts[1].strip() if len(parts) > 1 else ''
        
        # add special case handling
        if '(' in main_info:
            main_info = re.sub(r'\([^)]*\)', '', main_info)
        
        # check special phrases
        for phrase, values in self.special_phrases.items():
            if phrase in main_info:
                name = main_info.replace(phrase, '').replace('a ', '').strip()
                return {
                    'amount': values['amount'],
                    'unit': values['unit'],
                    'name': name,
                    'adjectives': [],
                    'prep': prep_info
                }
        
        # preprocess
        for word in self.common_words:
            main_info = main_info.replace(f' {word} ', ' ')
        
        # parse the quantity
        amount_match = re.search(r'^((?:\d+\s+)?\d+/\d+|\d+(?:\.\d+)?(?:\s*-\s*\d+)?)', main_info)
        amount = amount_match.group(1) if amount_match else ""
        main_info = main_info[len(amount):].strip() if amount else main_info
        
        # parse the unit and adjectives
        words = main_info.split()
        unit = ''
        adjectives = []
        name_parts = []
        
        for word in words:
            if word in self.converter.adjectives:
                adjectives.append(word)
            elif word in self.units and not unit:
                unit = word
            else:
                name_parts.append(word)
        
        # handle fluid ounces
        for phrase, values in self.special_phrases.items():
            if phrase in main_info and 'unit' in values:
                unit = values['unit']
                break
        
        return {
            'amount': amount,
            'unit': unit,
            'name': ' '.join(name_parts),
            'adjectives': adjectives,
            'prep': prep_info
        }
    
    def convert_recipe_quantities(self, ingredients, scale_factor=1, target_unit=None):
        return self.converter.convert_recipe_quantity(ingredients, scale_factor, target_unit)

class QuantityConverter:
    def __init__(self):
        # volume conversion (based on milliliters)
        self.volume_conversions = {
            'cup': 236.59,
            'cups': 236.59,
            'tablespoon': 14.79,
            'tablespoons': 14.79,
            'tbsp': 14.79,
            'teaspoon': 4.93,
            'teaspoons': 4.93,
            'tsp': 4.93,
            'ml': 1,
            'milliliter': 1,
            'milliliters': 1,
            'l': 1000,
            'liter': 1000,
            'liters': 1000,
            'dash': 0.62,
            'dashes': 0.62,
            'pinch': 0.31,
            'pinches': 0.31,
            'can': 354.88,
            'stick': 113.4,
        }
        
        # weight conversion (based on grams)
        self.weight_conversions = {
            'g': 1,
            'gram': 1,
            'grams': 1,
            'kg': 1000,
            'kilogram': 1000,
            'kilograms': 1000,
            'pound': 453.59,
            'pounds': 453.59,
            'lb': 453.59,
            'lbs': 453.59,
            'oz': 28.35,
            'ounce': 28.35,
            'ounces': 28.35
        }
        
        # non-convertible units
        self.non_convertible_units = {
            'whole',
            'piece',
            'pieces',
            'slice',
            'slices',
            'head',
            'heads',
            'clove',
            'cloves'
        }
        
        # adjectives list
        self.adjectives = {
            'large', 'medium', 'small',
            'fresh', 'dried', 'ground',
            'chopped', 'diced', 'minced',
            'sliced', 'grated', 'crushed'
        }
        
        # add fraction character mapping
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
            '\u00bd': '1/2',  
            '\u00bc': '1/4',  
            '\u00be': '3/4',  
        }

    def convert_fraction(self, fraction_str):
        # Handle fraction conversion, including special fraction characters
        try:
            # first check if it's a special fraction character
            if fraction_str in self.fraction_map:
                fraction_str = self.fraction_map[fraction_str]
            
            if ' ' in fraction_str:
                whole, frac = fraction_str.split()
                whole = float(whole)
                num, denom = map(int, frac.split('/'))
                return whole + (num / denom)
            elif '/' in fraction_str:
                num, denom = map(int, fraction_str.split('/'))
                return num / denom
            return float(fraction_str)
        except ValueError:
            print(f"Debug - Could not convert fraction: {fraction_str}")
            return None

    def parse_amount(self, amount_str):
        # parse the quantity, including fractions and ranges
        if not amount_str:
            return None
            
        if '-' in amount_str:
            start, end = amount_str.split('-')
            start_val = self.convert_fraction(start.strip())
            end_val = self.convert_fraction(end.strip())
            if start_val is not None and end_val is not None:
                return f"{start_val}-{end_val}"
        else:
            return self.convert_fraction(amount_str)
        
        return None

    def convert_recipe_quantity(self, ingredients, scale_factor=1, target_unit=None):
        converted = []
        for ing in ingredients:
            try:
                new_ing = ing.copy()
                amount = ing.get('amount', '')
                unit = ing.get('unit', '').lower()
                
                # handle special fraction characters
                if amount in self.fraction_map:
                    parsed_amount = self.convert_fraction(amount)
                    if parsed_amount:
                        new_amount = parsed_amount * scale_factor
                        new_ing['amount'] = f"{new_amount:.2f}".rstrip('0').rstrip('.')
                        converted.append(new_ing)
                        continue
                
                # handle the "a dash of" pattern
                if ing['name'].startswith('a dash'):
                    new_ing['amount'] = '1'
                    new_ing['unit'] = 'dash'
                    new_ing['name'] = ing['name'].replace('a dash of', '').strip()
                
                # handle the quantity conversion
                parsed_amount = self.parse_amount(amount)
                if parsed_amount:
                    if '-' in str(parsed_amount):
                        start, end = map(float, str(parsed_amount).split('-'))
                        new_amount = f"{start * scale_factor}-{end * scale_factor}"
                    else:
                        new_amount = float(parsed_amount) * scale_factor
                    new_ing['amount'] = str(new_amount)
                
                # handle the unit conversion
                if target_unit and unit in self.volume_conversions:
                    try:
                        value = float(new_ing['amount']) * self.volume_conversions[unit]
                        new_ing['amount'] = f"{value:.2f}".rstrip('0').rstrip('.')
                        new_ing['unit'] = target_unit
                    except ValueError as e:
                        print(f"Warning: Could not convert {amount} {unit}: {str(e)}")
                
                converted.append(new_ing)
            except Exception as e:
                print(f"Debug - Error converting ingredient: {e}")
                converted.append(ing)
                
        return converted

def adjust_quantity(ingredient_dict, adjustment_factor):
    # Interface for quantity adjustment called by health conversion functions
    converter = QuantityConverter()
    return converter.convert_recipe_quantity([ingredient_dict], scale_factor=adjustment_factor)[0]

# # Test code
# if __name__ == "__main__":
#     test_cases = [
#         "2 large eggs, beaten",
#         "3 cloves garlic, minced",
#         "1 head lettuce, chopped",
#         "2 1/4 cups all-purpose flour, sifted",
#         "1 stick butter, softened",
#         "2-3 medium carrots, diced",
#         "a dash of hot sauce",
#         "fresh basil to taste",
#         "1 can (14 oz) diced tomatoes",
#         "500 g ground beef"
#     ]

#     parser = IngredientParser()
#     for case in test_cases:
#         parsed = parser.parse_single_ingredient(case)
#         print(f"\nOriginal: {case}")
#         print(f"Parsed: {parsed}")
#         print(f"Double: {parser.convert_recipe_quantities([parsed], scale_factor=2)}")
#         print(f"Metric: {parser.convert_recipe_quantities([parsed], target_unit='ml')}")
