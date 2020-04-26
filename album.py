import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///Модуль B/B6. Обработка исключений. Веб-сервер/Практическое задание/albums.sqlite3"
Base = declarative_base()


class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find_artist(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def find_same_album(artist, album):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist, Album.album == album).first()
    return albums

def save(album_data):
    session = connect_db()

    year = album_data["year"]
    artist = album_data["artist"]
    genre = album_data["genre"]
    album = album_data["album"]

    album_item = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    session.add(album_item)
    session.commit()
    print("Спасибо. Данные сохранены")