#!/usr/bin/python3


from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = amenities


    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) > 100:
            raise ValueError("Title must be a string with a maximum length of 100 characters.")
        self.__title = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Description must be a string or None.")
        self.__description = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number.")
        self.__price = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be a number between -90.0 and 90.0.")
        self.__latitude = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be a number between -180.0 and 180.0.")
        self.__longitude = value

    @property
    def owner_id(self):
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str):
            raise ValueError("Owner ID must be a string.")
        self.__owner_id = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
