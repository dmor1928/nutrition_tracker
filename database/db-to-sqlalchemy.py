from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

engine = create_engine('sqlite:///CoFID_2021_nutrition_information.db', echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

from sqlalchemy.orm import relationship, backref

class Foods(Base):
    __table__ = Base.metadata.tables['complete_nutritional_data']

if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessionmaker(bind=engine))
    for item in db_session.query(Foods.id, Foods.name):
        print(item)