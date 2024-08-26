from pydantic import BaseModel


class LinkedDistanceSchema(BaseModel):
    name: str
    distance: float

    class Config:
        from_attributes = True
