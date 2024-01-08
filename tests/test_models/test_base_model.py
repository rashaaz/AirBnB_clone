#!/usr/bin/python3
"""This module contains unit tests for test_base_model.py"""

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import json
import os
import re
import time
import unittest
import uuid


class TestBaseModelMethods(unittest.TestCase):

    """Test methods for the BaseModel class"""

    def setUp(self):
        """Set up test environment"""
        pass

    def tearDown(self):
        """Tear down test environment"""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Reset the storage environment"""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_create_base_model(self):
        """Test creating an instance of BaseModel"""

        c = BaseModel()
        self.assertEqual(str(type(c)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(c, BaseModel)
        self.assertTrue(issubclass(type(c), BaseModel))

    def test_init_without_arguments(self):
        """Test initializing BaseModel without arguments"""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.__init__()
        ms = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(ee.exception), ms)

    def test_init_with_args(self):
        """Test initializing BaseModel with arguments"""
        self.resetStorage()
        args = [ii for ii in range(10000)]
        bb = BaseModel(10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
        bb = BaseModel(*args)

    def test_attributes(self):
        """Test BaseModel attributes"""

        attributes = storage.attributes()["BaseModel"]
        oo = BaseModel()
        for kk, vv in attributes.items():
            self.assertTrue(hasattr(oo, kk))
            self.assertEqual(type(getattr(oo, kk, None)), vv)

    def test_date_time_diff(self):
        """Test date time difference in BaseModel"""
        d_n = datetime.now()
        bb = BaseModel()
        di = bb.updated_at - bb.created_at
        self.assertTrue(abs(di.total_seconds()) < 0.001)
        di = bb.created_at - d_n
        self.assertTrue(abs(di.total_seconds()) < 0.01)

    def test_id_uniqueness(self):
        """Test uniqueness of BaseModel IDs"""

        ll = [BaseModel().id for ii in range(10000)]
        self.assertEqual(len(set(ll)), len(ll))

    def test_save_and_updated_at(self):
        """Test BaseModel save and updated_at"""

        bb = BaseModel()
        time.sleep(0.05)
        d_n = datetime.now()
        bb.save()
        di = bb.updated_at - d_n
        self.assertTrue(abs(di.total_seconds()) < 0.001)

    def test_str_representation(self):
        """Test BaseModel string representation"""
        bb = BaseModel()
        rx = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        rs = rx.match(str(bb))
        self.assertIsNotNone(rs)
        self.assertEqual(rs.group(1), "BaseModel")
        self.assertEqual(rs.group(2), bb.id)
        ss = rs.group(3)
        ss = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", ss)
        dd = json.loads(ss.replace("'", '"'))
        dd22 = bb.__dict__.copy()
        dd22["created_at"] = repr(dd22["created_at"])
        dd22["updated_at"] = repr(dd22["updated_at"])
        self.assertEqual(dd, dd22)

    def test_to_dict(self):
        """Test BaseModel to_dict method"""

        bb = BaseModel()
        bb.name = "Laura"
        bb.age = 24
        dd = bb.to_dict()
        self.assertEqual(dd["id"], bb.id)
        self.assertEqual(dd["__class__"], type(bb).__name__)
        self.assertEqual(dd["created_at"], bb.created_at.isoformat())
        self.assertEqual(dd["updated_at"], bb.updated_at.isoformat())
        self.assertEqual(dd["name"], bb.name)
        self.assertEqual(dd["age"], bb.age)

    def test_to_dict_exception(self):
        """Test to_dict method exceptions"""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.to_dict()
        m = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(ee.exception), m)

    def test_create_from_dict(self):
        """Test creating BaseModel instance from dictionary"""
        self.resetStorage()
        with self.assertRaises(TypeError) as s:
            BaseModel.to_dict(self, 99)
        m = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(s.exception), m)

    def test_create_from_dict_with_diff_types(self):
        """Test creating BaseModel instance from dictionary"""

        m_m = BaseModel()
        m_m.name = "Holberton"
        m_m.my_number = 90
        m_m_j = m_m.to_dict()
        m_n_m = BaseModel(**m_m_j)
        self.assertEqual(m_n_m.to_dict(), m_m.to_dict())

    def test_model_to_dict_conversion(self):
        """Test the to_dict method of the BaseModel class."""
        dd = {"__class__": "BaseModel",
              "updated_at":
              datetime(2050, 12, 30, 23, 59, 59, 123456).isoformat(),
              "created_at": datetime.now().isoformat(),
              "id": uuid.uuid4(),
              "var": "foobar",
              "int": 108,
              "float": 3.14}
        oo = BaseModel(**dd)
        self.assertEqual(oo.to_dict(), dd)

    def test_save_to_file(self):
        """Test saving BaseModel instance to file"""
        self.resetStorage()
        bb = BaseModel()
        bb.save()
        ky = "{}.{}".format(type(bb).__name__, bb.id)
        dd = {ky: bb.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as fa:
            self.assertEqual(len(fa.read()), len(json.dumps(dd)))
            fa.seek(0)
            self.assertEqual(json.load(fa), dd)

    def test_save_without_self_argument(self):
        """Test calling save() without self argument"""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.save()
        m = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(ee.exception), m)

    def test_save_with_extra_argument(self):
        """Test calling save() with an extra argument"""
        self.resetStorage()
        with self.assertRaises(TypeError) as ee:
            BaseModel.save(self, 98)
        m = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(ee.exception), m)


if __name__ == '__main__':
    unittest.main()
