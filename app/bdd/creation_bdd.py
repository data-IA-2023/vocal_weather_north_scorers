from connexion_bdd import engine_azure, Base
from models import MonitoredData

def create_database_tables():
    Base.metadata.create_all(bind=engine_azure)

if __name__ == "__main__":
    create_database_tables()
    print("La table a bien été créée.")