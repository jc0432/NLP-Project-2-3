import spacy
nlp = spacy.load("en_core_web_trf")


text = "Mash drained sweet potatoes with a fork. Add eggs; mix until well combined. Add sugar, milk, butter, vanilla, and salt; mix until smooth. Transfer to a 9x13-inch baking dish."
doc = nlp(text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)