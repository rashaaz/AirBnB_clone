#!/usr/bin/python3
"""
Defines the Amenity class representing a
type of amenity in the application.
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class represents a type of amenity in the application."""
    name = ""
