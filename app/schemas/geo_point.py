from pydantic import BaseModel


class GeoPointSchema(BaseModel):
    name: str
    address: str | None

    class Config:
        from_attributes = True
