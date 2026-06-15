from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. L'URL de connexion à notre base de données Docker
# Format: postgresql://utilisateur:mot_de_passe@hôte:port/nom_de_base
DATABASE_URL = "postgresql://postgres:mon_mot_de_passe@localhost:5432/trello_portfolio"

# 2. Le moteur qui gère les connexions physiques à Postgres
engine = create_engine(DATABASE_URL)

# 3. La fabrique de sessions pour interagir avec la base (exécuter des requêtes)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. La classe de base dont hériteront tous nos modèles de tables
Base = declarative_base()

# 5. Fonction utilitaire pour obtenir une session de base de données à chaque requête API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()