
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
print(doc)
for i in doc:
    print(i['word'], i['entity'])
loc=[i['word'] for i in doc if i['entity'] in ['I-LOC']]
date=[i['word'] for i in doc if i['entity'] in ['I-DATE']]  
print(loc)
print(date)