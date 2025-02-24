from app.persistence.repository import InMemoryRepository
from typing import List, Dict
from datetime import datetime
from models.review import Review
from models.user import User
from models.exceptions import ResourceNotFoundError, ValidationError

class HBnBUserFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data: Dict) -> User:
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User:
        user = self.user_repo.get(user_id)
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.user_repo.get_by_attribute('email', email)
        if not user:
            raise ResourceNotFoundError(f"User with email {email} not found")
        return user

class HBnBFacade:
    def __init__(self, storage):
        self.storage = storage

    def create_review(self, review_data: Dict) -> Review:
        self._validate_review_data(review_data)

        user = self.storage.get("User", review_data['user_id'])
        place = self.storage.get("Place", review_data['place_id'])

        if not user:
            raise ResourceNotFoundError(f"User {review_data['user_id']} not found")
        if not place:
            raise ResourceNotFoundError(f"Place {review_data['place_id']} not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.storage.save(review)
        return review

    def get_review(self, review_id: str) -> Review:
        review = self.storage.get("Review", review_id)
        if not review:
            raise ResourceNotFoundError(f"Review {review_id} not found")
        return review

    def get_all_reviews(self) -> List[Review]:
        return self.storage.all(Review)

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        place = self.storage.get("Place", place_id)
        if not place:
            raise ResourceNotFoundError(f"Place {place_id} not found")

        return [review for review in self.get_all_reviews() if review.place_id == place_id]

    def update_review(self, review_id: str, review_data: Dict) -> Review:
        review = self.get_review(review_id)
        self._validate_review_data(review_data, update=True)

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        review.updated_at = datetime.utcnow()
        self.storage.save(review)
        return review

    def delete_review(self, review_id: str) -> None:
        review = self.get_review(review_id)
        self.storage.delete(review)

    def _validate_review_data(self, data: Dict, update: bool = False) -> None:
        if not update:
            required_fields = ['text', 'rating', 'user_id', 'place_id']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Field {field} is required")

        if 'text' in data and not data['text'].strip():
            raise ValidationError("Review text cannot be empty")

        if 'rating' in data:
            rating = data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValidationError("Rating must be an integer between 1 and 5")
