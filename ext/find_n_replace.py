#!/usr/bin/python

import re
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class FindandReplace(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.lastMatch = None
        self.initUI()

    def initUI(self):
        findButton = QPushButton("Find", self)
        findButton.clicked.connect(self.find)

        replaceButton = QPushButton("Replace", self)
        replaceButton.clicked.connect(self.replace)

        allButton = QPushButton("Replace all", self)
        allButton.clicked.connect(self.replaceAll)

        # Normal mode - radio button
        self.normalRadio = QRadioButton("Normal", self)
        self.normalRadio.toggled.connect(self.normalMode)

        # Regular Expression Mode - radio button
        self.regexRadio = QRadioButton("RegEx", self)
        self.regexRadio.toggled.connect(self.regexMode)

        # Field to write query
        self.findField = QTextEdit(self)
        self.findField.resize(250, 10)

        # Field to write text to replace query
        self.replaceField = QTextEdit(self)
        self.replaceField.resize(250, 10)

        optionsLabel = QLabel("Options: ", self)

        # Case Sensitivity option
        self.caseSens = QCheckBox("Case sensitive", self)

        # Whole Words option
        self.wholeWords = QCheckBox("Whole words", self)

        # Layout the objects on the screen
        layout = QGridLayout()

        layout.addWidget(self.findField, 1, 0, 1, 4)
        layout.addWidget(self.normalRadio, 2, 2)
        layout.addWidget(self.regexRadio, 2, 3)
        layout.addWidget(findButton, 2, 0, 1, 2)
        layout.addWidget(self.replaceField, 3, 0, 1, 4)
        layout.addWidget(replaceButton, 4, 0, 1, 2)
        layout.addWidget(allButton, 4, 2, 1, 2)

        # Add some spacing
        spacer = QWidget(self)
        spacer.setFixedSize(0, 10)
        layout.addWidget(spacer, 5, 0)
        layout.addWidget(optionsLabel, 6, 0)
        layout.addWidget(self.caseSens, 6, 1)
        layout.addWidget(self.wholeWords, 6, 2)

        self.setGeometry(300, 300, 360, 100)
        self.setWindowTitle("Find and Replace")
        self.setLayout(layout)

        # By default the normal mode is activated
        self.normalRadio.setChecked(True)

    def find(self):
        text = self.parent.textArea.toPlainText()
        # And the text to search
        query = self.findField.toPlainText()
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

    def replace(self):
        cursor = self.parent.textArea.textCursor()
        # Security
        if self.lastMatch and cursor.hasSelection():
            cursor.insertText(self.replaceField.toPlainText())
            # Setting new cursor
            self.parent.textArea.setTextCursor(cursor)

    def replaceAll(self):
        self.lastMatch = None
        self.find()
        # Replace and find until find is None again
        while self.lastMatch:
            self.replace()
            self.find()

    def regexMode(self):
        # Uncheck the checkboxes
        self.caseSens.setChecked(False)
        self.wholeWords.setChecked(False)
        # Disable
        self.caseSens.setEnabled(False)
        self.wholeWords.setEnabled(False)

    def normalMode(self):
        self.caseSens.setEnabled(True)
        self.wholeWords.setEnabled(True)

    def moveCursor(self, start, end):
        cursor = self.parent.textArea.textCursor()
        cursor.setPosition(start)
        # Move the Cursor over the match and pass the KeepAnchor parameter
        # which will make the cursor select the the match's text
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                            end - start)
        self.parent.textArea.setTextCursor(cursor)
