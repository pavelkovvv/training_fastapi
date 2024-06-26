from sqlalchemy import Column, Integer, String

from database import Base


class Messages(Base):

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message = Column(String)

    def as_dict(self):
        """Сериализует данные в JSON."""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
