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

import copy
import logging

TEMPLATE_ENTRY = "FILE"


class TNode(object):
    """Base class of any node in a template tree structure."""

    def __init__(self, name, type_name, root=None, parent=None, index=0):
        self.name = name
        self.type_name = type_name
        self.parent = parent
        self.root = root
        self.index = index
        self.offset = 0
        self.size = 0

        if not parent:
            self.location = name
        else:
            self.location = parent.location + "." + name

    def _refresh(self, target_file, offset):
        raise NotImplementedError("Not implemented.")

class TVar(TNode):
    """."""

    def __init__(self, name, type_name, root, parent, index, type_cls):
        super().__init__(name, type_name, root, parent, index)
        self.type_cls = type_cls
        self.size = self.type_cls.size
        self.data = None

    def _refresh(self, target_file, offset):
        logging.debug("Reading {} bytes of type data at offset {}".format(offset,
                self.size))
        self.offset = offset
        target_file.seek(offset)
        # TODO: check if offset goes past file bounds
        # TODO: check if read goes past file bounds
        self.data = self.type_cls(target_file.read(self.size))
        # TODO: create property for data member, so we can r/w direct to file (if
        # cache is disabled).  This might mean we store the target_file somehow
        # (maybe keep a global reference in root) so that we can access it from
        # the property thing in the background.  A single reference also allows
        # easy changing of the target file.


class TArray(TVar):
    """."""

    def __init__(self, template_var, length):
        super().__init__(name, type_name, root, parent, index)
        self.items = []

        for i in range(length):
            items.append(copy.deepcopy(template_var))

    def __len__(self):
        return self.length

    # TODO: figure out how to implement index operator

    @property
    def length(self):
        len(self.items)

    def get_index(self, index):
        pass

    def _refresh(self, target_file, offset):
        for i in range(self.length):
            items._refresh(target_file, offset + (i * self.size))


class TStruct(TNode):
    """An ordered container for template nodes."""

    def __init__(self, name, type_name, root, parent, index):
        super().__init__(name, type_name, root, parent, index)
        self.fields = []
        self.offset = 0

    def _refresh(self, target_file, offset=0):
        self.offset = offset
        self.size = 0
        for node in self.fields:
            node._refresh(target_file, offset + self.size)
            self.size += node.size

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
        super().__init__(name, TEMPLATE_ENTRY, self, None, 0)

    def refresh(self, target_file):
        self._refresh(target_file, 0)
