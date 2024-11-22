import json
from ..parse.Test import scrape_and_save
from ..parse.Steps import parse_and_save

def parse_recipe(url):
    scrape_and_save(url)
    parse_and_save()

def load_recipe_steps(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_step(steps, step_number):

    return next((step for step in steps if step["step_number"] == step_number), None)


