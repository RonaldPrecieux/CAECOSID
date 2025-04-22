# 1. Imports standards
from datetime import datetime
# 2. Imports tiers

from fastapi import FastAPI, Depends, Request,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# 3. Imports locaux
from database import engine, SessionLocal
import models
import schemas

# Créer les tables si elles n'existent pas
models.Base.metadata.create_all(bind=engine)
# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    lieux = db.query(models.Lieux).all()
    microcontroleurs = db.query(models.Microcontroleur).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "lieux": lieux,
        "microcontroleurs": microcontroleurs,
        "title": "Dashboard Titan 5"
    })
# ------------------- ROUTES LIEUX -------------------

@app.get("/lieux/", response_model=list[schemas.Lieu])
def read_lieux(db: Session = Depends(get_db)):
    return db.query(models.Lieux).all()

@app.post("/lieux/", response_model=schemas.Lieu)
def create_lieu(lieu: schemas.LieuCreate, db: Session = Depends(get_db)):
    db_lieu = models.Lieux(nom=lieu.nom)
    db.add(db_lieu)
    db.commit()
    db.refresh(db_lieu)
    return db_lieu

# ------------------- ROUTES MICROCONTROLEURS -------------------

@app.get("/microcontroleurs/", response_model=list[schemas.Microcontroleur])
def read_microcontroleurs(db: Session = Depends(get_db)):
    return db.query(models.Microcontroleur).all()

@app.post("/microcontroleurs/", response_model=schemas.Microcontroleur)
def create_microcontroleur(micro: schemas.MicrocontroleurCreate, db: Session = Depends(get_db)):
    db_micro = models.Microcontroleur(
        uuid=micro.uuid,
        nom=micro.nom,
        lieu_id=micro.lieu_id
    )
    db.add(db_micro)
    db.commit()
    db.refresh(db_micro)
    return db_micro

@app.put("/microcontroleurs/{uuid}", response_model=schemas.Microcontroleur)
def update_microcontroleur(uuid: str, micro: schemas.MicrocontroleurCreate, db: Session = Depends(get_db)):
    db_micro = db.query(models.Microcontroleur).filter(models.Microcontroleur.uuid == uuid).first()
    if db_micro is None:
        raise HTTPException(status_code=404, detail="Microcontrôleur non trouvé")
    print('========================db""""""""""""',db_micro)
    db_micro.nom = micro.nom
    db_micro.lieu_id = micro.lieu_id
    db_micro.date_affectation = models.utc_now()  # remettre la date d'affectation à jour
    db.commit()
    db.refresh(db_micro)
    return db_micro

@app.delete("/microcontroleurs/{uuid}")
def delete_microcontroleur(uuid: str, db: Session = Depends(get_db)):
    db_micro = db.query(models.Microcontroleur).filter(models.Microcontroleur.uuid == uuid).first()
    if db_micro is None:
        raise HTTPException(status_code=404, detail="Microcontrôleur non trouvé")
    db.delete(db_micro)
    db.commit()
    return {"message": "Microcontrôleur supprimé"}