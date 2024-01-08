#!/usr/bin/python3
"""
Unit tests for the FileStorage class.
"""
from datetime import datetime
import unittest
from time import sleep
import json
from models.engine.file_storage import FileStorage


class test_fileStorage(unittest.TestCase):
    """TestFileStorage class contains unit tests for the FileStorage class."""
    def test_instance_creation(self):
        """Test if a FileStorage instance is created successfully."""
        ob = FileStorage()
        self.assertIsInstance(ob, FileStorage)

    def test_methods_existence(self):
        """Test if the necessary methods exist in the FileStorage class."""
        self.assertIsNotNone(FileStorage.all)
        self.assertIsNotNone(FileStorage.new)
        self.assertIsNotNone(FileStorage.save)
        self.assertIsNotNone(FileStorage.reload)

    if __name__ == '__main__':
        unittest.main()
