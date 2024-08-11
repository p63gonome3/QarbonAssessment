from pydantic import BaseModel, Field
from enum import Enum


class Face(str, Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class Coordinate(BaseModel):
    x: int = Field(ge=0, le=5)
    y: int = Field(ge=0, le=5)
    face: Face


FACES = [face.value for face in Face]
