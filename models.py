from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ARRAY, ForeignKey, BigInteger
from sqlalchemy.types import UserDefinedType
from database import Base

class Point(UserDefinedType):
    def get_col_spec(self):
        return "POINT"

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    chatgpt_prompt = Column(Text, nullable=False)
    picture_links = Column(ARRAY(String))
    location = Column(Point)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class UserDialog(Base):
    __tablename__ = "user_dialogs"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    message_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    place_id = Column(Integer, ForeignKey('places.id'))
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
