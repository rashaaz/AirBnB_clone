#!/usr/bin/python3
"""Test Module for Review Model"""

import unittest
from datetime import datetime
import time
from models.review import Review
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestReviewModel(unittest.TestCase):

    """Test cases for the Review model class."""

    def setUp(self):
        """Set up method to initialize test environment"""
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

    def test_review_instance_creation(self):
        """Test the creation of a Review instance."""

        bb = Review()
        self.assertEqual(str(type(bb)), "<class 'models.review.Review'>")
        self.assertIsInstance(bb, Review)
        self.assertTrue(issubclass(type(bb), BaseModel))

    def test_review_attributes(self):
        """Test the attributes of the Review class."""
        attributes = storage.attributes()["Review"]
        oo = Review()
        for kk, vv in attributes.items():
            self.assertTrue(hasattr(oo, kk))
            self.assertEqual(type(getattr(oo, kk, None)), vv)


if __name__ == "__main__":
    unittest.main()
