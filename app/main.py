from typing import List

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from app.models import Location, Device
from app.database import engine, Base, get_db
from app.schemas import LocationInput, LocationOutput

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/locations", status_code=status.HTTP_201_CREATED)
def create_location(locations: List[LocationInput], db: Session = Depends(get_db)):
    for location in locations:
        db_location = db.query(Location).filter(Location.device_id == location.device_id,
                                                Location.longitude == location.longitude,
                                                Location.latitude == location.latitude).first()
        if not db_location:
            db_location = Location(
                device_id=location.device_id,
                latitude=location.latitude,
                longitude=location.longitude
            )
            db.add(db_location)
            db_device = db.query(Device).filter(Device.id == location.device_id).first()
            if not db_device:
                db_device = Device(id=location.device_id)
                db.add(db_device)
            db.commit()
            db.refresh(db_location)
    return locations


@app.get("/locations/", response_model=List[LocationOutput])
def read_locations(device_id: int = None, db: Session = Depends(get_db)):
    if device_id:
        return db.query(Location).filter(Location.device_id == device_id).all()
    else:
        return db.query(Location).all()


# TODO - Remover esses dois metodos que são apenas para teste
@app.get("/devices")
def find_all(db: Session = Depends(get_db)):
    return db.query(Device).all()


@app.delete("/delete")
def delete_all(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    for device in devices:
        db.query(Device).filter(Device.id == device.id).delete()
    positions = db.query(Location).all()
    for position in positions:
        db.query(Location).filter(Location.id == position.id).delete()
    db.commit()
