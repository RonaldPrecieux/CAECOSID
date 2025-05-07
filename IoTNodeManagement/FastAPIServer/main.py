# 1. Imports standards
from datetime import datetime
# 2. Imports tiers

from fastapi import FastAPI, Depends, Request,HTTPException,APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# 3. Imports locaux
from IoTNodeManagement.FastAPIServer.database import engine, SessionLocal
import IoTNodeManagement.FastAPIServer.models as models
import IoTNodeManagement.FastAPIServer.schemas as schemas


mqtt_router = APIRouter(prefix="/mqtt", tags=["MQTT"])
app = FastAPI()
app.include_router(mqtt_router)



# Créer les tables si elles n'existent pas
models.Base.metadata.create_all(bind=engine)
# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

@app.get("/lieux/{lieu_id}", response_model=schemas.Lieu)
def read_lieu(lieu_id: int, db: Session = Depends(get_db)):
    db_lieu = db.query(models.Lieux).filter(models.Lieux.id == lieu_id).first()
    if db_lieu is None:
        raise HTTPException(status_code=404, detail="Lieu non trouvé")
    return db_lieu

@app.get("/lieux/nom/{nom}", response_model=schemas.Lieu)
def read_lieu(nom: str, db: Session = Depends(get_db)):
    db_lieu = db.query(models.Lieux).filter(models.Lieux.nom == nom).first()
    if db_lieu is None:
        raise HTTPException(status_code=404, detail="Lieu non trouvé")
    return db_lieu

@app.put("/lieux/{lieu_id}", response_model=schemas.Lieu)
def update_lieu(lieu_id: int, lieu: schemas.LieuCreate, db: Session = Depends(get_db)):
    db_lieu = db.query(models.Lieux).filter(models.Lieux.id == lieu_id).first()
    if db_lieu is None:
        raise HTTPException(status_code=404, detail="Lieu non trouvé")
    
    db_lieu.nom = lieu.nom
    db.commit()
    db.refresh(db_lieu)
    return db_lieu

@app.delete("/lieux/{lieu_id}", status_code=204)
def delete_lieu(lieu_id: int, db: Session = Depends(get_db)):
    db_lieu = db.query(models.Lieux).filter(models.Lieux.id == lieu_id).first()
    if db_lieu is None:
        raise HTTPException(status_code=404, detail="Lieu non trouvé")
    
    db.delete(db_lieu)
    db.commit()
    return


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

# ------------------- API POUR LES TOPICS MQTT -------------------

@app.get("/topics/")
def get_all_topics(db: Session = Depends(get_db)):
    """
    Retourne la liste de tous les topics MQTT (UUID des microcontrôleurs).
    """
    uuids = db.query(models.Microcontroleur.uuid).all()
    return [uuid for (uuid,) in uuids]

@app.get("/topics/lieux")
def get_topics_by_lieu(db: Session = Depends(get_db)):
    """
    Retourne un dictionnaire {lieu_nom: [uuid1, uuid2, ...]} pour l'écoute par lieu.
    """
    lieux = db.query(models.Lieux).all()
    microcontroleurs = db.query(models.Microcontroleur).all()

    mapping = {lieu.nom: [] for lieu in lieux}
    for micro in microcontroleurs:
        if micro.lieu_id:
            nom_lieu = next((lieu.nom for lieu in lieux if lieu.id == micro.lieu_id), None)
            if nom_lieu:
                mapping[nom_lieu].append(micro.uuid)

    return mapping
