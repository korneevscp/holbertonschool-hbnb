# models/amenity.py
from models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name: str):
        if not name or len(name) > 50:
            raise ValueError("Name must be between 1 and 50 characters")
