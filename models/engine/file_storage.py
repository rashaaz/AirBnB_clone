#!/usr/bin/python3
"""File Storage Module"""
import datetime
import json
import os


class FileStorage:

    """File Storage Class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Get all stored objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to storage"""
        ky = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[ky] = obj

    def save(self):
        """Save objects to JSON file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as fa:
            dd = {r: s.to_dict() for r, s in FileStorage.__objects.items()}
            json.dump(dd, fa)

    def classes(self):
        """Get classes for different objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def reload(self):
        """Reload objects from JSON file"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as fa:
            o_d = json.load(fa)
            o_d = {r: self.classes()[s["__class__"]](**s)
                   for r, s in o_d.items()}
            FileStorage.__objects = o_d

    def attributes(self):
        """Get attributes for different classes"""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
