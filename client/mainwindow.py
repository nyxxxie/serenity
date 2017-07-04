from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QDesktopWidget, QMainWindow, QDockWidget, QTextEdit, qApp
from client.editorwidget import EditorWidget
from client.consolewidget import ConsoleWidget

# https://github.com/baoboa/pyqt5/blob/master/examples/mainwindows/dockwidgets/dockwidgets.py
# http://zetcode.com/gui/pyqt5/firstprograms/

class SpadeMainWindow(QMainWindow):
    """Spade's main window."""

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._create_central_widget()
        self._create_projectview()
        self._create_templateview()
        self._create_consolewidget()

    def center(self):
        """Place the window in the center of the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _init_menubar(self):
        """Set up the menu bar."""
        action_exit = QAction("Exit", self)
        action_exit.setStatusTip("Exit application")
        action_exit.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menu_file = menubar.addMenu("File")
        menu_file.addAction(action_exit)

    def _init_ui(self):
        """Set up main window attributes."""
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle("Spade")
        self._init_menubar()
        self.statusBar().showMessage("Ready")

    def _create_central_widget(self):
        """Set up the central widget."""
        self.central_widget = EditorWidget()
        self.setCentralWidget(self.central_widget)

    def _create_projectview(self):
        """Spawn projectview."""
        self.dock_projectview = QDockWidget()
        self.dock_projectview.setAllowedAreas(Qt.LeftDockWidgetArea
                | Qt.RightDockWidgetArea)
        self.dock_projectview.setWidget(QTextEdit())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_projectview)

    def _create_templateview(self):
        """Spawn templateview."""
        self.dock_templateview = QDockWidget()
        self.dock_templateview.setAllowedAreas(Qt.LeftDockWidgetArea
                | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.dock_templateview.setWidget(QTextEdit())
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_templateview)

    def _create_consolewidget(self):
        """Spawn consoleview."""
        self.dock_templateview = QDockWidget()
        self.dock_templateview.setAllowedAreas(Qt.BottomDockWidgetArea)
        console = ConsoleWidget()
        self.dock_templateview.setWidget(console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_templateview)
