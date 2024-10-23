"""
Reads the clean .csv tables in clean-tables and creates an sqlite database out of them, 
saving them to the .db file named CoFID_complete_nutritional_data.db
"""

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine('sqlite:///CoFID_complete_nutritional_data.db', echo=False)
Base = declarative_base()

from sqlalchemy.orm import relationship, backref

class Foods(Base):
    __tablename__ = 'complete_nutritional_data'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    energy = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbohydrate = Column(Float)
    aoac = Column(Float)
    satd = Column(Float)
    n_6 = Column(Float)
    n_3 = Column(Float)
    mono = Column(Float)
    poly = Column(Float)
    trans = Column(Float)
    cholesterol = Column(Float)
    sodium = Column(Float)
    potassium = Column(Float)
    calcium = Column(Float)
    magnesium = Column(Float)
    phosphorus = Column(Float)
    iron = Column(Float)
    copper = Column(Float)
    zinc = Column(Float)
    chloride = Column(Float)
    manganese = Column(Float)
    selenium = Column(Float)
    iodine = Column(Float)
    retinol = Column(Float)
    carotene = Column(Float)
    retinol_equivalent = Column(Float)
    d = Column(Float)
    e = Column(Float)
    k = Column(Float)
    thiamin = Column(Float)
    riboflavin = Column(Float)
    niacin = Column(Float)
    tryptophan_60 = Column(Float)
    niacin_equivalent = Column(Float)
    b6 = Column(Float)
    b12 = Column(Float)
    folate = Column(Float)
    pantothenate = Column(Float)
    biotin = Column(Float)
    c = Column(Float)
    alpha_carotene = Column(Float)
    beta_carotene = Column(Float)
    lutein = Column(Float)
    lycopene = Column(Float)

    def __repr__(self):
        return '''<Foods(id='{0}', name='{1}', energy='{2}', protein='{3}', 
        fat='{4}', carbohydrate='{5}', aoac='{6}', satd='{7}', n_6='{8}', 
        n_3='{9}', mono='{10}', poly='{11}', trans='{12}', cholesterol='{13}', 
        sodium='{14}', potassium='{15}', calcium='{16}', magnesium='{17}', 
        phosphorus='{18}', iron='{19}', copper='{20}', zinc='{21}', chloride='{22}', 
        manganese='{23}', selenium='{24}', iodine='{25}', retinol='{26}', 
        carotene='{27}', retinol_equivalent='{28}', d='{29}', e='{30}', k='{31}', 
        thiamin='{32}', riboflavin='{33}', niacin='{34}', tryptophan_60='{35}', 
        niacin_equivalent='{36}', b6='{37}', b12='{38}', folate='{39}', 
        pantothenate='{40}', biotin='{41}', c='{42}', alpha_carotene='{43}', 
        beta_carotene='{44}', lutein='{45}', lycopene='{46}')>'''.format(
            self.id, self.name, self.energy, self.protein, self.fat, self.carbohydrate, 
            self.aoac, self.satd, self.n_6, self.n_3, self.mono, self.poly, self.trans, 
            self.cholesterol, self.sodium, self.potassium, self.calcium, self.magnesium, 
            self.phosphorus, self.iron, self.copper, self.zinc, self.chloride, 
            self.manganese, self.selenium, self.iodine, self.retinol, self.carotene, 
            self.retinol_equivalent, self.d,  self.e, self.k, self.thiamin, 
            self.riboflavin, self.niacin, self.tryptophan_60, self.niacin_equivalent,  
            self.b6, self.b12, self.folate, self.pantothenate, self.biotin, self.c, 
            self.alpha_carotene, self.beta_carotene, self.lutein, self.lycopene)

if __name__ == '__main__':
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    results = s.query(Foods).limit(10).all()
    for r in results:
        print(r)

Base.metadata.create_all(engine)
file_name = './clean-tables/complete_nutritional_data.csv'
df = pd.read_csv(file_name)

df.to_sql(con=engine, name=Foods.__tablename__, if_exists='replace', index=False)

