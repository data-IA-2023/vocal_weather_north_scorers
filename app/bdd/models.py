from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from bdd.connexion_bdd import Base

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

    # Pour sauvegarder dans la base de données
    def to_dict(self):
        return {
            "idSavedData": self.idSavedData,
            "timeStampSavedData": self.timeStampSavedData.isoformat() if self.timeStampSavedData else None,
            "azureSTT": self.azureSTT,
            "statusCodeAzureSTT": self.statusCodeAzureSTT,
            "extractedEntity": self.extractedEntity,
            "statusCodeNER": self.statusCodeNER,
            "position": self.position,
            "statusCodePosition": self.statusCodePosition,
            "meteo": self.meteo,
            "statusCodeMeteo": self.statusCodeMeteo,
            "finalResponse": self.finalResponse,
        }

