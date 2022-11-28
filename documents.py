from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import ARRAY

from config import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    created_date = Column(Date, nullable=False)
    rubrics = Column(ARRAY(String), nullable=False)
