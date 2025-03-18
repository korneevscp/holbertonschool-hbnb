#!/usr/bin/python3
from part3.hbnb.app.models.baseclass import BaseModel
from part3.hbnb.app import bcrypt, db
import uuid
import re


class Amenity(BaseModel):
    __tablename__ = 'amenity'

    __table_args__ = {'extend_existing': True}

    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

        # Validations
        self.amenity_validation()

    def amenity_validation(self):
        # Required, maximum length of 50 characters.
        if not self.name or len(self.name) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
