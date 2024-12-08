import json
import re
import spacy 
import warnings
warnings.filterwarnings("ignore")
nlp = spacy.load("en_core_web_trf")



# def baking_script(sentence, ingredient):

grill_match = r'\bgrill\b'
preparation_match = r'\bpreheat\b'  


with open('recipe.json', 'r') as file:
    recipe = json.load(file)
    

def sentence_replacer(full_instruction, original_sentence):
    if re.search(preparation_match, original_sentence, re.IGNORECASE):
        if len(full_instruction.split('.')) == 2:
            new_sentence = "Preheat pan with high heat and lightly spray with oil"
        else:
            new_sentence = "Preheat pan with high heat and lightly spray with cooking oil"
        full_instruction = full_instruction.replace(original_sentence, new_sentence)
        return {"Preheated": True, "new sentence": new_sentence, "instruction": full_instruction}
    
    else:
        original_doc = nlp(original_sentence)
        new_sentence = original_sentence  

        for token in original_doc:
            if token.pos_ == 'NOUN' and re.search(token.text, grill_match, re.IGNORECASE):
                new_sentence = new_sentence.replace(token.text, "pan")
            elif token.pos_ == 'VERB' and re.search(token.text, r'\bgrilling\b', re.IGNORECASE):
                new_sentence = new_sentence.replace(token.text, "searing")

        full_instruction = full_instruction.replace(original_sentence, new_sentence)
        return {"Preheated": False, "new sentence": new_sentence, "instruction": full_instruction}


def change_order(preheated_occurence):
    preheat_steps = [step for step in recipe["steps"] if step["step"] == preheated_occurence]
    remaining_steps = [step for step in recipe["steps"] if step["step"] != preheated_occurence]

    place_step_index = -1
    for i, step in enumerate(remaining_steps):
        direction_doc = nlp(step["direction"])
        if any(token.text.lower() == "place" and token.dep_ == "ROOT" for token in direction_doc):
            place_step_index = i
            break
    if place_step_index != -1:
        reordered_steps = remaining_steps[:place_step_index] + preheat_steps + remaining_steps[place_step_index:]
    else:
        reordered_steps = preheat_steps + remaining_steps

    for i, step in enumerate(reordered_steps):
        step["step"] = i + 1

    # Update the recipe steps
    recipe["steps"] = reordered_steps
    return recipe


def check_methods(): 
    preheated_occurence =  ''
    ingredient_list = recipe['steps']
    for step in ingredient_list:
        full_instruction = step['direction']
        modified_instruction = full_instruction  

        for sentence in full_instruction.split('.'):
            sentence = sentence.strip()
            if 'grill' in sentence.lower():
                result = sentence_replacer(full_instruction, sentence)
                if result['Preheated']:
                    preheated_occurence = step['step']
                modified_instruction = modified_instruction.replace(sentence, result["new sentence"])

        step['direction'] = modified_instruction
    return recipe, preheated_occurence



def save_recipe_to_file(final_recipe, filename="change cooking method.json"):

    with open(filename, "w") as json_file:
        json.dump(final_recipe, json_file, indent=4)
    print(f"Updated recipe saved to {filename}")



def main():
    recipe, preheat = check_methods()
    final_recipe = change_order(preheat)
    save_recipe_to_file(final_recipe)



main()
