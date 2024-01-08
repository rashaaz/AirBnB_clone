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
