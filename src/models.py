import os
import sys
import enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, String, Integer, ForeignKey, Enum, Table, Column
from sqlalchemy.ext.declarative import DeclarativeMeta
from eralchemy2 import render_er

Base: DeclarativeMeta = declarative_base()

character_episode = Table(
    'character_episode', Base.metadata,
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True),
    Column('episode_id', Integer, ForeignKey('episode.id'), primary_key=True)
)

favorite_character = Table(
    'favorite_character', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

favorite_location = Table(
    'favorite_location', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('location_id', Integer, ForeignKey('location.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    reviews = relationship('Review', back_populates='user')
    favorite_characters = relationship('Character')
    favorite_locations = relationship('Location')

class Location(Base):
    __tablename__ = 'location'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    dimension: Mapped[str] = mapped_column(nullable=False)

    characters = relationship('Character')
    favorited_by = relationship('User')

class Character(Base):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    species: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    
    origin_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))

    origin = relationship('Location', foreign_keys=[origin_id])
    location = relationship('Location', foreign_keys=[location_id])
    episodes = relationship('Episode')
    reviews = relationship('Review')
    favorited_by = relationship('User')

class Episode(Base):
    __tablename__ = 'episode'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    air_date: Mapped[str] = mapped_column(nullable=False)
    episode_code: Mapped[str] = mapped_column(nullable=False)

    characters = relationship('Character')

class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'))

    user = relationship('User')
    character = relationship('Character')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
