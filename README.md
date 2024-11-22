# NLP-Project-2
Parsing recipes to support conversational interaction

# Set up
1. Be sure to be in a python environment where the python version is < 3.13. Spacy doesn't work for python 3.13 for now. Best bet is to either be in a virtual env with a downgraded version of python or use a conda environment.
2. Run ```pip install -r requirements.txt```
3. Download the spacy model with ```python -m spacy download en_core_web_trf```
4. To start the program, run ```python3 main_console.py```

# Question Answering Goals

### Retrieval:
Enter an allrecipes recipe to begin.

Ex: https://www.allrecipes.com/the-best-million-dollar-spaghetti-recipe-8747691

### Next step:
Say "next" to go to the next step

### Go to step:
Ask "go back" to go back to the previous step

Ask "go to step n" to go to the nth step

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

Ask "how do I do that" to prompt an external search of the first part of the step
