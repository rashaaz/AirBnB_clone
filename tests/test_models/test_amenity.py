#!/usr/bin/python3
"""Unit tests for the Amenity class"""

import unittest
from datetime import datetime
import time
from models.amenity import Amenity
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):

    """TestAmenity class contains unit tests for the Amenity class."""

    def setUp(self):
        """Set up any necessary resources for the tests."""
        pass

    def tearDown(self):
        """Clean up any resources used in the tests."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Reset the storage for testing purposes."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_amenity_creation(self):
        """
        Test if Amenity instance is
        created successfully and inherits from BaseModel.
        """

        r = Amenity()
        self.assertEqual(str(type(r)), "<class 'models.amenity.Amenity'>")
        self.assertIsInstance(r, Amenity)
        self.assertTrue(issubclass(type(r), BaseModel))

    def test_amenity_attributes(self):
        """Test if Amenity instance has the correct attributes."""
        attributes = storage.attributes()["Amenity"]
        n = Amenity()
        for key, value in attributes.items():
            self.assertTrue(hasattr(n, key))
            self.assertEqual(type(getattr(n, key, None)), value)


if __name__ == "__main__":
    unittest.main()
