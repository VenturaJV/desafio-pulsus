from pydantic import BaseModel


class LocationOutput(BaseModel):
    longitude: float
    latitude: float
    id: int
    device_id: int

    class Config:
        orm_mode = True


class LocationInput(BaseModel):
    latitude: float
    longitude: float
    device_id: int
