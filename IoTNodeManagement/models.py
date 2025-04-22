# models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from database import Base

def utc_now():
    return datetime.now(timezone.utc)
class Lieux(Base):
    __tablename__ = "lieux"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)

    # relation avec les microcontrôleurs
    microcontroleurs = relationship("Microcontroleur", back_populates="lieu")


class Microcontroleur(Base):
    __tablename__ = "microcontroleurs"

    uuid = Column(String, primary_key=True, index=True)
    nom = Column(String)
    lieu_id = Column(Integer, ForeignKey("lieux.id"))
    date_affectation = Column(DateTime, default=utc_now)

   # date_affectation = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))

    # relation vers le lieu
    lieu = relationship("Lieux", back_populates="microcontroleurs")
