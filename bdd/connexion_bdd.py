from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import urllib
from dotenv import load_dotenv

# Chargement des informations depuis le fichier .env
load_dotenv()
server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Urllib permet de prendre en compte le pilote ODBC dans l'url donné
params = urllib.parse.quote_plus(
    r'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)

# Connexion au serveur Azure
connexion = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(connexion, echo=True)

# Création de la session utilisateur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_azure)

# Création d'une classe de base dont héritera chaque modèle
Base = declarative_base()
