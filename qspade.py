#!/usr/bin/env python
import sys
import traceback
from PyQt5.QtWidgets import QApplication
from qspade.mainwindow import SpadeMainWindow

def rungui(args):
    try:
        app = QApplication(args)
        w = SpadeMainWindow()
        w.show()
        return app.exec_()
    except Exception as e:
        print("Exception!")
        print(e)
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(rungui(sys.argv))
