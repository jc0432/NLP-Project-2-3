import requests 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 
from gadgets import get_gadgets
import json

def get_recipe_page(url: str) -> BeautifulSoup:
    """ Fetch and parse recipe page"""
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')


class Ingredients: 
    def __init__(self, ingredient, amount, preparation):
        self.ingredient = ingredient
        self.amount = amount
        self.preparation = preparation
    
    def __repr__(self):
        return f"(ingredient='{self.ingredient}', amount='{self.amount}', preparation='{self.preparation}')"
    

class Step:
    def __init__(self, step, direction):
        self.step = step 
        self.direction = direction

    def __repr__(self):
        return f"(step={self.step}, direction='{self.direction}')"
    
def get_title(soup: BeautifulSoup) -> str:
    """Fetch the title of the recipe."""
    title_tag = soup.find('h1', class_='article-heading text-headline-400')
    return title_tag.text.strip() if title_tag else "No title found"


def get_recipe_page(url: str) -> BeautifulSoup:
    """ Fetch and parse recipe page"""
    try:
        request = requests.get(url)
        request.raise_for_status()
        return BeautifulSoup(request.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching the recipe page: {e}")
        return None


def other_information(soup: BeautifulSoup):
    details_section = soup.find('div', class_='comp mm-recipes-details')
    
    recipe_info = {} 
    if details_section:
        items = details_section.find_all('div', class_='mm-recipes-details__item')

        for item in items:
            label = item.find('div', class_= 'mm-recipes-details__label')
            value = item.find('div', class_='mm-recipes-details__value')
            if label and value:
                recipe_info[label.text.strip()] = value.text.strip()
    else:
        print("No additional recipe information found.")
    
    return recipe_info 


def direction_parser(soup: BeautifulSoup):
    direction_list = []
    steps_container = soup.find('div', class_="comp mm-recipes-steps__content mntl-sc-page mntl-block")
    if not steps_container:
        print("No steps found.")
        return direction_list

    directions = steps_container.find_all(['li','p'], class_='comp mntl-sc-block mntl-sc-block-html')
    counter = 0 
    for direction_description in directions:
        counter +=1 
        direction_text = direction_description.get_text(strip=True)
        direction_list.append(Step(step=counter, direction=direction_text))
    return direction_list


def ingredient_parser(soup: BeautifulSoup):
    ingredients = []

    key_tags = soup.find_all('li', class_='mm-recipes-structured-ingredients__list-item')
    if not key_tags:
        print("No ingredients found.")
        return ingredients

    for tag in key_tags:
        prep_method = ''
        ingredient_span = tag.find('span', attrs={'data-ingredient-name': 'true'})
        quantiy_span = tag.find('span', attrs={'data-ingredient-quantity': 'true'})
        unit_span = tag.find('span', attrs={'data-ingredient-unit': 'true'})
        
        if ingredient_span:
            ingredient_name = ingredient_span.text.strip()
        else:
            ingredient_name = ""

        if quantiy_span and unit_span:
            amount = quantiy_span.text.strip() + " " + unit_span.text.strip()
        elif quantiy_span:
            amount = quantiy_span.text.strip()
        else:
            amount = ""

        # Split the ingredient name and preparation if comma exists
        match = re.split(r',\s*', ingredient_name)
        if len(match) > 1: 
            prep_method = match[1].strip()
            ingredient_name = match[0].strip()
        
        ingredients.append(Ingredient(ingredient=ingredient_name, amount=amount, preparation=prep_method))
    
    return ingredients


def main():
    url = 'https://www.allrecipes.com/recipe/21261/yummy-sweet-potato-casserole/'

    site_html = get_recipe_page(url)
    if not site_html:
        return
    title = get_title(site_html)

    ingredients = ingredient_parser(site_html)
    steps = direction_parser(site_html)
    recipe_details = other_information(site_html)
    gadgets = get_gadgets([step.direction for step in steps])

    # Prepare data for JSON serialization
    recipe_data = {
        "title": title,
        "ingredients": [vars(ing) for ing in ingredients],
        "steps": [vars(step) for step in steps],
        "details": recipe_details
    }

    # Save to JSON file
    with open('recipe.json', 'w') as f:
        json.dump(recipe_data, f, indent=4)
    print("\nScraped data has been saved to 'recipe.json'.")

if __name__ == "__main__":
    main()
