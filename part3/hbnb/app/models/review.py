from .baseclass import BaseModel
from part3.hbnb.app import db


class Review(BaseModel):
    __tablename__ = 'review'
    __table_args__ = {'extend_existing': True}

    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        self.validations()

    def validations(self):
        # Rating validation, must be between 0 and 5
        if self.rating < 0 or self.rating > 5:
            raise ValueError("Rating must be between 0 and 5")

        # Review text can't be empty
        if self.text is None:
            raise ValueError("Review required")

        # Validate place and user ids to ensure they are properly assigned
        if not isinstance(self.place_id, str) or not self.place_id:
            raise ValueError("Place ID must be valid.")

        if not isinstance(self.user_id, str) or not self.user_id:
            raise ValueError("User ID must be valid.")

