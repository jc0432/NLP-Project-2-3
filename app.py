# app.py

import os
import json
import re
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from main import (
    parse_recipe,
    load_recipe_steps,
    get_step,
)
from ingredient import get_ingredients
from query import answer_question
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
handler = SlackRequestHandler(app)

flask_app = Flask(__name__)

user_sessions = {}

def initialize_session(user_id):
    user_sessions[user_id] = {
        "recipe_url": None,
        "recipe_data": None,
        "ingredients_list": [],
        "steps": [],
        "current_step": 1,
        "conversation_context": {"last_method": None},
    }

def reset_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]

def get_session(user_id):
    if user_id not in user_sessions:
        initialize_session(user_id)
    return user_sessions[user_id]

def update_last_method(session, step):
    methods = step.get("methods", {})
    if methods:
        primary_method = next(iter(methods.keys()), None)
        session["conversation_context"]["last_method"] = primary_method
    else:
        session["conversation_context"]["last_method"] = None

def format_ingredients(ingredients, recipe_title):
    message = f"Here are the ingredients for \"{recipe_title}\":\n"
    for item in ingredients:
        ingredient = item.get('ingredient', 'Unknown ingredient')
        amount = item.get('amount', '')
        preparation = item.get('preparation', '')
        details = f"- {amount} {ingredient}" if amount else f"- {ingredient}"
        if preparation:
            details += f" ({preparation})"
        message += details + "\n"
    return message

def format_step(step):
    return f"*Step {step['step_number']}*: {step['direction']}"

# Event listener for app mentions
@app.event("message")
def handle_app_mentions(event, say):
    if event.get("subtype") == "bot_message" or "bot_id" in event:
        return
    user_id = event["user"]
    text = event["text"]
    print("text: ", text.strip())
    session = get_session(user_id)

    # Check if user is starting a new recipe
    if "walk me through a recipe" in text.lower():
        say("Sure. Please specify a URL.")
        return

    if session["recipe_url"] is None:
        # Assume the user is sending a URL
        url = text.strip()
        if url.startswith("<") and url.endswith(">"):
            url = url[1:-1]
        if not (url.startswith("http") or url.startswith("https")):
            say("Please provide a valid URL to a recipe.")
            return
        session["recipe_url"] = url
        say("Parsing the recipe, please wait...")

        try:
            parse_recipe(url)
            with open("recipe.json", 'r') as file:
                recipe_data = json.load(file)
            session["recipe_data"] = recipe_data
            session["ingredients_list"] = get_ingredients(url)
            session["steps"] = load_recipe_steps("parsed_steps.json")
            recipe_title = recipe_data.get("title", "Unknown Recipe")
            say(f"Alright. So let's start working with \"{recipe_title}\".")
            say("What do you want to do?\n1) Go over ingredients list\n2) Go over recipe steps")
        except Exception as e:
            say(f"Error parsing the recipe: {str(e)}")
            reset_session(user_id)
        return

    # Handle user choices
    if session["recipe_data"] and session["ingredients_list"] and session["steps"]:
        if "what do you want to do" in text.lower() or text in ["1", "2"]:
            choice = text.strip()
            if choice == "1":
                if session["ingredients_list"]:
                    ingredients_msg = format_ingredients(session["ingredients_list"], session["recipe_data"].get("title", "the recipe"))
                    say(ingredients_msg)
                else:
                    say("No ingredients were found in the recipe.")
                say("Would you like to continue to the steps? (yes or no)")
                return
            elif choice == "2":
                step = get_step(session["steps"], session["current_step"])
                update_last_method(session, step)
                if step:
                    print(session["ingredients_list"])
                    say(format_step(step))
                    say("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
                else:
                    say("No steps found in the recipe.")
                return

        if "yes" in text.lower():
            choice = "2"
            step = get_step(session["steps"], session["current_step"])
            if step:
                update_last_method(session, step)
                say(format_step(step))
                say("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
            else:
                say("No steps found in the recipe.")
            return
        elif "no" in text.lower() and "done" not in text.lower():
            say("Alright! Let me know if you need anything else.")
            reset_session(user_id)
            return

        # Handle step interactions
        step = get_step(session["steps"], session["current_step"])
        if step:
            response = answer_question(step, text, session["conversation_context"], session["ingredients_list"])

            if isinstance(response, str):
                if response == "next":
                    if session["current_step"] < len(session["steps"]):
                        session["current_step"] += 1
                        next_step = get_step(session["steps"], session["current_step"])
                        update_last_method(session, next_step)
                        say(format_step(next_step))
                        say("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
                    else:
                        say("You are already at the last step. Enjoy your meal!")
                elif response == "back":
                    if session["current_step"] > 1:
                        session["current_step"] -= 1
                        prev_step = get_step(session["steps"], session["current_step"])
                        update_last_method(session, prev_step)
                        say(format_step(prev_step))
                        say("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
                    else:
                        say("You are already at the first step.")
                elif response.startswith("go to step") or response.startswith("take me to step"):
                    try:
                        step_number = int(response.split()[-1])
                        if get_step(session["steps"], step_number):
                            session["current_step"] = step_number
                            say(f"Got it! Here is step {step_number}.")
                            current_step = get_step(session["steps"], step_number)
                            update_last_method(session, current_step)
                            say(format_step(current_step))
                            say("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
                        else:
                            say("Invalid step number.")
                    except ValueError:
                        say("Invalid step number.")
                elif response == "repeat":
                    say(format_step(step))
                    say("What would you like to do? (ask a question, go to the next step, go back a step, or exit)")
                elif response == "DISP_ING_YES":
                    ingredients_msg = format_ingredients(session["ingredients_list"], session["recipe_data"].get("title", "the recipe"))
                    say(ingredients_msg)
                elif response == "DISP_ING_NO":
                    say("Returning to the step...")
                else:
                    # For all other responses (e.g., detailed question answers), just send them as messages
                    say(response)
            elif isinstance(response, list) and response[0] == -1:
                say(response[1])
                ingredients_msg = format_ingredients(session["ingredients_list"], session["recipe_data"].get("title", "the recipe"))
                say(ingredients_msg)
            else:
                # If response is not a string, handle accordingly
                say(response[0])
        else:
            say("No more steps in the recipe. Enjoy your meal!")
            reset_session(user_id)

# Flask route to handle Slack requests
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)
