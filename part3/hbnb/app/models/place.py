#!/usr/bin/python3
from .baseclass import BaseModel
from part3.hbnb.app.models.user import User
from part3.hbnb.app import bcrypt, db


class Place(BaseModel):
    __tablename__ = 'place'
    __table_args__ = {'extend_existing': True}

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        # Validations
        self.validations()

    def validations(self):
        # Ensure the owner exists
        user = db.session.query(User).filter_by(id=self.owner_id).first()
        if not user:
            raise ValueError('Owner must be a valid User')

        # Validates required length of title
        if not self.title or len(self.title) > 100:
            raise ValueError('Maximum length of 100 characters')

        # Price must be a positive value
        if self.price < 1:
            raise ValueError('Price must be greater than 0')

        # Latitude must be within the range of -90.0 to 90.0.
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError('Latitude must be between -90 and 90')
        # Longitude must be within the range of -180.0 to 180.0.
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError('Longitude must be between -180 and 180')

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
