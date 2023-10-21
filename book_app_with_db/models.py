from sqlalchemy import Column, Integer, String
from database import Base


# this is going to be the table within the db we are creating
class Books(Base):
    # __tablename__ is a SQLAlchemy specific thing to be able to name our db table
    __tablename__ = "books"
    # below is the schema, the column names along with it's datatype
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)
