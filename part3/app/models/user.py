#!/usr/bin/python3

from .base_model import BaseModel
import re
import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)  # Hachage du mot de passe lors de l'initialisation
        self.is_admin = is_admin

    # ---- Gestion du prénom ----
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

    # ---- Gestion du nom ----
    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string.")
        if len(value) > 50:
            raise ValueError("Maximum length of 50 characters.")
        self.__last_name = value

    # ---- Gestion de l'email ----
    @property
    def email(self):
        return self.__email

    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @email.setter
    def email(self, value):
        if not self.is_valid_email(value):
            raise ValueError("Invalid email format.")
        self.__email = value

    # ---- Gestion du mot de passe avec hachage ----
    @property
    def password(self):
        return self.__password  # Ne retourne pas directement le hash

    def hash_password(self, password):
        """Hache le mot de passe avant de le stocker."""
        if not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be a string of at least 6 characters.")
        self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe en clair correspond au hash stocké."""
        return bcrypt.checkpw(password.encode('utf-8'), self.__password.encode('utf-8'))

    # ---- Gestion de is_admin ----
    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Admin must be a boolean.")
        self.__is_admin = value