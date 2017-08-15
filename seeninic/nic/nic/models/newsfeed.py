from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
	ForeignKey
)

from .meta import Base
from .login import login

class newsfeed(Base):
    __tablename__ = 'newsfeed'
    username = Column(Text)
    about = Column(Text)
    content = Column(Text,primary_key =True)
    submitted_date = Column(Text)
    submitted_time = Column(Text)
