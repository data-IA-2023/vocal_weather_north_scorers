#%%
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import requests

"""load_dotenv()
def recognize_from_microphone():
    # This example
    #  requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ['SPEECH_KEY'], region=os.environ['SPEECH_REGION'])
    speech_config.speech_recognition_language="fr-FR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        a=speech_recognition_result.text
        print("Recognized: {}".format(speech_recognition_result.text))
        return a
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

a=recognize_from_microphone()"""
a="Tours, Beaumont, la Rance, Saint Cyr sur Loire, demain"
from googletrans import Translator
translator = Translator()
translated = translator.translate(a,dest='en')
print(translated.text)
b=translated.text
import spacy
nlp = spacy.load("en_core_web_md")
doc = nlp(b)
print(doc.ents)
for token in doc:
    print(token.text,token.head.text,token.dep_)
for ent in doc.ents:
    print(ent.text, ent.label_)
print(doc)
loc=[ent.text for ent in doc.ents if ent.label_ in ['LOC', 'GPE', 'FAC','ORG','PERSON']]
date=[ent.text for ent in doc.ents if ent.label_ in ['DATE','TIME']]  
print(loc,date)
loc1=' '.join(loc)
from geopy.geocoders import Nominatim
from sys import argv
def city_to_coordinates(city):

    geolocator = Nominatim(user_agent="vocal_weather_app")

    location = geolocator.geocode(city)
    
    lat = location.latitude
    lon = location.longitude

    print(f'Latitude, Longitude : {lat, lon}')
    return({'lat': lat,
            'lon' : lon})
a=city_to_coordinates(loc1)
print(a)

def get_weather_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error")
        return None
"""print(get_weather_forecast(a['lat'], a['lon'],""))"""