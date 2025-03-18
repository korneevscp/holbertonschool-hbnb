#!/usr/bin/python3
from sqlalchemy import Column, String, ForeignKey
from part3.hbnb.app.models.baseclass import BaseModel


class PlaceAmenity(BaseModel):
    __tablename__ = 'place_amenity'
    __table_args__ = {'extend_existing': True}
    place_id = Column(String, ForeignKey('place.id'), nullable=False)
    amenity_id = Column(String, ForeignKey('place_amenity.id'), nullable=False)

    def __init__(self, place_id, amenity_id):
        super().__init__()
        self.place_id = place_id
        self.amenity_id = amenity_id
