#!/usr/bin/python3
"""Console module for managing instances of various classes."""
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
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class defines a command-line interface"""

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

    def empl(self):
        """Placeholder method."""
        pass

    def default(self, arg):
        """Placeholder method."""
        a = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        m = re.search(r"\.", arg)
        if m is not None:
            aa = [arg[:m.span()[0]], arg[m.span()[1]:]]
            m = re.search(r"\((.*?)\)", aa[1])
            if m is not None:
                com = [aa[1][:m.span()[0]], m.group()[1:-1]]
                if com[0] in a.keys():
                    call = "{} {}".format(aa[0], com[1])
                    return a[com[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit the command-line interface."""
        return True

    def do_EOF(self, arg):
        """Handle end-of-file condition."""
        print("")
        return True

    def do_create(self, arg):
        """
        Create a new instance based on the provided class name.

        Args:
            arg (str): The input string containing the class name.

        Returns:
            None
        """
        aa = parse(arg)
        if len(aa) == 0:
            print("** class name missing **")
        elif aa[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(aa[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        aa = parse(arg)
        objdict = storage.all()
        if len(aa) == 0:
            print("** class name missing **")
        elif aa[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(aa) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(aa[0], aa[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(aa[0], aa[1])])

    def do_destroy(self, arg):
        """Show information about a specific instance."""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """
        Display information about instances.

        Args:
            arg (str): The input string containing the class name.

        Returns:
            None
        """
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """
        Count and print the number of instances.

        Args:
            arg (str): The input string containing the class name.

        Returns:
            None
        """
        argl = parse(arg)
        c = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                c += 1
        print(c)

    def do_update(self, arg):
        """
        Update attributes of a specific instance.

        Args:
            arg (str): The input string containing the class name, instance ID,
                       attribute name, and value.

        Returns:
            None
        """
        aa = parse(arg)
        b = storage.all()

        if len(aa) == 0:
            print("** class name missing **")
            return False
        if aa[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(aa) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(aa[0], aa[1]) not in b.keys():
            print("** no instance found **")
            return False
        if len(aa) == 2:
            print("** attribute name missing **")
            return False
        if len(aa) == 3:
            try:
                type(eval(aa[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(aa) == 4:
            obj = b["{}.{}".format(aa[0], aa[1])]
            if aa[2] in obj.__class__.__dict__.keys():
                vt = type(obj.__class__.__dict__[aa[2]])
                obj.__dict__[aa[2]] = vt(aa[3])
            else:
                obj.__dict__[aa[2]] = aa[3]
        elif type(eval(aa[2])) == dict:
            obj = b["{}.{}".format(aa[0], aa[1])]
            for k, value in eval(aa[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    vt = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = vt(value)
                else:
                    obj.__dict__[k] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
