#!/usr/bin/python3
"""Unit tests for the State class."""

import unittest
from datetime import datetime
import time
from models.state import State
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestState(unittest.TestCase):

    """TestState class contains unit tests for the State class."""

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

    def test_state_creation(self):
        """
        Test if State instance is created
        successfully and inherits from BaseModel.
        """

        d = State()
        self.assertEqual(str(type(d)), "<class 'models.state.State'>")
        self.assertIsInstance(d, State)
        self.assertTrue(issubclass(type(d), BaseModel))

    def test_state_attributes(self):
        """Test if State instance has the correct attributes."""
        attributes = storage.attributes()["State"]
        a = State()
        for key, value in attributes.items():
            self.assertTrue(hasattr(a, key))
            self.assertEqual(type(getattr(a, key, None)), value)


if __name__ == "__main__":
    unittest.main()
