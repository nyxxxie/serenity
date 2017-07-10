from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from spade import template

HEADERS = ("Name", "Type", "Hex", "Value")

class TreeItem(object):
    """Wrapper class that fits a spade TNode into the tree.

    This is necessary so that we can implement some of the required methods
    for the QAbstractItemModel container these items will be displayed in.
    """

    def __init__(self, node):
        pass

# (venv) endor:src/spade :: ./qspade
# Exception!
# 'NoneType' object has no attribute 'from_file'
# Traceback (most recent call last):
#   File "./qspade", line 10, in rungui
#     w = SpadeMainWindow()
#   File "/home/nyx/src/spade/client/mainwindow.py", line 18, in __init__
#     self._create_templateview()
#   File "/home/nyx/src/spade/client/mainwindow.py", line 64, in _create_templateview
#     self.dock_templateview.setWidget(TemplateWidget())
#   File "/home/nyx/src/spade/client/templatewidget.py", line 58, in __init__
#     template = template.from_file("template.stf", "target.bin")
# AttributeError: 'NoneType' object has no attribute 'from_file'

class TreeModel(QtCore.QAbstractItemModel):
    """Displays TreeItems containing TNodes."""

    def __init__(self, root_node):
        super().__init__()
        self.root_node = root_node

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.root_node)
        parent_node = parent.internalPointer()
        return self.createIndex(row, column, parent_node)

    def parent(self, index):
        if not index.isValid():
            return Qt.QModelIndex()
        node = index.internalPointer()
        if not node.parent:
            return Qt.QModelIndex()
        else:
            return self.createIndex(node.parent_node, 0, node.parent)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return "adsf"

    def rowCount(self, parent):
        if not parent.isValid():
            return 1
        node = parent.internalPointer()
        return len(node.subnodes)

class TemplateWidget(QtWidgets.QTreeView):

    def __init__(self, template_root=None):
        super().__init__()

        # DELETE THE BELOW WHEN TESTING IS DONE
        template_root = template.from_file(
                "tests/template/testdata/multistruct.stf",
                "tests/template/testdata/multistruct_target")
        if not template_root:
            print("Bad root!")
        # DELETE THE ABOVE WHEN TESTING IS DONE

        if template_root:
            self.setTemplateRoot(template_root)

    def setTemplateRoot(self, template_root):
        model = TreeModel(template_root)
        self.setModel(model)
