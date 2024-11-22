import json
import os
from Test import scrape_and_save
from Steps import parse_and_save
from ingredient import get_ingredients
from query import answer_question

def parse_recipe(url):
    scrape_and_save(url)
    parse_and_save()

def load_recipe_steps(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_step(steps, step_number):
    return next((step for step in steps if step["step_number"] == step_number), None)

# Display ingredients in a human-readable format
def display_ingredients(ingredients):
    print("\nHere are the ingredients:")
    for item in ingredients:
        ingredient = item.get('ingredient', 'Unknown ingredient')
        amount = item.get('amount', '')
        preparation = item.get('preparation', '')

        details = f"- {amount} {ingredient}" if amount else f"- {ingredient}"
        if preparation:
            details += f" ({preparation})"
        print(details)

# Main conversational loop
def recipe_bot_interface():
    print("Welcome to the Recipe Bot!")
    print("Please provide a URL to the recipe:")
    url = input("> ").strip()

    # Parse the recipe
    parse_recipe(url)

    # Load parsed data
    recipe_file = "recipe.json"
    steps_file = "parsed_steps.json"

    if not os.path.exists(recipe_file) or not os.path.exists(steps_file):
        print("Error: Parsed recipe files not found.")
        return

    with open(recipe_file, 'r') as file:
        recipe_data = json.load(file)

    recipe_title = recipe_data.get("title", "Unknown Recipe")

    ingredients_list = get_ingredients(url)

    steps = load_recipe_steps(steps_file)

    print(f"\nAlright. So let's start working with \"{recipe_title}\".")
    print("What do you want to do?")
    print("[1] Go over ingredients list")
    print("[2] Go over recipe steps")
    choice = input("> ").strip()

    if choice == "1":
        # Display ingredients list
        if ingredients_list:
            display_ingredients(ingredients_list)
        else:
            print("No ingredients were found in the recipe.")

        print("\nWould you like to continue to the steps? (yes or no)")
        continue_choice = input("> ").strip().lower()
        if continue_choice in ["yes", "y"]:
            choice = "2"
        else:
            print("Goodbye!")
            return

    if choice == "2":
        step_number = 1  # Start at the first step
        conversation_context = {"last_method": None}  # Store conversation context

        while True:
            current_step = get_step(steps, step_number)

            if not current_step:
                print("No more steps in the recipe. Enjoy your meal!")
                break

            print(f"\nStep {current_step['step_number']}: {current_step['direction']}")
            print("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
            user_input = input("> ").strip()

            if "exit" in user_input.lower():
                print("Goodbye!")
                break
            
            # Extract methods from the current step to update conversation context
            methods_in_step = current_step.get("methods", {})
            if methods_in_step:
                # Assuming the last method in the list is the most recent
                last_method = list(methods_in_step.keys())[-1]
                conversation_context["last_method"] = last_method
            response = answer_question(current_step, user_input, conversation_context, ingredients_list)

            # Handle navigation responses
            if isinstance(response, str):
                if response == "next":
                    if step_number < len(steps):
                        step_number += 1
                    else:
                        print("You are already at the last step.")
                elif response == "back":
                    if step_number > 1:
                        step_number -= 1
                    else:
                        print("You are already at the first step.")
                elif response.startswith("go to step"):
                    try:
                        step_number = int(response.split()[-1])
                        if get_step(steps, step_number):
                            print(f"\nGot it! Here is step {step_number}.")
                        else:
                            print("Invalid step number.")
                    except ValueError:
                        print("Invalid step number.")
                elif response == "repeat":
                    print(f"\nRepeating step {current_step['step_number']}: {current_step['direction']}")
                elif response == "DISP_ING_YES":
                    display_ingredients(ingredients_list)
                elif response == "DISP_ING_NO":
                    print("Returning to the step...")
                else:
                    # For all other responses (e.g., detailed question answers), just print them
                    print(response)
            else:
                print(response[0])

  

# Example usage
if __name__ == "__main__":
    recipe_bot_interface()
