import logging

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from spade import template

HEADERS = ("Name", "Type", "Offset", "Hex", "Value")


class TreeItem(object):
    """Wrapper class that fits a spade TNode into the tree.

    This is necessary so that we can implement some of the required methods
    for the QAbstractItemModel container these items will be displayed in.
    """

    def __init__(self, node):
        self.node = node
        self.row = 0
        self.column = 0

    @property
    def fields(self):
        return self.node.fields


class TreeModel(QtCore.QAbstractItemModel):
    """Displays TreeItems containing TNodes."""

    def __init__(self, root_node):
        super().__init__()
        self.root_node = root_node

    def getParent(self, parent):
        if not parent.isValid():
            return self.root_node
        else:
            return parent.internalPointer()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        parent_node = self.getParent(parent)
        if not parent_node:
            logging.error("Bad parent node.")
            return QtCore.QModelIndex()

        child_node = parent_node.fields[row]
        if not child_node:
            logging.error("Bad child node.")
            return QtCore.QModelIndex()

        return self.createIndex(row, column, child_node)

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_node = index.internalPointer()
        if not child_node:
            logging.error("Bad child node.")

        parent_node = child_node.parent
        if not parent_node:
            logging.error("Bad parent node.")
            return QtCore.QModelIndex()

        if parent_node is self.root_node:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.index, 0, parent_node)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        parent_node = self.getParent(parent)
        if not parent_node:
            logging.error("Bad parent node.")
            return QtCore.QModelIndex()

        if isinstance(parent_node, template.TVar):
            return 0
        elif isinstance(parent_node, template.TStruct):
            return len(parent_node.fields)

        return 0

    def columnCount(self, parent):
        return len(HEADERS)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if role != Qt.DisplayRole:
            return QtCore.QVariant()

        node = index.internalPointer()
        if not node:
            logging.error("Bad node.")
            return QtCore.QVariant()

        if isinstance(node, template.TVar):
            if index.column() == 0:
                return node.name
            elif index.column() == 1:
                return node.type_name
            elif index.column() == 2:
                return node.offset
            elif index.column() == 3:
                return str(node.data.bytes())
            elif index.column() == 4:
                return node.data.string()
        elif isinstance(node, template.TStruct):
            if index.column() == 0:
                return node.name
            elif index.column() == 1:
                return node.type_name
            elif index.column() == 2:
                return node.offset

        return QtCore.QVariant()

    def flags(self, index):
        if not index.isValid():
            return 0

        return super().flags(index)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return HEADERS[section]

        return QtCore.QVariant()

class TemplateWidget(QtWidgets.QTreeView):

    def __init__(self, template_root=None):
        super().__init__()

        print("AND THE HELL BEGINS")

        # DELETE THE BELOW WHEN TESTING IS DONE
        template_root = template.from_file(
                "tests/template/testdata/multistruct1.stf",
                "tests/template/testdata/multistruct1_target")
        if not template_root:
            print("Bad root!")
        # DELETE THE ABOVE WHEN TESTING IS DONE

        if template_root:
            self.setTemplateRoot(template_root)

    def setTemplateRoot(self, template_root):
        model = TreeModel(template_root)
        self.setModel(model)
