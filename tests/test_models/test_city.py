#!/usr/bin/python3
"""This is a Python tests"""

import unittest
from datetime import datetime
import time
from models.city import City
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestCity(unittest.TestCase):

    """Test suite for City class"""

    def setUp(self):
        """Set up test environment"""
        pass

    def tearDown(self):
        """Tear down test environment"""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Test City instance creation"""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_city_instance_creation(self):
        """Test City instance creation"""

        bb = City()
        self.assertEqual(str(type(bb)), "<class 'models.city.City'>")
        self.assertIsInstance(bb, City)
        self.assertTrue(issubclass(type(bb), BaseModel))

    def test_city_attributes(self):
        """test_city_attributes"""
        attributes = storage.attributes()["City"]
        oo = City()
        for kk, vv in attributes.items():
            self.assertTrue(hasattr(oo, kk))
            self.assertEqual(type(getattr(oo, kk, None)), vv)


if __name__ == "__main__":
    unittest.main()
