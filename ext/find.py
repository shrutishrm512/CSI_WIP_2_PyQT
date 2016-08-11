#!/usr/bin/python

import re
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Search(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.lastMatch = None
        self.initUI()

    def initUI(self):
        # label for search text field
        self.searchtxt = QLabel("Search for :", self)
        self.searchtxt.setStyleSheet("font-size: 15px")
        self.searchtxt.move(10, 10)

        # Button to search the text
        searchButton = QPushButton("search", self)
        searchButton.move(270, 40)
        searchButton.clicked.connect(self.search)

        # Field area to write text which is to be searched
        self.searchField = QTextEdit(self)
        self.searchField.move(10, 40)
        self.searchField.resize(250, 25)

        optionLabel = QLabel("Options", self)
        optionLabel.move(10, 70)

        # Case Sensitivity option
        self.caseSens = QCheckBox("Case sensitive", self)
        self.caseSens.move(10, 90)

        # Whole Words only option
        self.wholeWords = QCheckBox("Whole words only", self)
        self.wholeWords.move(10, 110)
        # Close option
        self.close = QPushButton("Close", self)
        self.close.move(270, 130)
        self.close.clicked.connect(self.Close)

        self.setGeometry(300, 300, 360, 160)
        self.setWindowTitle("Find")

    def search(self):
        text = self.parent.textArea.toPlainText()
        # And the text to search
        query = self.searchField.toPlainText()
        if self.wholeWords.isChecked():
            query = r'\W' + query + r'\W'
        # By default regexes are case sensitive, switch this around here
        flags = 0 if self.caseSens.isChecked() else re.I
        # Compile the pattern
        pattern = re.compile(str(query), flags)
        start = self.lastMatch.start() + 1 if self.lastMatch else 0
        # The actual search
        self.lastMatch = pattern.search(text, start)
        if self.lastMatch:
            start = self.lastMatch.start()
            end = self.lastMatch.end()

            if self.wholeWords.isChecked():
                start += 1
                end -= 1
            self.moveCursor(start, end)

        else:
            # setting cursor to the end if the search was unsuccessful
            self.parent.textArea.moveCursor(QTextCursor.End)

    def moveCursor(self, start, end):
        cursor = self.parent.textArea.textCursor()
        cursor.setPosition(start)
        # Move the Cursor over the match and pass the KeepAnchor parameter
        # which will make the cursor select the the match's text
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                            end - start)
        self.parent.textArea.setTextCursor(cursor)

    def Close(self):
        self.hide()
