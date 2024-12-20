# conda activate nlp_project_env
import re
from Test import get_title, get_recipe_page
# spacy_model = spacy.load("en_core_web_sm")
from anthropic import Anthropic
import os

os.environ["ANTHROPIC_API_KEY"] = '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'

anthropic_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def clean_claude_response(response):
    response_str = str(response)
    
    if "TextBlock" in response_str:
        start_idx = response_str.find('text="') + 6
        end_idx = response_str.find('", type=')
        if start_idx != -1 and end_idx != -1:
            return response_str[start_idx:end_idx]
        

def get_ai_response(query): 
    """
    Get an AI-generated response using Claude API
    """
    try:
        # Construct the system message
        system_prompt = """You are an expert chef AI assistant, well-versed in all types of ingredients, tools, and cooking methodologies. 
        Your task is to provide quick and concise answers to cooking queries from people who are in the middle of preparing a dish. 
        Keep responses brief and practical, focusing on immediate cooking applications."""
        
        # Construct the user message
        recipe_title = get_title(get_recipe_page('https://www.allrecipes.com/recipe/19547/grandmas-corn-bread-dressing/'))
        user_message = f"""Question: {query}
        Recipe being prepared: {recipe_title}"""     

        # Create the message
        message = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0,
            system=system_prompt,
            messages=[
                {
                    "role": "user",    
                    "content": user_message
                }
            ]
        )
    
        return clean_claude_response(message.content) 
    

    except Exception as e:
        print(f"Error calling Claude API: {str(e)}")
        return "Sorry, I couldn't generate an AI response at the moment."

def action_formatting(string): 
    string = string.lower()
    query_string = ['https://www.youtube.com/results?search_query=']
    split_string =  string.split()
    query_string.append(split_string[0])
    split_string.pop(0)
    for word in split_string:
        query_string.append('+' + word)
    return "".join(query_string)

def item_formatting(string): 
    string = string.lower()
    query_string = ['https://www.google.com/search?q=']
    split_string =  string.split()
    query_string.append(split_string[0])
    split_string.pop(0)
    for word in split_string:
        query_string.append('+' + word)
    return get_ai_response(string), "".join(query_string)

def determine_type(string):
    match1_pattern = r'\bhow\b'
    match2_pattern = r'\bwhat\b'
    if re.search(match1_pattern, string, re.IGNORECASE): 
        query = action_formatting(string)
    elif re.search(match2_pattern, string, re.IGNORECASE): 
        query = item_formatting(string)
    else:
        query = "Neither pattern matched" 
    return query
    
def external_search(query):
    return determine_type(query)










    # loaded = spacy_model(string)
    # pos_dict = {}
    # for token in loaded:
    #     if token not in pos_dict.keys():
    #         pos_dict[token] = token.pos_
    # for item in list(pos_dict.values())[:3]:
    #     if item == 'SCONJ' or item == 'AUX': 
    #      query_formatting(string)
    #     else:
    #         query_formatting("how to " + string)
