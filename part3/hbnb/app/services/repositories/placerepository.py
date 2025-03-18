from part3.hbnb.app.models.place import Place
from part3.hbnb.app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
