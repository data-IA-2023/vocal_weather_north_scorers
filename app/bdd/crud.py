from sqlalchemy.orm import Session
from .models import MonitoredData
from .connexion_bdd import SessionLocal, engine_azure, Base

Base.metadata.create_all(bind=engine_azure)

def create_monitored_data(db: Session, monitored_data: MonitoredData):
    db_monitored_data = MonitoredData(**monitored_data.dict())
    db.add(db_monitored_data)
    db.commit()
    db.refresh(db_monitored_data)
    return db_monitored_data

def get_monitored_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MonitoredData).offset(skip).limit(limit).all()

def get_monitored_data_by_id(db: Session, id: int):
    return db.query(MonitoredData).filter(MonitoredData.idSavedData == id).first()

def update_monitored_data(db: Session, id: int, update_data: dict):
    db_monitored_data = db.query(MonitoredData).filter(MonitoredData.idSavedData == id).first()
    for key, value in update_data.items():
        setattr(db_monitored_data, key, value)
    db.commit()
    return db_monitored_data

def delete_monitored_data(db: Session, id: int):
    db_monitored_data = db.query(MonitoredData).filter(MonitoredData.idSavedData == id).first()
    db.delete(db_monitored_data)
    db.commit()
    return {"ok": True}