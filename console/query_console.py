from External_search import external_search
import spacy
import difflib


nlp = spacy.load("en_core_web_sm")

def answer_question(step, question, conversation_context, ingredients_list):
    doc = nlp(question.lower())
    methods = step.get("methods", {})
    tools = step.get("tools", [])
    step_ingredients = step.get("ingredients", {})
    response = None

    tokens = {token.text for token in doc}
    specific_tool = None
    specific_technique = None

    # Navigation intents
    if "next" in tokens or "continue" in tokens:
        return "next"
    elif "back" in tokens or "previous" in tokens:
        return "back"
    elif "repeat" in tokens:
        return "repeat"
    elif "step" in tokens:
        for token in doc:
            if token.like_num:
                step_number = int(token.text)
                return f"go to step {step_number}"

    # What do I chop (or other methods)
    if "what" in tokens and any(method in tokens for method in methods.keys()):
        for method, details in methods.items():
            if method in tokens:
                subjects = details.get("subject", [])
                if subjects:
                    subjects_str = ", ".join(subjects)
                    print (
                        f"{method.capitalize()} the {subjects_str}. "
                        "Would you like more guidance on that?\n"
                        "1) Yes - look up with external search\n"
                        "2) No - go back to the step"
                    )
                    ans =  input("> ").strip()
                    if "1" in ans:
                        return external_search(f"How to {method.capitalize()}{subjects_str}?")
                    else:
                        return "Going back to step..."

        return "I couldn't determine what you're asking about."

    # What tools do I need for this step
    if "tool" in tokens or "tools" in tokens:
        if tools:
            tool_list = ", ".join(tool.get("name", "unknown tool") for tool in tools)
            return f"You will need: {tool_list}."
        return "No tools are explicitly mentioned for this step."

    # What ingredients do I need
    if "ingredient" in tokens or "ingredients" in tokens:
        if step_ingredients:
            ingredient_list = ", ".join(step_ingredients.keys())
            print( f"For this step, you will need the {ingredient_list}. ")
        
        else:
            print("No ingredients are explicitly mentioned for this step.")
        
        print("Would you like to refer to the full ingredients list?")
        print("1) Yes - display ingredients list")
        print("2) No - go back to the step")
        ans =  input("> ").strip()
        if "1" in ans:
            return "DISP_ING_YES"
        else:
            return "DISP_ING_NO"

    # Goal (3): Ask about parameters of the current step
    if ("how" in tokens and "much" in tokens) or ("how" in tokens and "many" in tokens) or "amount" in tokens:
        step_ingredient_phrases = [chunk.text for chunk in doc.noun_chunks]
        for phrase in step_ingredient_phrases:
            matched_ingredient = find_matching_ingredient(phrase, ingredients_list)
            if matched_ingredient:
                # Fetch the ingredient from the ingredients_list
                for item in ingredients_list:
                    if item['ingredient'].lower() == matched_ingredient:
                        amount = item.get('amount', 'unknown amount')
                        return f"You will need {amount} of {item['ingredient']}."
        return "I couldn't find the specific ingredient mentioned in this step or the recipe."
    elif "how" in tokens and "long" in tokens:
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

    elif "when" in tokens or "done" in tokens or "until" in tokens:
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
    if "what" in tokens and "is" in tokens:
        for token in doc:
            if token.text in [tool.get("name") for tool in tools]:
                specific_tool = token.text
                break
        if specific_tool:
            return external_search(f"What is {specific_tool}?")
        return external_search(question)

    # Goal (5): Specific "how to" questions
    if "how" in tokens:
        for token in doc:
            for method in methods.keys():
                if method in token.text:
                    specific_technique = method
                    break
        if specific_technique:
            return f"I've found a reference for you {external_search(question)}"

    # Goal (6): Vague "how to" questions
    if "how" in tokens and "do" in tokens and "that" in tokens:
        last_action = conversation_context.get("last_method")
        subject = methods[last_action]["subject"][0]
        if last_action:
            return external_search(f"How do I {last_action} {subject}?")
        return "Could you clarify what 'that' refers to?"

    # Fallback response
    return "Sorry, I don't have enough information to answer that question."


def find_matching_ingredient(step_ingredient, ingredients_list):
    ingredient_names = [item['ingredient'].lower() for item in ingredients_list]
    matches = difflib.get_close_matches(step_ingredient.lower(), ingredient_names, n=1, cutoff=0.3)
    return matches[0] if matches else None