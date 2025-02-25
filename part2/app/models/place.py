#!/usr/bin/python3
from typing import List, Optional
from models.base_model import BaseModel
from models.user import User

class Place(BaseModel):
    def __init__(self, title: str, description: Optional[str], price: float,
                 latitude: float, longitude: float, owner: User):
        super().__init__()
        self.validate_title(title)
        self.validate_coordinates(latitude, longitude)
        self.validate_price(price)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews: List['Review'] = []
        self.amenities: List['Amenity'] = []

    @staticmethod
    def validate_title(title: str):
        if not title or len(title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")

    @staticmethod
    def validate_coordinates(lat: float, lon: float):
        if not -90 <= lat <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= lon <= 180:
            raise ValueError("Longitude must be between -180 and 180")

    @staticmethod
    def validate_price(price: float):
        if price <= 0:
            raise ValueError("Price must be positive")

    def add_review(self, review: 'Review'):
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity: 'Amenity'):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()
