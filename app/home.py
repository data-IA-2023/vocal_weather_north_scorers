from fastapi import FastAPI
from api_stt.voice_recognizer import recognize_from_microphone
app = FastAPI()


@app.get("/")
def read_root():
    return {"Prochainement...": "Votre météo"}

@app.post("/")
def ask_weather():
    return recognize_from_microphone()