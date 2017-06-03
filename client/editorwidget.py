from PyQt5.QtWidgets import QTabWidget
from client.hexeditor import HexEditor

class EditorWidget(QTabWidget):
    """Container widget for editors."""

    def __init__(self):
        super().__init__()
        self._add_hexeditor()

    def _add_hexeditor(self):
        hexedit = HexEditor()
        self.addTab(hexedit, "Hex Editor")
