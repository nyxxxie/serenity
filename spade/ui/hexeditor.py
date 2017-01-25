from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QFont, QColor, QPen

class HexEditor(QWidget):
    def paintEvent(self, e):
        paint = QPainter()
        paint.begin(self)
        paint.setPen(QColor(255, 255, 255))
        paint.setBrush(QColor(0, 255, 0))
        paint.drawRect(0, 0, 50, 50)
        paint.end()

    def __init__(self):
        super().__init__()
