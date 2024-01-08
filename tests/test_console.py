#!/usr/bin/python3
"""Test cases for HBNBCommand prompt behavior."""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
    """Test if HBNBCommand initializes the correct prompt."""

    def test_prompt_initialization(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_prompt_output_on_empty_input(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Test cases for HBNBCommand help command."""

    def test_help_quit_command(self):
        n = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_create_command(self):
        n = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_eof_command(self):
        n = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_show_command(self):
        n = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_destroy_command(self):
        n = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_all_command(self):
        n = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_count_command(self):
        n = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_update_command(self):
        n = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(n, output.getvalue().strip())

    def test_help_general_command(self):
        n = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(n, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Test cases for HBNBCommand exit command."""

    def test_exit_quit(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_exit_eof(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Test cases for HBNBCommand create command."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class_name(self):
        corr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_create_nonexistent_class(self):
        corr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_create_unknown_syntax(self):
        corr = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(corr, output.getvalue().strip())
        corr = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_create_valid_classes(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            tK = "User.{}".format(output.getvalue().strip())
            self.assertIn(tK, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            tK = "State.{}".format(output.getvalue().strip())
            self.assertIn(tK, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(tK, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            tK = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(tK, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            tK = "Place.{}".format(output.getvalue().strip())
            self.assertIn(tK, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            tK = "Review.{}".format(output.getvalue().strip())
            self.assertIn(tK, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Test cases for HBNBCommand show command."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class_name(self):
        corr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_show_nonexistent_class(self):
        corr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_show_missing_instance_id(self):
        corr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_show_nonexistent_instance(self):
        corr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_show_valid_instances(self):
        corr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_show_nonexistent_instance_cmd_syntax(self):
        corr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_show_valid_instances_cmd_syntax(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["BaseModel.{}".format(testID)]
            com = "show BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["User.{}".format(testID)]
            com = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["State.{}".format(testID)]
            com = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["City.{}".format(testID)]
            com = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Amenity.{}".format(testID)]
            com = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Review.{}".format(testID)]
            com = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), output.getvalue().strip())

    def test_show_create_and_display_instances(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["BaseModel.{}".format(testID)]
            com = "BaseModel.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["User.{}".format(testID)]
            com = "User.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["State.{}".format(testID)]
            com = "State.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Place.{}".format(testID)]
            com = "Place.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["City.{}".format(testID)]
            com = "City.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Amenity.{}".format(testID)]
            com = "Amenity.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Review.{}".format(testID)]
            com = "Review.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertEqual(o.__str__(), outp.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Test cases for the destroy command in HBNBCommand."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def test_destroy_class_name_missing(self):
        corr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_destroy_class_doesnt_exist(self):
        corr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_destroy_instance_id_missing(self):
        corr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_destroy_no_instance_found(self):
        corr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_destroy_command(self):
        corr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_destroy_no_instance_found(self):
        corr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_create_and_show_destroy(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["BaseModel.{}".format(testID)]
            command = "destroy BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["User.{}".format(testID)]
            com = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["State.{}".format(testID)]
            com = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Place.{}".format(testID)]
            com = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["City.{}".format(testID)]
            com = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Amenity.{}".format(testID)]
            com = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Review.{}".format(testID)]
            com = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())

    def test_destroy_with_valid_instance_id(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["BaseModel.{}".format(testID)]
            com = "BaseModel.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["User.{}".format(testID)]
            com = "User.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["State.{}".format(testID)]
            com = "State.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Place.{}".format(testID)]
            com = "Place.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            ob = storage.all()["City.{}".format(testID)]
            com = "City.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Amenity.{}".format(testID)]
            com = "Amenity.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            o = storage.all()["Review.{}".format(testID)]
            com = "Review.destory({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(com))
            self.assertNotIn(o, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Test cases for HBNBCommand's 'all' command."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_command_class_not_exist(self):
        corr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_all_command_with_created_instances(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", outp.getvalue().strip())
            self.assertIn("User", outp.getvalue().strip())
            self.assertIn("State", outp.getvalue().strip())
            self.assertIn("Place", outp.getvalue().strip())
            self.assertIn("City", outp.getvalue().strip())
            self.assertIn("Amenity", outp.getvalue().strip())
            self.assertIn("Review", outp.getvalue().strip())

    def test_all_command_with_class_specified(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", outp.getvalue().strip())
            self.assertIn("User", outp.getvalue().strip())
            self.assertIn("State", outp.getvalue().strip())
            self.assertIn("Place", outp.getvalue().strip())
            self.assertIn("City", outp.getvalue().strip())
            self.assertIn("Amenity", outp.getvalue().strip())
            self.assertIn("Review", outp.getvalue().strip())

    def test_all_command_with_class_specified_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", outp.getvalue().strip())
            self.assertNotIn("User", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())

    def test_all_command_with_empty_storage(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", outp.getvalue().strip())
            self.assertNotIn("User", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", outp.getvalue().strip())
            self.assertNotIn("BaseModel", outp.getvalue().strip())


class TestUpdateCommand(unittest.TestCase):
    """Test cases for the update command."""

    @classmethod
    def setUpClass(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_class_name_missing(self):
        corr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_update_class_not_exist(self):
        corr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_update_instance_id_missing(self):
        corr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_upd_ins_id_mi_wi_c_n(self):
        corr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_update_no_instance_found(self):
        corr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(corr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(corr, output.getvalue().strip())

    def test_upd_no_ins_fo_wi_cl_n(self):
        corr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_up_attr_ne_mi(self):
        corr = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = outp.getvalue().strip()
            testCmd = "update BaseModel {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = outp.getvalue().strip()
            testCmd = "update User {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = outp.getvalue().strip()
            testCmd = "update State {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = outp.getvalue().strip()
            testCmd = "update City {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = outp.getvalue().strip()
            testCmd = "update Amenity {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = outp.getvalue().strip()
            testCmd = "update Place {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_update_attribute_name_missing(self):
        corr = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = outp.getvalue().strip()
            testCmd = "BaseModel.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = outp.getvalue().strip()
            testCmd = "User.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = outp.getvalue().strip()
            testCmd = "State.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = outp.getvalue().strip()
            testCmd = "City.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = outp.getvalue().strip()
            testCmd = "Amenity.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = outp.getvalue().strip()
            testCmd = "Place.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_update_value_missing(self):
        corr = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create BaseModel")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "update BaseModel {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create User")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "update User {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create State")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "update State {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create City")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "update City {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Amenity")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "update Amenity {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "update Place {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Review")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "update Review {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_up_va_mi(self):
        corr = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create BaseModel")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "BaseModel.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create User")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "User.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create State")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "State.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create City")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "City.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Amenity")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "Amenity.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "Place.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Review")
            testId = outp.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as outp:
            testCmd = "Review.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(corr, outp.getvalue().strip())

    def test_update_attribute_value(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create BaseModel")
            testId = outp.getvalue().strip()
        testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create User")
            testId = outp.getvalue().strip()
        testCmd = "update User {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create State")
            testId = outp.getvalue().strip()
        testCmd = "update State {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create City")
            testId = outp.getvalue().strip()
        testCmd = "update City {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "update Place {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Amenity")
            testId = outp.getvalue().strip()
        testCmd = "update Amenity {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Review")
            testId = outp.getvalue().strip()
        testCmd = "update Review {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Review.{}".format(testId)].__dict__
        self.assertTrue("attr_value", test_di["attr_name"])

    def test_update_attribute_value_comma(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create BaseModel")
            tId = outp.getvalue().strip()
        testCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create User")
            tId = outp.getvalue().strip()
        testCmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create State")
            tId = outp.getvalue().strip()
        testCmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create City")
            tId = outp.getvalue().strip()
        testCmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            tId = outp.getvalue().strip()
        testCmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Amenity")
            tId = outp.getvalue().strip()
        testCmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Review")
            tId = outp.getvalue().strip()
        testCmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

    def test_update_attribute_value_with_space(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "update Place {} max_guest 98".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_di["max_guest"])

    def test_update_float_value(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            tId = outp.getvalue().strip()
        testCmd = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, test_di["max_guest"])

    def test_update_float_value_comma(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "update Place {} latitude 7.2".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(7.2, test_di["latitude"])

    def test_update_dict_value(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            tId = outp.getvalue().strip()
        testCmd = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_di = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, test_di["latitude"])

    def test_update_dict_value_with_space(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create BaseModel")
            testId = outp.getvalue().strip()
        testCmd = "update BaseModel {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create User")
            testId = outp.getvalue().strip()
        testCmd = "update User {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create State")
            testId = outp.getvalue().strip()
        testCmd = "update State {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        testCmd = "update City {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Amenity")
            testId = outp.getvalue().strip()
        testCmd = "update Amenity {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Review")
            testId = outp.getvalue().strip()
        testCmd = "update Review {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

    def test_update_dict_value_without_comma(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create BaseModel")
            testId = outp.getvalue().strip()
        testCmd = "BaseModel.update({}".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create User")
            testId = outp.getvalue().strip()
        testCmd = "User.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create State")
            testId = outp.getvalue().strip()
        testCmd = "State.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create City")
            testId = outp.getvalue().strip()
        testCmd = "City.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Amenity")
            testId = outp.getvalue().strip()
        testCmd = "Amenity.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Review")
            testId = outp.getvalue().strip()
        testCmd = "Review.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_di["attr_name"])

    def test_update_max_guest_int_value(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_di["max_guest"])

    def test_update_max_guest_int_value_comma(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_di["max_guest"])

    def test_update_latitude_float_value(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_di["latitude"])

    def test_update_latitude_float_value_comma(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            HBNBCommand().onecmd("create Place")
            testId = outp.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_di = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_di["latitude"])


class TestCountCommand(unittest.TestCase):
    """Test cases for the count command"""

    @classmethod
    def setUpClass(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_no_objects(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", outp.getvalue().strip())

    def test_count_single_object_per_class(self):
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", outp.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as outp:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", outp.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
