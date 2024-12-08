"""
Quantity Converter Usage:
- Scale adjustment: converter.convert_recipe_quantity(ingredients, scale=2)  # 2 times
- Unit conversion: converter.convert_recipe_quantity(ingredients, unit='ml')  # unit conversion
- Combined usage: converter.convert_recipe_quantity(ingredients, scale=2, unit='ml')
"""

import re

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
            'whole', 'piece', 'pieces', 'slice', 'slices',
            'head', 'heads', 'clove', 'cloves'
        }
        
        # fraction character mapping
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
            '\u00bd': '1/2',  # ½
            '\u00bc': '1/4',  # ¼
            '\u00be': '3/4',  # ¾
        }

    def convert_fraction(self, fraction_str):
        try:
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
    converter = QuantityConverter()
    return converter.convert_recipe_quantity([ingredient_dict], scale_factor=adjustment_factor)[0]
