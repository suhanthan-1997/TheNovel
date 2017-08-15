from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class login(Base):
    __tablename__ = 'login'
    username = Column(Text, primary_key=True)
    password = Column(Text)
