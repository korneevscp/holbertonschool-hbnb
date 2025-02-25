from app.persistence.repository import InMemoryRepository
from typing import List, Dict
from datetime import datetime
from app.models.review import Review
from models.user import User
from models.exceptions import ResourceNotFoundError, ValidationError

class HBnBFacade:
    def __init__(self, storage=None):
        self.user_repo = InMemoryRepository()
        self.storage = storage or InMemoryRepository()  # Unification du stockage

    # =====================
    # Gestion des utilisateurs
    # =====================
    
    def create_user(self, user_data: Dict) -> User:
        """Crée un utilisateur et l'ajoute au stockage."""
        user = User(**user_data, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User:
        """Récupère un utilisateur par son ID."""
        user = self.user_repo.get(user_id)
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")
        return user

    def get_user_by_email(self, email: str) -> User:
        """Récupère un utilisateur par email."""
        user = next((u for u in self.user_repo.all(User) if u.email == email), None)
        if not user:
            raise ResourceNotFoundError(f"User with email {email} not found")
        return user

    # =====================
    # Gestion des avis (Reviews)
    # =====================

    def create_review(self, review_data: Dict) -> Review:
        """Crée un avis après validation."""
        self._validate_review_data(review_data)

        # Vérification avec la même source de vérité pour les utilisateurs
        user = self.get_user(review_data['user_id'])  
        place = self.storage.get("Place", review_data['place_id'])

        if not place:
            raise ResourceNotFoundError(f"Place {review_data['place_id']} not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user.id,  # Assurer la cohérence
            place_id=review_data['place_id'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.storage.save(review)
        return review

    def get_review(self, review_id: str) -> Review:
        """Récupère un avis par ID."""
        review = self.storage.get("Review", review_id)
        if not review:
            raise ResourceNotFoundError(f"Review {review_id} not found")
        return review

    def get_all_reviews(self) -> List[Review]:
        """Récupère tous les avis."""
        return self.storage.all(Review)

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """Récupère les avis pour un lieu donné."""
        place = self.storage.get("Place", place_id)
        if not place:
            raise ResourceNotFoundError(f"Place {place_id} not found")

        return [review for review in self.get_all_reviews() if review.place_id == place_id]

    def update_review(self, review_id: str, review_data: Dict) -> Review:
        """Met à jour un avis existant."""
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
        """Supprime un avis."""
        review = self.get_review(review_id)
        self.storage.delete(review)

    # =====================
    # Validation des données
    # =====================

    def _validate_review_data(self, data: Dict, update: bool = False) -> None:
        """Valide les données des avis."""
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
