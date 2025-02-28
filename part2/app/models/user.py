#!/usr/bin/python3


from .base_model import BaseModel
import re


class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin


@property
def first_name(self):
    return self.__first_name

@first_name.setter
def first_name(self, value):
    if not isinstance(value, str):
        raise TypeError("First name must be a string.")
    if len(value) > 50:
        raise ValueError("Maximum length of 50 characters.")
    self.__first_name = value


@property
def last_name(self):
    return self.__last_name

@last_name.setter
def last_name(self, value):
    if not isinstance(value, str):
        raise TypeError ("Last name must be a string.")
    if len(value) > 50:
        raise ValueError("Maximum length of 50 charcters.")
    self.__last_name = value


@property
def email(self):
    return self.__email

def is_valid_email(self, email):
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    return re.match(email_regex, email) is not None

@email.setter
def email(self, value):
    if not self.is_valid_email(value):
        raise ValueError ("Invalid email format.")
    self.__email = value


@property
def is_admin(self):
    return self.__is_admin

@is_admin.setter
def is_admin(self, value):
    if not isinstance (value, bool):
        raise TypeError ("Admin must be a boolean.")
    self.__is_admin = value
