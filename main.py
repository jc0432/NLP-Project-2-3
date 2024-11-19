import json
import spacy
import os
from Test import scrape_and_save
from Steps import parse_and_save
# from external_search import external_search

nlp = spacy.load("en_core_web_sm")

def parse_recipe(url):
    scrape_and_save(url)
    parse_and_save()

def load_recipe_steps(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_step(steps, step_number):
    return next((step for step in steps if step["step_number"] == step_number), None)


def answer_question(step, question, conversation_context, ingredients_list):
    # print("AQ QUESTION: ", question)
    doc = nlp(question.lower())
    methods = step.get("methods", {})
    tools = step.get("tools", [])
    step_ingredients = step.get("ingredients", {})
    response = None

    tokens = {token.text for token in doc}
    specific_tool = None
    specific_technique = None
    # print("@@@ A_Q, ", step.get("step_number", -1))
    # print("@@@ AQ TOKENS: ", tokens)

    if "next" in tokens or "continue" in tokens:
        # print("@@ NEXT")
        return "next"
    elif "back" in tokens or "previous" in tokens:
        # print("@@ BACK")
        return "back"
    elif "repeat" in tokens:
        # print("@@ REPEAT")
        return "repeat"
    elif "step" in tokens:
        for token in doc:
            if token.like_num:
                step_number = int(token.text)
                return f"go to step {step_number}"

    # Goal (3): Ask about parameters of the current step
    if "how" in tokens and "much" in tokens or "amount" in tokens:
        # print("@@ GOAL 3 _ 1")
        # Identify the ingredient
        for token in doc:
            for ingredient in step_ingredients:
                if ingredient in token.text:
                    # Check if the ingredient value is in the step
                    if step_ingredients[ingredient] is not None:
                        return f"You will need {step_ingredients[ingredient]} of {ingredient}."
                    else:
                        # Lookup in the original recipe
                        for item in ingredients_list:
                            if item.get("ingredient") == ingredient:
                                amount = item.get("amount", "unknown amount")
                                return f"You will need {amount} of {ingredient}."

        return "I couldn't find the specific ingredient mentioned in this step or the recipe."

    elif "how" in tokens and "long" in tokens:
        # Check if the user specifies a technique
        # print("@@ GOAL_3_2")
        for token in doc:
            for method in methods.keys():
                if method in token.text:
                    specific_technique = method
                    break

        if specific_technique:
            duration = methods[specific_technique].get("duration")
            if duration:
                return f"{specific_technique.capitalize()} for {duration}."
            else:
                return f"I'm sorry, I don't have the duration for {specific_technique}."
        return "I couldn't determine which technique you're referring to."

    elif "when" in tokens or "done" in tokens:
        # Return "duration" and "until" for the most relevant method
        # print("@@ GOAL 3 3")
        for method, details in methods.items():
            duration = details.get("duration")
            until = details.get("until")
            if duration or until:
                parts = []
                if until:
                    parts.append(f"until {until}")
                if duration:
                    parts.append(f"for {duration}")
                return f"{method.capitalize()} {' '.join(parts)}."

        return "I couldn't find any relevant information about when this step is done."

    # Goal (4): Simple "what is" questions
    # if "what" in tokens and "is" in tokens:
    #     for token in doc:
    #         if token.text in tools:
    #             specific_tool = token.text
    #             break

    #     if specific_tool:
    #         return external_search(f"What is {specific_tool}?")
    #     return "I couldn't determine which tool you're asking about."

    # Goal (5): Specific "how to" questions
    # if "how" in tokens:
    #     for token in doc:
    #         for method in methods.keys():
    #             if method in token.text:
    #                 specific_technique = method
    #                 break

    #     if specific_technique:
    #         return external_search(f"How do I {specific_technique}?")

    # # Goal (6): Vague "how to" questions
    # if "how" in tokens and "do" in tokens and "that" in tokens:
    #     last_action = conversation_context.get("last_action")
    #     if last_action:
    #         return external_search(f"How do I {last_action}?")
    #     return "Could you clarify what 'that' refers to?"

    # Fallback response
    return "Sorry, I don't have enough information to answer that question."


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
    ingredients_list = recipe_data.get("ingredients", [])
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
        conversation_context = {"last_action": None}  # Store conversation context

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
            # print("@@@ USER_INPUT: ", user_input)
            response = answer_question(current_step, user_input, conversation_context, ingredients_list)

            # Handle navigation responses
            if response == "next":
                if step_number < len(steps):
                    step_number += 1
                else:
                    print("You are already at the last step.")
            elif response == "back":
                if step_number > 1:
                    # print("@@HERE")
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
            else:
                # For all other responses (e.g., detailed question answers), just print them
                print(response)

            # Update the conversation context for vague "how to" questions
            conversation_context["last_action"] = user_input

# Example usage
if __name__ == "__main__":
    recipe_bot_interface()
