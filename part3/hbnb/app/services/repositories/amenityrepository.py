from part3.hbnb.app.models.amenity import Amenity
from part3.hbnb.app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
