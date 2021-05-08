from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class Models(Base):
    __tablename__ = 'models'

    id: int
    manufacturer: str
    year: int
    customer_id: int

    id = Column(Integer, primary_key=True)
    manufacturer = Column(String)
    year = Column(Integer)
    customer_id = Column(Integer)


@dataclass
class Customers(Base):
    __tablename__ = 'customers'

    id: int
    first_name: str
    family_name: str
    age: int

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    family_name = Column(String)
    age = Column(Integer)
