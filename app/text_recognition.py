#%% prep
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import requests
import re
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from transformers import pipeline
import time

load_dotenv()

def prep_bert():
    nlp = pipeline("ner", model = "bert/pipeline")
    return nlp

def recognize_from_microphone():
    # This example
    #  requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ['SPEECH_KEY'], region=os.environ['SPEECH_REGION'])
    speech_config.speech_recognition_language = "fr-FR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    try:
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
            return speech_recognition_result.text, 200
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
            return "No speech could be recognized", 404
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
                # Récupérer le code d'état HTTP à partir des détails de l'erreur
                status_code = cancellation_details.error_details.get("statusCode")
                if status_code:
                    return "Speech Recognition canceled", status_code
    except Exception as ex:
        # En cas d'erreur, capturer l'exception et extraire le code d'état HTTP
        if hasattr(ex, "response"):
            status_code = ex.response.status_code
            return str(ex), status_code
        else:
            print("Error:", ex)
            return str(ex), 500

def create_entity(a,nlp):
    doc = nlp(a)
    loc=[i['word'] for i in doc if i['entity'] in ['I-LOC']]
    dat=[i['word'] for i in doc if i['entity'] in ['I-DATE']]  
    return({'loc': loc,
            'dat' : dat})

def colle_mot(a):
    b=[]
    for i in a:
        if len(i)==1 and i[0]=='h':
            i=':'
        if i[0]!='▁' and len(b)!=0:
            b[-1]+=i
        else:
            b.append(i)
    return b

def virgule(a):
    b=""
    a = a.lower().replace('\xa0', '')
    for carac in a:
        if carac==',' or carac== ';' or carac== '.' or carac== '?' or carac== '!':
            b+=' , '
        else:
            b+=carac
    return b

def underscore(a):
    a=' '.join(a)
    b=''
    for carac in a:
        if carac=='▁':
            b+=''
        else:
            b+=carac
    b=b.lower()
    b=b.split(' ')
    return b

def localisation_func(a,b):
    a=a.lower()
    a=virgule(a)
    a=a.split(' ')
    b=underscore(b)
    c=[]
    for i in range(len(a)):
        if a[i] in b:
            if i!=0 and a[i-1] in b:
                c[-1]=c[-1]+' '+a[i]
            else:
                c.append(a[i])
    return c

def date(a):
    jours=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    date = r'(aujourd\'hui|demain|main|après main|après demain|aprèsmain|après-demain|(\d+) h|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|(\d+) jour)'
    time = r'(matin|après-midi|soir|nuit|\d+:\d+)(?:\s*(?:à|jusqu\'à)\s*(\d+:\d+))?'
    b=re.search(date, a)
    c=re.search(time,a)
    time1=datetime.now().date()
    hour_delta=6
    hour=True
    if b:
        if b.group(1)=="aujourd'hui":
            time1=time1
        elif b.group(1)=="demain":
            time1=time1+timedelta(days=1)
        elif b.group(1)=="lundi":
            jour='monday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="mardi":
            jour='tuesday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="mercredi":
            jour='wednesday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="jeudi":
            jour='thursday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="vendredi":
            jour='friday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="samedi":
            jour='saturday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="dimanche":
            jour='sunday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=='après-demain' or b.group(1)=='aprèsmain' or b.group(1)=='après main' or b.group(1)=='main' or b.group(1)=='après demain':
            time1=time1+timedelta(days=2)
        elif b.group(2) and 'h' not in a:
            time1=time1+timedelta(days=int(b.group(2)))
        elif b.group(1) and 'h' in a:
            time2=(datetime.now())+timedelta(hours=int(b.group(2)))
            if time2.minute > 30:
                time2 += timedelta(hours=1)
            time2 = time2.replace(minute=0, second=0, microsecond=0)
            time1 = time2.date()
            base_time = time2.strftime("%H:%M:%S")
            interval=False
            hour=False
    else:
        time1=time1
    if c:
        if c.group(1)=='matin':
            base_time='06:00:00'
            interval=False
        elif c.group(1)=='après-midi':
            base_time='13:00:00'
            interval=False
        elif c.group(1)=='soir':
            base_time='18:00:00'
            interval=False
        elif c.group(1)=='nuit':
            base_time='24:00:00'
            interval=False
        elif c.group(1)=='midi':
            base_time='10:00:00'
            interval=False
        else :
            base_time=c.group(1)+':00'
            interval=False
            if c.group(2):
                 base_time2=c.group(2)+':00'
                 interval=True
    elif hour==True:
        base_time='08:00:00'
        interval=False
        hour_delta=15
    time_final = datetime.combine(time1, datetime.strptime(base_time, '%H:%M:%S').time())
    if interval==False:
        time_final2=time_final+timedelta(hours=hour_delta)
    else:
        time_final2=datetime.combine(time1, datetime.strptime(base_time2, '%H:%M:%S').time())
    d=[]
    while time_final2>time_final:
        d.append(time_final.strftime('%Y-%m-%d %H:%M:%S'))
        time_final=time_final+timedelta(hours=1)
    return d

def city_to_coordinates(city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return {'lat': lat, 'lon': lon}, response.status_code
        else:
            return None, response.status_code 
    else:
        return None, response.status_code 

def get_weather_forecast(lat, lon, api_key=os.environ['meteo_key']):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data, response.status_code
    else:
        return None, response.status_code
    
def trie_json(json_meteo,date):
    liste_meteo_final=[]
    for i in json_meteo['list']:
        if i['dt_txt'] in date:
            liste_meteo_final.append(i)
    dico_meteo={}
    element_garder=['main','weather','clouds','wind','rain']
    for i in liste_meteo_final:
        date_key=i['dt_txt']
        del i['dt_txt']
        filtered_dict = {key: value for key, value in i.items() if key in element_garder}
        if date_key in dico_meteo :
            dico_meteo[date_key].append(filtered_dict)
        else:
            dico_meteo[date_key]=filtered_dict
    return dico_meteo
