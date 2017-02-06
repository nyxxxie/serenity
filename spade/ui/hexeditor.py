import os
from math import log
from PyQt5.QtWidgets import QWidget, QAbstractScrollArea
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QFont, QFontMetrics, QColor, QPen

COLUMN_GAP=6
TEXT_OFFSET=4
ROW_OFFSET=0
BYTE_GAP=4
BYTES_PER_ROW=16

def get_file_size(f):
    old_pos = f.tell()
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(old_pos, os.SEEK_SET)
    return size

class HexEditorColumn:
    def __init__(self, hexeditor):
        self.hexeditor = hexeditor
        self.width = 0

    def cursor(self):
        return self.hexeditor.cursor

    def rows(self):
        return self.hexeditor.rows_total

    def rows_visible(self):
        return self.hexeditor.rows_shown

    def row_start(self):
        return self.hexeditor.cursor

    def viewport(self):
        return self.hexeditor.viewport()

    def font_width(self):
        return self.hexeditor.font_width

    def font_height(self):
        return self.hexeditor.font_height

    def file(self):
        return self.hexeditor.file

    def file_size(self):
        return get_file_size(self.hexeditor.file)

class AddressColumn(HexEditorColumn):
    def __init__(self, hexeditor):
        super().__init__(hexeditor)

    def render(self, start, paint):
        # If this isn't the first column rendered, space ourselves out from the
        # previous column
        if (start != 0):
            start += COLUMN_GAP

        # Calc width of the address bar
        n = self.file_size()
        byte_num = int(log(n, 0xff)) + 1 if n != 0 else 1
        if byte_num < 4:
            byte_num = 4 # byte num should at least be 4
        width = ((byte_num+1)*self.font_width()) + (2*TEXT_OFFSET)

        # Draw bar
        paint.fillRect(
            QRect(start, 0, width, self.viewport().height()),
            QColor(255, 0, 0))

        # Draw addresses
        start += TEXT_OFFSET
        for row in range(1, self.rows_visible()):
            addr = (row + self.row_start() - 1) * BYTES_PER_ROW
            paint.drawText(start,
                row*(ROW_OFFSET + self.font_height()*2),
                ("%x" % addr).zfill(byte_num) + "h")

        # Let caller know how much space we took up while drawing
        return start + width

class HexColumn(HexEditorColumn):
    def __init__(self, hexeditor):
        super().__init__(hexeditor)

    def render(self, start, paint):
        # If this isn't the first column rendered, space ourselves out from the
        # previous column
        if (start != 0):
            start += COLUMN_GAP

        # Calc width of the address bar
        width = BYTES_PER_ROW * (2*self.font_width())
        width += (BYTES_PER_ROW-1) * BYTE_GAP
        width += (2 * TEXT_OFFSET)

        # Draw bar
        paint.fillRect(
            QRect(start, 0, width, self.viewport().height()),
            QColor(0, 255, 0))

        # Draw hex
        start += TEXT_OFFSET
        old_pos = self.file().tell()
        self.file().seek(self.row_start() * BYTES_PER_ROW, os.SEEK_SET)

        for row in range(1, self.rows_visible()):
            data = self.file().read(BYTES_PER_ROW)
            for i, byte in enumerate(data):
                paint.drawText(start+i*(BYTE_GAP+self.font_width()*2),
                    row*(ROW_OFFSET + self.font_height()*2),
                    "%02x " % byte)

        self.file().seek(old_pos, os.SEEK_SET)

        # Let caller know how much space we took up while drawing
        return start + width

class AsciiColumn(HexEditorColumn):
    def __init__(self, hexeditor):
        super().__init__(hexeditor)

    def render(self, start, paint):
        # If this isn't the first column rendered, space ourselves out from the
        # previous column
        if (start != 0):
            start += COLUMN_GAP

        # Calc width of the address bar
        width = BYTES_PER_ROW * self.font_width()
        width += (2 * TEXT_OFFSET)

        # Draw bar
        paint.fillRect(
            QRect(start, 0, width, self.viewport().height()),
            QColor(0, 0, 255))

        # Draw hex
        start += TEXT_OFFSET
        old_pos = self.file().tell()
        self.file().seek(self.row_start() * BYTES_PER_ROW, os.SEEK_SET)

        for row in range(1, self.rows_visible()):
            data = self.file().read(BYTES_PER_ROW)
            for i, byte in enumerate(data):
                paint.drawText(start + (i*self.font_width()),
                    row*(ROW_OFFSET + self.font_height()*2),
                    "%c" % byte)

        self.file().seek(old_pos, os.SEEK_SET)

        # Let caller know how much space we took up while drawing
        return start + width

class HexEditor(QAbstractScrollArea):
    def _adjust(self):
        """
        Recalculates scrollbar variables when window size/contents are changed.
        """
        # We don't need to set any of this if file is bad
        if self.file is None:
            return

        self.rows_total = int(get_file_size(self.file) / BYTES_PER_ROW)
        self.rows_shown = int((self.viewport().height() / (self.font_height+ROW_OFFSET))) + 1
        self.widgets_width = 1000

        self.horizontalScrollBar().setRange(0, self.widgets_width - self.viewport().width());
        self.horizontalScrollBar().setPageStep(self.viewport().width());
        self.verticalScrollBar().setRange(0, self.rows_total)
        self.verticalScrollBar().setPageStep(self.rows_shown)

    def setFont(self, font):
        """
        Sets font and updates related variables and the viewport.
        """
        # Set font
        super().setFont(font)

        # Calculate font width and height
        fm = QFontMetrics(font)
        self.font_width = fm.width(" ")
        self.font_height = int(fm.height()/2) - 1

        # Recalc vars since font has changed
        self._adjust()
        self.viewport().update()

    def setFile(self, f):
        self.file = f
        self._adjust()
        self.viewport().update()

    def drawNoFile(self, paint):
        paint.drawText(self.geometry(), Qt.AlignCenter, "No file, add one!")

    def drawFile(self, paint):
        start = 0
        for widget in self.widgets:
            start = widget.render(start, paint)

    def paintEvent(self, e):
        """
        Called by qt when window wants to paint itself.
        """
        paint = QPainter(self.viewport())

        if self.file is None:
            self.drawNoFile(paint)
        else:
            self.drawFile(paint)

    def __init__(self):
        super().__init__()

        self.file = None
        self.cursor = 0
        self.rows_total = 0
        self.rows_shown = 0
        self.widgets_width = 0
        self.font_width = 0
        self.font_height = 0

        # Columns in the hex editor that will be displayed by default
        self.widgets = [
            AddressColumn(self),
            HexColumn(self),
            AsciiColumn(self)
        ]

        self.verticalScrollBar().setValue(0);
        self.horizontalScrollBar().setValue(0);

        self.setFont(QFont("Monospace", 7, QFont.Light))
        #self.setFile(open("testfile", "rb"))
