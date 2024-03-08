from googletrans import Translator
translator = Translator()
translated = translator.translate("Quelle temps fera t'il à tours hier",dest='en')
print(translated.text)
a=translated.text
import spacy
nlp = spacy.load("en_core_web_md")
doc = nlp(a)
print(doc.ents)
for ent in doc.ents:
    print(ent.text, ent.label_)
print(doc)
