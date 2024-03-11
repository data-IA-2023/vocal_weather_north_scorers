
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import requests

load_dotenv()
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

a=recognize_from_microphone()
from transformers import pipeline

nlp = pipeline("ner", model = "bert/pipeline")

doc = nlp(a)
for i in doc:
    print(i['word'], i['entity'])
loc=[i['word'] for i in doc if i['entity'] in ['I-LOC']]
date=[i['word'] for i in doc if i['entity'] in ['I-DATE']]  
print(loc)
print(date)

def colle_mot(a):
    b=[]
    for i in a:
        if len(i)==1 and i[0]=='h':
            i=':'
        if i[0]!='_' and len(b)!=0:
            b[-1]+=i
        else:
            b.append(i)
    return b
loc=colle_mot(loc)
#date=colle_mot(date)

def virgule(a):
    b=""
    for carac in a:
        if carac==',' or carac== ';':
            b+=' , '
        else:
            b+=carac
    return b
def underscore(a):
    a=' '.join(a)
    b=''
    for carac in a:
        if carac=='_':
            b+=''
        else:
            b+=carac
    b=b.lower()
    b=b.split(' ')
    return b
def localisation(a,b):
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
loc=localisation(a,loc)
print(loc)







