import json
import os
from parse.Test import scrape_and_save
from parse.Steps import parse_and_save
from parse.ingredient import get_ingredients
from .query_console import answer_question

def parse_recipe(url):
    scrape_and_save(url)
    parse_and_save()

def load_recipe_steps(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_step(steps, step_number):
    return next((step for step in steps if step["step_number"] == step_number), None)

def display_ingredients(ingredients, recipe_title):
    print(f"\nHere are the ingredients for \"{recipe_title}\":")
    for item in ingredients:
        ingredient = item.get('ingredient', 'Unknown ingredient')
        amount = item.get('amount', '')
        preparation = item.get('preparation', '')

        details = f"- {amount} {ingredient}" if amount else f"- {ingredient}"
        if preparation:
            details += f" ({preparation})"
        print(details)

def recipe_bot_interface():
    print("Welcome to the Recipe Bot!")
    print("Please provide a URL to the recipe:")
    url = input("> ").strip()

    # Parse the recipe
    try:
        parse_recipe(url)
        recipe_file = "../resFiles/recipe.json"
        steps_file = "../resFiles/parsed_steps.json"

        if not os.path.exists(recipe_file) or not os.path.exists(steps_file):
            raise FileNotFoundError("Parsed recipe files not found.")

        with open(recipe_file, 'r') as file:
            recipe_data = json.load(file)

        recipe_title = recipe_data.get("title", "Unknown Recipe")
        ingredients_list = get_ingredients(url)
        steps = load_recipe_steps(steps_file)

        print(f"\nAlright. So let's start working with \"{recipe_title}\".")
        while True:
            print("What do you want to do?")
            print("[1] Go over ingredients list")
            print("[2] Go over recipe steps")
            choice = input("> ").strip()

            if choice == "1":
                if ingredients_list:
                    display_ingredients(ingredients_list, recipe_title)
                else:
                    print("No ingredients were found in the recipe.")

                print("\nWould you like to continue to the steps? (yes or no)")
                if input("> ").strip().lower() not in ["yes", "y"]:
                    print("Goodbye!")
                    break
                choice = "2"

            if choice == "2":
                step_number = 1
                conversation_context = {"last_method": None}

                while True:
                    current_step = get_step(steps, step_number)

                    if not current_step:
                        print("No more steps in the recipe. Enjoy your meal!")
                        return

                    print(f"\nStep {current_step['step_number']}: {current_step['direction']}")
                    print("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
                    user_input = input("> ").strip()

                    if "exit" in user_input.lower():
                        print("Goodbye!")
                        return

                    methods_in_step = current_step.get("methods", {})
                    if methods_in_step:
                        # Assuming the last method in the list is the most recent
                        last_method = list(methods_in_step.keys())[-1]
                        conversation_context["last_method"] = last_method
                    response = answer_question(current_step, user_input, conversation_context, ingredients_list)

                    if isinstance(response, str):
                        if response == "next":
                            step_number = min(step_number + 1, len(steps))
                        elif response == "back":
                            step_number = max(step_number - 1, 1)
                        elif response.startswith("go to step"):
                            try:
                                step_number = int(response.split()[-1])
                                if not get_step(steps, step_number):
                                    print("Invalid step number.")
                                    step_number = current_step["step_number"]
                            except ValueError:
                                print("Invalid step number.")
                        elif response == "repeat":
                            print(f"\nRepeating step {current_step['step_number']}: {current_step['direction']}")
                        elif response == "DISP_ING_YES":
                            display_ingredients(ingredients_list, recipe_title)
                        elif response == "DISP_ING_NO":
                            print("Returning to the step...")
                        else:
                            print(response)
                    elif isinstance(response, list) and response[0] == -1:
                        print(response[1])
                        display_ingredients(ingredients_list, recipe_title)
                    else:
                        print(response[0])
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    recipe_bot_interface()
