from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bdd.connexion_bdd import SessionLocal
from sqlalchemy.orm import Session
from bdd.models import MonitoredData
from bdd.crud import create_monitored_data, get_monitored_data, get_monitored_data_by_id, update_monitored_data, delete_monitored_data

app = FastAPI()

# Récupération de la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuration de Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "titre": "Accueil"})

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