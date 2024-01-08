#!/usr/bin/python3
"""Defines the HBnB conso."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    x = re.search(r"\{(.*?)\}", arg)
    b = re.search(r"\[(.*?)\]", arg)
    if x is None:
        if b is None:
            return [i.strip(",") for i in split(arg)]
        else:
            li = split(arg[:b.span()[0]])
            y = [i.strip(",") for i in li]
            y.append(b.group())
            return y
    else:
        li = split(arg[:x.span()[0]])
        y = [i.strip(",") for i in li]
        y.append(x.group())
        return y


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def empt(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        ar = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        m = re.search(r"\.", arg)
        if m is not None:
            h = [arg[:m.span()[0]], arg[m.span()[1]:]]
            m = re.search(r"\((.*?)\)", h[1])
            if m is not None:
                cm = [h[1][:m.span()[0]], m.group()[1:-1]]
                if cm[0] in ar.keys():
                    call = "{} {}".format(h[0], cm[1])
                    return ar[cm[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        h = parse(arg)
        if len(h) == 0:
            print("** class name missing **")
        elif h[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(h[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        h = parse(arg)
        ob = storage.all()
        if len(h) == 0:
            print("** class name missing **")
        elif h[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(h) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(h[0], h[1]) not in ob:
            print("** no instance found **")
        else:
            print(ob["{}.{}".format(h[0], h[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        h = parse(arg)
        ob = storage.all()
        if len(h) == 0:
            print("** class name missing **")
        elif h[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(h) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(h[0], h[1]) not in ob.keys():
            print("** no instance found **")
        else:
            del ob["{}.{}".format(h[0], h[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        h = parse(arg)
        if len(h) > 0 and h[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            ob1 = []
            for ob in storage.all().values():
                if len(h) > 0 and h[0] == ob.__class__.__name__:
                    ob1.append(ob.__str__())
                elif len(h) == 0:
                    ob1.append(ob.__str__())
            print(ob1)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        h = parse(arg)
        c = 0
        for ob in storage.all().values():
            if h[0] == ob.__class__.__name__:
                c += 1
        print(c)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        h = parse(arg)
        x = storage.all()

        if len(h) == 0:
            print("** class name missing **")
            return False
        if h[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(h) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(h[0], h[1]) not in x.keys():
            print("** no instance found **")
            return False
        if len(h) == 2:
            print("** attribute name missing **")
            return False
        if len(h) == 3:
            try:
                type(eval(h[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(h) == 4:
            ob = x["{}.{}".format(h[0], h[1])]
            if h[2] in ob.__class__.__dict__.keys():
                vp = type(ob.__class__.__dict__[h[2]])
                ob.__dict__[h[2]] = vp(h[3])
            else:
                ob.__dict__[h[2]] = h[3]
        elif type(eval(h[2])) == dict:
            ob = x["{}.{}".format(h[0], h[1])]
            for n, b in eval(h[2]).items():
                if (n in ob.__class__.__dict__.keys() and
                        type(ob.__class__.__dict__[n]) in {str, int, float}):
                    vp = type(ob.__class__.__dict__[n])
                    ob.__dict__[n] = vp(b)
                else:
                    ob.__dict__[n] = b
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
