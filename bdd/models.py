from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from connexion_bdd import Base

class MonitoredData(Base):
    __tablename__ = "monitored_data"

    idSavedData = Column(Integer, primary_key=True, index=True)
    timeStampSavedData = Column(DateTime(timezone=True), server_default=func.now()) # Pour la création d'un timestamp généré automatiquement par le serveur
    azureSTT = Column(String(250))
    statusCodeAzureSTT = Column(Integer)
    extractedEntity = Column(String(100))
    statusCodeNER = Column(Integer)
    position = Column(String(50))
    statusCodePosition = Column(Integer)
    meteo = Column(JSON)
    statusCodeMeteo = Column(Integer)
    finalResponse = Column(String(50))