from app.persistence.repository import InMemoryRepository
from typing import List, Dict, Optional
from datetime import datetime
from models.review import Review
from models.exceptions import ResourceNotFoundError, ValidationError

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

class HBnBFacade:
    def __init__(self, storage):
        self.storage = storage

    def create_review(self, review_data: Dict) -> Review:
        """
        Creates a new review with validation.
        
        Args:
            review_data: Review data including text, rating, user_id, place_id
            
        Returns:
            Review: The created review
            
        Raises:
            ValidationError: If data is invalid
            ResourceNotFoundError: If user or place doesn't exist
        """
        self._validate_review_data(review_data)
        
        # Check if user and place exist
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
            place_id=review_data['place_id']
        )
        
        self.storage.save(review)
        return review

    def get_review(self, review_id: str) -> Review:
        """
        Retrieves a review by its ID.
        
        Args:
            review_id: The review identifier
            
        Returns:
            Review: The found review
            
        Raises:
            ResourceNotFoundError: If review doesn't exist
        """
        review = self.storage.get(Review, review_id)
        if not review:
            raise ResourceNotFoundError(f"Review {review_id} not found")
        return review

    def get_all_reviews(self) -> List[Review]:
        """
        Retrieves all reviews.
        
        Returns:
            List[Review]: List of all reviews
        """
        return self.storage.all(Review)

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """
        Retrieves all reviews for a specific place.
        
        Args:
            place_id: The place identifier
            
        Returns:
            List[Review]: List of reviews for this place
            
        Raises:
            ResourceNotFoundError: If place doesn't exist
        """
        place = self.storage.get("Place", place_id)
        if not place:
            raise ResourceNotFoundError(f"Place {place_id} not found")
            
        return [review for review in self.get_all_reviews() 
                if review.place_id == place_id]

    def update_review(self, review_id: str, review_data: Dict) -> Review:
        """
        Updates an existing review.
        
        Args:
            review_id: The review identifier
            review_data: New review data
            
        Returns:
            Review: The updated review
            
        Raises:
            ResourceNotFoundError: If review doesn't exist
            ValidationError: If data is invalid
        """
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
        """
        Deletes a review.
        
        Args:
            review_id: The review identifier
            
        Raises:
            ResourceNotFoundError: If review doesn't exist
        """
        review = self.get_review(review_id)
        self.storage.delete(review)

    def _validate_review_data(self, data: Dict, update: bool = False) -> None:
        """
        Validates review data.
        
        Args:
            data: Data to validate
            update: If True, validation for update
            
        Raises:
            ValidationError: If data is invalid
        """
        if not update:
            required_fields = ['text', 'rating', 'user_id', 'place_id']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Field {field} is required")

        if 'text' in data and not data['text'].strip():
            raise ValidationError("Review text cannot be empty")
            
        if 'rating' in data:
            rating = data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValidationError("Rating must be an integer between 1 and 5")

