#!/usr/bin/python3
"""BaseModel Module"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:

    """BaseModel class for other classes to inherit"""

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel"""

        if kwargs is not None and kwargs != {}:
            for ky in kwargs:
                if ky == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif ky == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[ky] = kwargs[ky]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return a string representation of the BaseModel"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update the 'updated_at' attribute and save to storage"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel"""

        m_di = self.__dict__.copy()
        m_di["__class__"] = type(self).__name__
        m_di["created_at"] = m_di["created_at"].isoformat()
        m_di["updated_at"] = m_di["updated_at"].isoformat()
        return m_di
