import requests 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 
from gadgets import get_gadgets

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
        return f"(ingredient={self.ingredient}, amount='{self.amount}', preparation={self.preparation})"
    

class Steps:
    def __init__(self, step, direction):
        self.step = step 
        self.direction = direction

    def __repr__(self):
        return f"(step='step {self.step}', direction={self.direction})"

    

def other_information(soup: BeautifulSoup):
    details_section = soup.find('div', class_='comp mm-recipes-details')
    
    recipe_info = {} 
    items = details_section.find_all('div', class_='mm-recipes-details__item')

    for item in items:
        label = item.find('div', class_= 'mm-recipes-details__label')
        value = item.find('div', class_='mm-recipes-details__value')
        recipe_info[label.text] = value.text

    return recipe_info 


def direction_parser(soup: BeautifulSoup):
    direction_list = []
    steps_container = soup.find('div', class_="comp mm-recipes-steps__content mntl-sc-page mntl-block")
    directions = steps_container.find_all(['li','p'], class_='comp mntl-sc-block mntl-sc-block-html')
    counter = 0 
    for direction_description in directions:
        counter +=1 
        direction_list.append(Steps(step = counter, direction=direction_description.text))
    return direction_list

    
def ingredient_parser(soup: BeautifulSoup):
    ingredients = []

    key_tag = soup.find_all('li', class_='mm-recipes-structured-ingredients__list-item')
    # print(key_tag)

    for tag in key_tag:
        prep_method = ''
        # tags_list = tag.find('p')
        ingredient_span = tag.find('span', attrs={'data-ingredient-name': 'true'}).text
        quantiy_span = tag.find('span', attrs={'data-ingredient-quantity': 'true'})
        unit_span = tag.find('span', attrs={'data-ingredient-unit': 'true'})
        unit_quantity = quantiy_span.text + " " + unit_span.text 

        """ Split the name_span apart - current format looks like pepper, to taste"""
        match = re.split(r',\s*', ingredient_span)
        if len(match) > 1: 
            prep_method = match[1].strip()
            ingredient_span = match[0].strip()
        ingredients.append(Ingredients(ingredient=ingredient_span, amount = unit_quantity, preparation= prep_method))
    
    return(ingredients)



def main():
    url = 'https://www.allrecipes.com/recipe/21261/yummy-sweet-potato-casserole/'

    site_html = get_recipe_page(url)

    ingredients = ingredient_parser(site_html)
    steps = direction_parser(site_html)
    recipe_details = other_information(site_html)
    gadgets = get_gadgets([step.direction for step in steps])


main()