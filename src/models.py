import enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Double, String, Enum
from sqlalchemy.orm import declarative_base
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    # See https://docs.sqlalchemy.org/en/20/core/defaults.html
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

# I will use enums to ensure the strings are only the ones specified. See
# https://docs.python.org/3/library/enum.html
# https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum

class ItemType(enum.Enum):
    CHARACTER = "character"
    FILM = "film"
    MANUFACTURER = "manufacturer"
    PERSON = "person"
    PLANET = "planet"
    SPECIES = "species"
    STARSHIP = "starship"
    VEHICLE = "vehicle"

class Favorite(Base):
    __tablename__ = "favorite"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    type = Column(Enum(ItemType), nullable=False)

class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "unknown"
    AGENDER = "n/a"

# I will not be able to control these tables as my enums, so will use the UNIQUE constraint.
# See https://docs.sqlalchemy.org/en/20/core/constraints.html#unique-constraint

class Color(Base):
    __tablename__ = "color"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True)
    homeworld = Column(Integer, ForeignKey("planet.id"))
    eye_color_id = Column(Integer, ForeignKey("color.id"))
    hair_color_id = Column(Integer, ForeignKey("color.id"))
    skin_color_id = Column(Integer, ForeignKey("color.id"))
    name = Column(String, nullable=False)
    birth_year = Column(String)
    gender = Column(Enum(Gender), nullable=False)
    height = Column(Double, nullable=False)
    mass = Column(Double, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)

class Film(Base):
    __tablename__ = "film"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    episode_id = Column(Integer, nullable=False)
    opening_crawl = Column(String, nullable=False)
    release_date = Column(DateTime)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)

class Starship(Base):
    __tablename__ = "starship"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    starship_class = Column(String, nullable=False)
    cost_in_credits = Column(Double)
    length = Column(Double, nullable=False)
    crew = Column(Integer, nullable=False)
    passengers = Column(Integer, nullable=False)
    max_atmosphering_speed = Column(Double)
    hyperdrive_rating = Column(Double, nullable=False)
    mglt = Column(String, nullable=False)
    cargo_capacity = Column(Double, nullable=False)
    consumables = Column(String, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)

class Vehicle(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    vehicle_class = Column(String, nullable=False)
    length = Column(Double, nullable=False)
    cost_in_credits = Column(Double)
    crew = Column(Integer, nullable=False)
    passengers = Column(Integer, nullable=False)
    max_atmosphering_speed = Column(Double)
    cargo_capacity = Column(Double, nullable=False)
    consumables = Column(String, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)

class Species(Base):
    __tablename__ = "species"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    classification = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    average_height = Column(Double)
    average_lifespan = Column(Integer)
    language = Column(String, nullable=False)
    homeworld = Column(Integer, ForeignKey("planet.id"), nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)

class Climate(Base):
    __tablename__ = "climate"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)

class Terrain(Base):
    __tablename__ = "terrain"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)

class Planet(Base):
    __tablename__ = "planet"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    diameter = Column(Integer)
    rotation_period = Column(Integer, nullable=False)
    orbital_period = Column(Integer, nullable=False)
    gravity = Column(Double, nullable=False)
    population = Column(Integer)
    surface_water = Column(Double)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)

# I will represent individuals involved in the creation of films.
# Film schema attributes:
# director string -- The name of the director of this film.
# producer string -- The name(s) of the producer(s) of this film. Comma separated.
class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

# I will represent manufacturers associated with starships and vehicles.
# Starship and Vehicle attributes:
# manufacturer string -- The name of the manufacturer. For starships and vehicles, this can be a comma-separated list if there are multiple manufacturers.
class Manufacturer(Base):
    __tablename__ = "manufacturer"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

# I will be using composite primary keys.
# See https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html

class FilmDirector(Base):
    __tablename__ = "film_director"
    film_id = Column(Integer, ForeignKey("film.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), primary_key=True)

class FilmProducer(Base):
    __tablename__ = "film_producer"
    film_id = Column(Integer, ForeignKey("film.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), primary_key=True)

class FilmCharacter(Base):
    __tablename__ = "film_character"
    film_id = Column(Integer, ForeignKey("film.id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)

class FilmPlanet(Base):
    __tablename__ = "film_planet"
    film_id = Column(Integer, ForeignKey("film.id"), primary_key=True)
    planet_id = Column(Integer, ForeignKey("planet.id"), primary_key=True)

class FilmSpecies(Base):
    __tablename__ = "film_species"
    film_id = Column(Integer, ForeignKey("film.id"), primary_key=True)
    species_id = Column(Integer, ForeignKey("species.id"), primary_key=True)

class FilmStarship(Base):
    __tablename__ = "film_starship"
    film_id = Column(Integer, ForeignKey("film.id"), primary_key=True)
    starship_id = Column(Integer, ForeignKey("starship.id"), primary_key=True)

class FilmVehicle(Base):
    __tablename__ = "film_vehicle"
    film_id = Column(Integer, ForeignKey("film.id"), primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), primary_key=True)

class Resident(Base):
    __tablename__ = "resident"
    planet_id = Column(Integer, ForeignKey("planet.id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)

class ColorType(enum.Enum):
    EYE = "eye"
    HAIR = "hair"
    SKIN = "skin"

class SpeciesColor(Base):
    __tablename__ = "species_color"
    id = Column(Integer, primary_key=True)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
    color_id = Column(Integer, ForeignKey("eye_color.id"), nullable=False)
    color_type = Column(Enum(ColorType), nullable=False)

class SpeciesIndividual(Base):
    __tablename__ = "species_individual"
    species_id = Column(Integer, ForeignKey("species.id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)

class StarshipPilot(Base):
    __tablename__ = "starship_pilot"
    starship_id = Column(Integer, ForeignKey("starship.id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)

class VehiclePilot(Base):
    __tablename__ = "vehicle_pilot"
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.id"), primary_key=True)

class StarshipManufacturer(Base):
    __tablename__ = "starship_manufacturer"
    starship_id = Column(Integer, ForeignKey("starship.id"), primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"), primary_key=True)

class VehicleManufacturer(Base):
    __tablename__ = "vehicle_manufacturer"
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"), primary_key=True)

class PlanetClimate(Base):
    __tablename__ = "planet_climate"
    planet_id = Column(Integer, ForeignKey("planet.id"), primary_key=True)
    climate_id = Column(Integer, ForeignKey("climate.id"), primary_key=True)

class PlanetTerrain(Base):
    __tablename__ = "planet_terrain"
    planet_id = Column(Integer, ForeignKey("planet.id"), primary_key=True)
    terrain_id = Column(Integer, ForeignKey("terrain.id"), primary_key=True)

# Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
