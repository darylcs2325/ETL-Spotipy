from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from cfg import DB_CONNSTR

print(DB_CONNSTR)
engine = create_engine(DB_CONNSTR)
meta = MetaData(engine)
Base = declarative_base(metadata=meta)

TABLENAME = "musicas_spotipy"


class Musica(Base):
    __tablename__ = TABLENAME
    played_at = Column(TIMESTAMP(), primary_key=True)
    duration = Column(String(20), nullable=False, unique=False)
    album = Column(String(100), nullable=False, unique=False)
    popularity = Column(Integer(), nullable=False, unique=False)

    def __str__(self):
        return self.album


session = sessionmaker(engine)

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("HECHO2")
