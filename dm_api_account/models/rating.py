from pydantic import BaseModel


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int
