# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de la base SQLite (le fichier sera créé automatiquement s'il n'existe pas)
DATABASE_URL = "sqlite:///./edgedommo.db"

# Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour déclarer les modèles
Base = declarative_base()
