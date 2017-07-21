"""Contains definitions for the various components of a workable spade template.

Templates
*********
A "workable" template is one that is able to be used directly inside python
programs.  These templates may either be constructed node by node either inside
a python program or be generated from a template file.

Templates From Template Files
=============================
Most users will probably
want to make use of templates using the latter option, in which case they should
direct their attention to the various helper methods in the __init__.py file in
this directory.

Creating Templates From Scratch
===============================
A template should start with a TemplateRoot and may be built up from
there.

Template Root
-------------
blah

Template Structs
----------------
blah

Struct Fields
-------------
blah

Array Fields
------------
blah
"""

import logging

TEMPLATE_ENTRY = "FILE"


class TNode(object):
    """Base class of any node in a template tree structure."""

    def __init__(self, name, root=None, parent=None):
        self.name = name
        self.parent = parent
        self.root = root

        if not parent:
            self.location = name
        else:
            self.location = parent.location + "." + name


class TVar(TNode):
    """."""

    def __init__(self, name, root, parent, type_cls):
        super().__init__(name, root, parent)
        self.type_cls = type_cls


class TArray(TNode):
    """."""

    def __init__(self, name, root, parent):
        super().__init__(name, root, parent)


class TStruct(TNode):
    """An ordered container for template nodes."""

    def __init__(self, name, root, parent):
        super().__init__(name, root, parent)
        self.fields = []

    def refresh():
        pass

    def add_field(self, field):
        self.fields.append(field)

    def find_node(self, location):
        """Locates a node in scope of thise struct"""

        split = location.split(".", 1)

        # Are we currently dealing with our entry point?
        if split[0] == TEMPLATE_ENTRY:
            # Have we reached the end of the path?
            if len(split) == 1:
                return self.root
            # If we havent, continue on up the path
            if self.root is self:
                return self.root.find_node(split[1])
            # If this has also failed, we've encountered a problem
            else:
                logging.error("Failed to process location {} relative "
                        "to {}".format(location, self.location))
                return None

        # Find the field that cooresponds to the current location
        for node in self.fields:
            if node.name == split[0]:
                break
        else:
            logging.debug("Failed to find node {} at {}".format(split[0],
                    location))
            return None

        # Using this field, determine its type and handle it accordingly
        if isinstance(node, TStruct):
            # Have we reached the end?
            if len(split) == 1:
                return node
            # If not, continue searching
            else:
                return node.find_node(split[1])
        elif isinstance(node, TVar):
            # Have we reached the end?
            if len(split) == 1:
                return node
            # If not, we should have since TVars are terminals!
            else:
                logging.error("Encountered non terminal node {} at {}".format(
                        split[0], location))
                return None
        else:
            logging.error("Unexpected node at location {} [{}]".format(
                    location, type(node)))
            return None


class TRoot(TStruct):
    """Base of a spade template."""

    def __init__(self, name):
        super().__init__(name, self, None)
