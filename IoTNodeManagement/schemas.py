# schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------- LIEUX --------
class LieuBase(BaseModel):
    nom: str

class LieuCreate(LieuBase):
    pass

class Lieu(LieuBase):
    id: int

    class Config:
        orm_mode = True


# -------- MICROCONTROLEURS --------
class MicrocontroleurBase(BaseModel):
    uuid: str
    nom: Optional[str] = None

class MicrocontroleurCreate(MicrocontroleurBase):
    lieu_id: int  # pour l'affectation initiale

class Microcontroleur(MicrocontroleurBase):
    date_affectation: datetime
    lieu_id: Optional[int] = None

    class Config:
        orm_mode = True
