#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import QApplication
from ui.mainwindow import SpadeMainWindow

def rungui(args):
    app = QApplication(args)

    w = SpadeMainWindow()
    w.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    rungui(sys.argv)
