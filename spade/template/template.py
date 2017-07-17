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

class TNode(object):
    """Base class of any node in a template tree structure."""

    def __init__(self, name, root=None, parent=None):
        self.name = name
        self.parent = parent
        self.root = root


class TVar(TNode):
    """."""

    def __init__(self, name, root, parent, type_cls):
        super().__init__(name, root, parent)


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


class TRoot(TStruct):
    """Base of a spade template."""

    def __init__(self, name):
        super().__init__(name, self, None)
