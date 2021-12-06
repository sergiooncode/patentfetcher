from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base


class ModelBase:
    def save(self):
        session.session.add(self)
        self.__commit()
        return self

    def bulk_save(self):
        session.session.add_all(self)
        session.session.commit()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def __commit(self):
        try:
            session.session.commit()
        except DatabaseError:
            session.session.rollback()
            raise


session = SQLAlchemy(model_class=declarative_base(cls=ModelBase))

from src.patents.infrastructure.models.patent import (
    Patent,
)
