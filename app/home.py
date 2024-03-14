from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from bdd.connexion_bdd import SessionLocal
from sqlalchemy.orm import Session
from bdd.models import MonitoredData
from datetime import datetime
import asyncio
from cachetools import cached, TTLCache
from transformers import pipeline
from bdd.crud import create_monitored_data, get_monitored_data, get_monitored_data_by_id, update_monitored_data, delete_monitored_data
from text_recognition import recognize_from_microphone, create_entity, colle_mot, underscore, city_to_coordinates, date, get_weather_forecast, trie_json, localisation_func 
app = FastAPI()

# Récupération de la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Récupération du BERT depuis le cache
cache = TTLCache(maxsize=1, ttl=600)

@cached(cache)
def prep_bert():
    nlp = pipeline("ner", model = "saved_pipe")
    return nlp

# Configuration de Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def load_index(request: Request):
    monitoring = {
        'status_azure': None,
        'texte': None,
        'date': None,
        'localisations': [],
        'coord': {},
        'status_code_geoloc': {},
        'status_code_weather': {},
        'dico_meteo': {},
    }
    return templates.TemplateResponse("index.html", context={'request': request, 'monitoring': monitoring})

@app.get("/vocal-recognizer")
async def func_final(request: Request, db: Session = Depends(get_db),):
    monitoring = {
        'status_azure': None,
        'texte': None,
        'date': None,
        'localisations': [],
        'coord': {},
        'status_code_geoloc': {},
        'status_code_weather': {},
        'dico_meteo': {},
    }
    nlp = prep_bert()

    # Variables contenant les éléments à afficher dans les templates
    # contenu = None
    error_message = None

    text_donne,status_azure=recognize_from_microphone()
    monitoring['status_azure']=status_azure
    monitoring['texte']=text_donne
    if status_azure != 200:
        error_message="Probleme avec le text_to_speech"
        return templates.TemplateResponse("erreurs/affichageErreur.html", context={'request': request, 'monitoring': monitoring, "error_message": error_message})
    
    entites=create_entity(text_donne,nlp)

    if len(entites['loc'])==0:
        error_message="Veuillez donner une localisation précise"
        return templates.TemplateResponse("erreurs/affichageErreur.html", context={'request': request, 'monitoring': monitoring, "error_message": error_message})
    
    loc=colle_mot(entites['loc'])
    loc=localisation_func(text_donne,loc)
    if len(entites['dat'])==0:
            heure_actuelle = datetime.now().replace(minute=0, second=0, microsecond=0)
            heure_actu = heure_actuelle.strftime("%Hh00")
            date_base=f"aujourd'hui à {heure_actu}"
            entites['dat'].append(date_base)
    dat=colle_mot(entites['dat'])
    dat=underscore(dat)
    dat=' '.join(dat)
    date_final=date(dat)

    monitoring['date']=date_final


    for localisation in loc:
        monitoring['localisations'].append(localisation)
        coord,status_code_geoloc=city_to_coordinates(localisation)
        monitoring['coord'][localisation]=coord
        monitoring['status_code_geoloc'][localisation]=status_code_geoloc
        if coord is None:
            pass
        else:
            json_meteo,status_code_weather=get_weather_forecast(coord['lat'], coord['lon'])
            monitoring['status_code_weather'][localisation]=status_code_weather
            if json_meteo is None:
                monitoring['dico_meteo'][localisation]=None
                pass
            else:
                dico_meteo=trie_json(json_meteo,date_final)
                monitoring['dico_meteo'][localisation]=dico_meteo
        await asyncio.sleep(0.5)
    return JSONResponse(content=monitoring)

# CRUD Monitoring
# Création d'une entrée dans la base de donnée
@app.post("/monitor/create")
async def create_monitored_data_route(monitored_data_dict: dict, db: Session = Depends(get_db)):
    monitored_data = MonitoredData(**monitored_data_dict)
    return create_monitored_data(db=db, monitored_data=monitored_data).to_dict()

# Lecture de toutes les entrées de la BDD
@app.get("/monitor")
def read_monitored_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    monitored_data = get_monitored_data(db, skip=skip, limit=limit)
    return [item.to_dict() for item in monitored_data]

# Lecture de l'entrée spécifiée
@app.get("/monitor/{id}")
def read_monitored_data_by_id(id: int, db: Session = Depends(get_db)):
    db_monitored_data = get_monitored_data_by_id(db, id=id)
    if db_monitored_data is None:
        raise HTTPException(status_code=404, detail="MonitoredData not found")
    return db_monitored_data.to_dict()

# Mise à jour de l'entrée spécifiée
@app.put("/monitor/update/{id}")
def update_monitored_data_route(id: int, monitored_data_dict: dict, db: Session = Depends(get_db)):
    db_monitored_data = update_monitored_data(db=db, id=id, update_data=monitored_data_dict)
    if db_monitored_data is None:
        raise HTTPException(status_code=404, detail="MonitoredData not found")
    return db_monitored_data.to_dict()

# Suppression de l'entrée spécifiée
@app.delete("/monitor/delete/{id}")
def delete_monitored_data(id: int, db: Session = Depends(get_db)):
    success = delete_monitored_data(db, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="MonitoredData not found")
    return {"ok": True}