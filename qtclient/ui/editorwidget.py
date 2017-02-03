from PyQt5.QtWidgets import QTabWidget
from .hexeditor import HexEditor

class EditorWidget(QTabWidget):
    def _add_hexeditor(self):
        hexedit = HexEditor()
        self.addTab(hexedit, "Hex Editor")

    def __init__(self):
        super().__init__()
        self._add_hexeditor()

