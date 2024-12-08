# NLP-Project-2
Parsing recipes to support conversational interaction

# Set up
1. Be sure to be in a python environment where the python version is < 3.13. Spacy doesn't work for python 3.13 for now. Best bet is to either be in a virtual env with a downgraded version of python or use a conda environment.
2. Run ```pip install -r requirements.txt```
3. Download the spacy model with ```python -m spacy download en_core_web_trf``` and ```python -m spacy download en_core_web_sm```
4. To start the program in the terminal, run ```python3 main_console.py```. To start the slack bot, run ```python3 app.py```

# Question Answering Goals

### Retrieval:
Enter an allrecipes recipe to begin.

Ex: https://www.allrecipes.com/the-best-million-dollar-spaghetti-recipe-8747691

### Next step:
Say "next" to go to the next step

### Navigation:
Ask "go back" to go back to the previous step

Ask "go to step n" to go to the nth step

Ask "repeat this step" to repeat the step

### Parameters:
Ask "how do I know when it's done" to get the definition of done in the current step

Ask "how much \<ingredient\> do I need" to the the amount of the current ingredient in the step

Ask "what ingredients do I need" to get the ingredients needed for the current step

Ask "what tools do I need" to get the tools needed for the current step

Ask "what do I \<action\> to get the subject of that action

Ask "how long do I \<action\> to get the duration of that action

### What is:
Ask a "what is ___" question to prompt an external google search

### How to:
Ask a "how do I ___" question to prompt an external search to a youtube video

Ask "how do I do that" to prompt an external search for the most recent cooking action from the conversation context

## Project 3: Transformations
Transforming Recipes

## Set up:
To preload a recipe into recipe.json for transformations, run ```python3 main_console.py``` and enter the URL you want to test. When the recipe is parsed, you can exit the program.

### Healthy
Run ```python3 healthy.py``` to test a healthy transformation, and look in healthier_parsed_steps.json for the output.

### South Asian
Run ```python3 south_asian_transform.py``` to transform into south asian cuisine, and look in recipe.json for the output.

### Quantity
Look in the ingredient.py file, and specify the test_url (line 246) you want to test.
If you want to change the scale factor, change the scale_factor parameter on line 261.

Run ```python3 ingredient.py``` and check the console output for the transformation.

### Vegetarian
Run ```python3 vegetarian_transformation.py``` to turn the recipe vegetarian, and look in recipe.json for the output.

### Change Cooking Method
Run ```python3 change_cooking_method_transformation.py``` to test changing the cooking method, and look in recipe.json for the output.

### Gluten Free
Run ```python3 gluten.py``` to change a recipe to gluten free, and look in recipe.json for the output.

### Lactose Free
Run ```python3 lactose.py``` to change a recipe to lactose free, and look in recipe.json for the output.
