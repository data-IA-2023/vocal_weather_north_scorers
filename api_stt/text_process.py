from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")


#nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

#nlp.save_pretrained("api_stt\saved_pipe")

nlp = pipeline('ner', model= 'saved_pipe')

doc = nlp("Abliblablo Tours, c'est très bien Tours, surtout que demain abliblablo à 17h")
print(doc)