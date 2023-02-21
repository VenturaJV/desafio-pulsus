from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: int = Column(Integer, primary_key=True, index=True)

    locations = relationship("Location", back_populates="device")


class Location(Base):
    __tablename__ = "locations"

    id: int = Column(Integer, primary_key=True, index=True)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)
    device_id: int = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="locations")
