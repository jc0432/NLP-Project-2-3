from Test import ingredient_parser, get_recipe_page
import re

# create Ingredient class
class Ingredient:
    def __init__(self, ingredient="", amount="", preparation=""):
        self.ingredient = ingredient
        self.amount = amount
        self.preparation = preparation

# fix Test module
import Test
Test.Ingredient = Ingredient

class IngredientParser:
    def __init__(self):
        # expand unit pattern to include more possible units
        self.unit_pattern = r'\b(cup|cups|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|to taste|tsp|pound|pounds|ounce|ounces|oz|gram|grams|g|pinch|pinches|dash|dashes|piece|pieces|slice|slices|whole|package|pkg|can|cans)\b'
        # expand descriptor pattern to include more possible preparation methods
        self.descriptor_pattern = r'\b(fresh|dried|chopped|minced|sliced|diced|grated|shredded|crushed|ground|whole|frozen|large|medium|small|ripe|raw|cooked|cold|hot|warm|softened|melted|beaten|peeled|cubed)\b'
        self.number_pattern = r'(\d+(?:/\d+)?|\d*\.\d+|\d+)'

    def clean_text(self, text):
        # clean text, keep meaningful punctuation
        # keep comma for preparation method separation
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def parse_amount(self, amount_str, unit_text):
        # optimized amount parsing
        amount = amount_str.strip() if amount_str else ""
        
        # handle special fraction characters
        amount = amount.replace('\u00bd', '1/2')\
                      .replace('\u00bc', '1/4')\
                      .replace('\u00be', '3/4')
        
        # handle "fluid ounces" -> "oz"
        if 'fluid' in unit_text.lower() and 'ounce' in unit_text.lower():
            return f"{amount} oz"
        
        # handle "1 (1 inch) piece" -> "1 piece"
        piece_match = re.search(r'(\d+)\s*\(.*?\)\s*piece', amount + " " + unit_text)
        if piece_match:
            return f"{piece_match.group(1)} piece"
        
        # handle normal ounces
        if 'ounce' in unit_text.lower() or 'oz' in unit_text.lower():
            return f"{amount} oz"
        
        # simplify can unit
        can_match = re.search(r'(\d+)\s*\([\d.]+\s*ounce\)\s*cans?', amount + " " + unit_text)
        if can_match:
            num = int(can_match.group(1))
            return f"{num} {'cans' if num > 1 else 'can'}"
        
        # handle other units
        unit_match = re.search(self.unit_pattern, unit_text)
        if unit_match:
            unit = unit_match.group(1)
            if amount == "1":
                unit = unit.rstrip('s')
            return f"{amount} {unit}"
        
        # handle package unit
        package_match = re.search(r'(\d+)\s*\((\d+)\s*ounce\)\s*package', amount + " " + unit_text)
        if package_match:
            return f"{package_match.group(2)} oz"
        
        return amount.strip()

    def extract_preparation(self, text, descriptors):
        # optimized preparation method extraction
        prep_parts = []
        
        # extract preparation methods from descriptors
        prep_descriptors = [d for d in descriptors if d in [
            "fresh", "dried", "chopped", "minced", "sliced", "diced", "grated", "shredded",
            "crushed", "ground", "whole", "frozen", "large", "medium", "small", "ripe",
            "raw", "cooked", "cold", "hot", "warm", "softened", "melted", "beaten", 
            "peeled", "cubed"
            ]]
        if prep_descriptors:
            prep_parts.extend(prep_descriptors)
        
        # extract other preparation methods
        if ',' in text:
            prep_text = text.split(',', 1)[1].strip()
            if prep_text and prep_text not in prep_parts:
                prep_parts.append(prep_text)
        
        return ", ".join(prep_parts)

    def clean_ingredient_name(self, text, unit_match, descriptors):
        # clean and format ingredient name
        name = text
        
        # remove unit
        if unit_match:
            name = re.sub(self.unit_pattern, '', name)
        
        # remove descriptors
        for desc in descriptors:
            name = name.replace(desc, '')
        
        # remove content in parentheses and after comma
        name = re.sub(r'\([^)]*\)', '', name)
        if ',' in name:
            name = name.split(',')[0]
        
        # handle special cases
        if "reduced-fat" in name:
            name = "cream of chicken soup"
            descriptors.append("reduced-fat")
        
        # clean and return
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    def parse_single_ingredient(self, ing):
        # parse single ingredient, ensure output format is correct

        try:
            ingredient_dict = {
                "ingredient": "",
                "amount": "",
                "preparation": ""
            }
            
            # get basic information
            amount = ing.amount if hasattr(ing, 'amount') else ""
            ingredient_text = ing.ingredient.lower() if hasattr(ing, 'ingredient') else ""
            
            # extract descriptors
            descriptors = re.findall(self.descriptor_pattern, ingredient_text)
            
            # handle amount
            ingredient_dict["amount"] = self.parse_amount(amount, ingredient_text)
            
            # handle preparation method
            prep_method = ing.preparation if hasattr(ing, 'preparation') else ""
            ingredient_dict["preparation"] = self.extract_preparation(
                ingredient_text + (f", {prep_method}" if prep_method else ""),
                descriptors
            )
            
            
            # handle ingredient name
            unit_match = re.search(self.unit_pattern, ingredient_text)
            ingredient_dict["ingredient"] = self.clean_ingredient_name(
                ingredient_text,
                unit_match,
                descriptors
            )     
            return ingredient_dict
            
        except Exception as e:
            print(f"Error parsing single ingredient: {e}")
            return None

    def parse_ingredients(self, url: str) -> str:
        # parse all ingredients in recipe URL
        try:
            soup = get_recipe_page(url)
            raw_ingredients = ingredient_parser(soup)
            
            parsed_ingredients = []
            for ing in raw_ingredients:
                parsed = self.parse_single_ingredient(ing)
                if parsed and parsed["ingredient"]:  # only add valid ingredients
                    parsed_ingredients.append(parsed)
            
            return parsed_ingredients
            
        except Exception as e:
            print(f"Debug - Exception details: {str(e)}")
            return f"Error parsing ingredients: {e}"

def get_ingredients(url: str) -> str:
    # main function, keep compatible with original interface
    parser = IngredientParser()
    return parser.parse_ingredients(url)

# test code
if __name__ == "__main__":
    test_urls = ['https://www.allrecipes.com/recipe/18045/yellow-squash-casserole/']
    
    # [
    #    'https://www.allrecipes.com/recipe/230966/country-sunday-breakfast-casserole/',  # casserole 1
    #     'https://www.allrecipes.com/recipe/18045/yellow-squash-casserole/',   # casserole 2
    #     'https://www.allrecipes.com/recipe/231154/creamy-chicken-cordon-bleu-casserole/' # casserole 3
    # ]
    
    parser = IngredientParser()
    for url in test_urls:
        try:
            print(f"\nRecipe: {url.split('/')[-2].replace('-', ' ').title()}")
            result = parser.parse_ingredients(url)
            print(result)
            print("\n" + "-"*50)
        except Exception as e:
            print(f"Error parsing recipe: {e}")
