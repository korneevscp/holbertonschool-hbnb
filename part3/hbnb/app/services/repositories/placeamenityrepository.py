from part3.hbnb.app.models.placeamenity import PlaceAmenity
from part3.hbnb.app.persistence.repository import SQLAlchemyRepository


class PlaceAmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(PlaceAmenity)

    def get_by_attribute(self, attribute_name, attribute_value):
        return self.model.query(PlaceAmenity).filter_by(**{attribute_name: attribute_value}).all()
