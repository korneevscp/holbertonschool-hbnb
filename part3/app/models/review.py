#!/usr/bin/python3


from .base_model import BaseModel
from .place import Place
from .user import User


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Review text is required and must be a string.")
        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.__rating = value

    @property
    def place_id(self):
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        if value is None or not isinstance(value, str) or not value:
            raise ValueError("Place ID is required and must be a string.")
        self.__place_id = value

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        if value is None or not isinstance(value, str) or not value:
            raise ValueError("User ID is required and must be a string.")
        self.__user_id = value
