#!/usr/bin/python3
"""Test Module for User Model"""

import unittest
from datetime import datetime
import time
from models.user import User
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestUserModel(unittest.TestCase):

    """Test cases for the User model class"""

    def setUp(self):
        """Set up method to initialize test environment."""
        pass

    def tearDown(self):
        """Tear down method to clean up after each test."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Reset the FileStorage objects and remove the file path."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_user_instance_creation(self):
        """Test the creation of a User instance."""

        c = User()
        self.assertEqual(str(type(c)), "<class 'models.user.User'>")
        self.assertIsInstance(c, User)
        self.assertTrue(issubclass(type(c), BaseModel))

    def test_user_attributes(self):
        """Test the attributes of the User class."""
        attributes = storage.attributes()["User"]
        oo = User()
        for r, s in attributes.items():
            self.assertTrue(hasattr(oo, r))
            self.assertEqual(type(getattr(oo, r, None)), s)


if __name__ == "__main__":
    unittest.main()
