import re

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QApplication, QTextEdit, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor, QTextFormat, QPainter, QTextCharFormat, QSyntaxHighlighter, QFont
from PyQt5.QtCore import QRect, pyqtSlot, Qt, QSize, QRegExp, QRegularExpression
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        self.highlighting_rules = []

        # Define highlighting rule with words with red color
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(reg|logic|wire|integer|real|initial)($|\s+)")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for input and output
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(input|output|parameter|import|`include|`timescale|localparam)($|\s+)")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for modules
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(module|endmodule)($|\s+)")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for always
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(always)\s*@")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for assign
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+|\t+)(assign)\s+")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for if
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(if|for)")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for else
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(else)($|\s+|\()")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for case
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("red"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(case|endcase)($|\s+)")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with red color for posedge
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("blue"))
        module_pattern = QRegExp("(?!//.+)(posedge|negedge)($|\s+)")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with blue color
        module_format = QTextCharFormat()
        module_format.setForeground(QColor("blue"))
        module_pattern = QRegExp("(?!//.+)(^|\s+)(case|endcase|begin|end)($|\s+)")
        self.highlighting_rules.append((module_pattern, module_format))

        # Define highlighting rule with words with dim color for comments
        module_format = QTextCharFormat()
        module_format.setForeground(QColor(80, 120, 200))
        module_pattern = QRegExp("(//.+)")
        module_format.setFontItalic(True)
        self.highlighting_rules.append((module_pattern, module_format))

        # for long comments
        module_format = QTextCharFormat()
        module_format.setForeground(QColor(80, 120, 200))
        module_pattern = QRegExp("(/\*.*|.*\*/)")
        module_format.setFontItalic(True)
        self.highlighting_rules.append((module_pattern, module_format))
        self.commentStartExpression = re.compile("/\*")
        self.commentEndExpression = re.compile("\*/")
        self.commentFormat = QTextCharFormat()
        self.commentFormat.setForeground(QColor(80, 120, 200))
        self.commentFormat.setFontItalic(True)
        self.state = None

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        if self.state is None:
            match = self.commentStartExpression.match(text)
            if match:
                self.state = 1
                self.setFormat(match.start(), match.end(), self.commentFormat)
                text = text[match.end():]

        if self.state == 1:
            match = self.commentEndExpression.search(text)
            if match:
                self.setFormat(match.start(), match.end(), self.commentFormat)
                self.state = None
            else:
                self.setFormat(0, len(text), self.commentFormat)


class BlockCommentHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.commentStartExpression = re.compile("/\*.*")
        self.commentEndExpression = re.compile("\*/")
        self.commentFormat = QTextCharFormat()
        self.commentFormat.setForeground(Qt.darkGreen)
        self.commentFormat.setFontItalic(True)
        self.state = None

    def highlightBlock(self, text):
        if self.state is None:
            match = self.commentStartExpression.match(text)
            if match:
                self.state = 1
                self.setFormat(match.start(), match.end(), self.commentFormat)
                text = text[match.end():]

        if self.state == 1:
            match = self.commentEndExpression.search(text)
            if match:
                self.setFormat(match.start(), match.end(), self.commentFormat)
                self.state = None
            else:
                self.setFormat(0, len(text), self.commentFormat)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, parent=editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        # self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        # self.highlightCurrentLine()
        self.setToolTipDuration(0)
        self.setMouseTracking(True)
        self.line_written = None
        self.cursorPositionChanged.connect(self.show_tool_tip)

    def show_tool_tip(self):
        cursor = self.textCursor()
        line_number = cursor.blockNumber() + 1
        if self.line_written:
            if line_number in self.line_written:
                tooltip_text = self.line_written[line_number]
                QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), tooltip_text, self)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.show_tool_tip()

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.setFont(QFont('Consolas', 12))  # set font size here
                painter.drawText(0, int(top), self.lineNumberArea.width(),
                                 self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    @pyqtSlot(int)
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    # @pyqtSlot()
    # def highlightCurrentLine(self):
    #     extraSelections = []
    #     if not self.isReadOnly():
    #         selection = QTextEdit.ExtraSelection()
    #         lineColor = QColor(Qt.blue).lighter(190)
    #         selection.format.setBackground(lineColor)
    #         selection.format.setProperty(QTextFormat.FullWidthSelection, True)
    #         selection.cursor = self.textCursor()
    #         selection.cursor.clearSelection()
    #         extraSelections.append(selection)
    #     self.setExtraSelections(extraSelections)

    # @pyqtSlot()
    # def change_words_color(self):
    #     redFormat = '<span style="color:red;">{}</span>'
    #     Special_word = re.search("()")

    @pyqtSlot(QRect, int)
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)


class WaveViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure(figsize=(10, 1)))
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111, position=[0.2, 0, 1, 1])
        self.setLayout(vertical_layout)
        self.canvas.axes.get_yaxis().set_visible(False)
        self.canvas.axes.get_xaxis().set_visible(False)
        self.canvas.axes.clear()
        self.canvas.axes.spines['top'].set_visible(False)
        self.canvas.axes.spines['right'].set_visible(False)
        self.canvas.axes.spines['left'].set_visible(False)
        self.canvas.axes.spines['bottom'].set_visible(False)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = CodeEditor()
    w.show()
    sys.exit(app.exec_())
