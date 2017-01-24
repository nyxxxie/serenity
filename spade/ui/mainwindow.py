from .editorwidget import SpadeEditorWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QDockWidget, QTextEdit

# https://github.com/baoboa/pyqt5/blob/master/examples/mainwindows/dockwidgets/dockwidgets.py
# http://zetcode.com/gui/pyqt5/firstprograms/

class SpadeMainWindow(QMainWindow):
    def _init_ui(self):
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle("Spade")

    def _create_central_widget(self):
        self.central_widget = SpadeEditorWidget()
        self.setCentralWidget(self.central_widget)

    def _create_projectview(self):
        self.dock_projectview = QDockWidget();
        self.dock_projectview.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dock_projectview.setWidget(QTextEdit())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_projectview)

    def _create_templateview(self):
        self.dock_templateview = QDockWidget();
        self.dock_templateview.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.dock_templateview.setWidget(QTextEdit())
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_templateview)

    def _create_docks(self):
        self._create_projectview()
        self._create_templateview()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._create_central_widget()
        self._create_docks()


