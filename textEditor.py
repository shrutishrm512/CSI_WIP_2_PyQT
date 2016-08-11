#!/usr/bin/python

# Text - Editor
from ext import *

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Editor(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.filenm = ""
        self.updateUI()

    def updateUI(self):
        # set text area
        self.textArea = QTextEdit()
        self.setCentralWidget(self.textArea)
        # UPDATING TOOLBAR
        self.toolbar = self.addToolBar("Text Actions")
        self.updateToolBar()
        # UPDATING FORMATBAR
        self.formatBar = self.addToolBar("Format")
        self.updateFormatBar()
        # UPDATING MENUBAR
        self.menubar = self.menuBar()
        self.updateMenuBar()
        # UPDATING STATUSBAR
        self.statusBar = self.statusBar()
        self.updateStatusBar()
        self.resize(1030, 800)
        self.move(100, 100)
        self.textArea.setTabStopWidth(33)  # 8 spaces
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.setWindowTitle("Text Editor")

    def updateStatusBar(self):
        self.statusBar.setSizeGripEnabled(True)
        # ADDING SLIDER FOR ZOOM
        self.zoomSlider = QSlider(Qt.Horizontal, self.statusBar)
        self.zoomSlider.setTickPosition(QSlider.TicksAbove)
        self.zoomSlider.setTickInterval(10)
        # SETTING DEFAULT VALUE
        self.zoomSlider.setValue(80)
        # SETTING RANGE OF SLIDER
        self.zoomSlider.setRange(70, 90)
        # STORES THE CURRENT VALUE OF ZOOM
        self.curZoomValue = 80
        # TO DISPLAY WORD AND SYMBOL COUNT
        self.countLabel = QLabel(self)
        self.positionLabel = QLabel(self)
        self.emptyLabel = QLabel(self)
        self.statusBar.insertPermanentWidget(0, self.emptyLabel, 10)
        self.statusBar.insertPermanentWidget(1, self.positionLabel, 10)
        self.statusBar.insertPermanentWidget(2, self.countLabel, 10)
        self.statusBar.insertPermanentWidget(3, self.zoomSlider, 4)
        # CALCULATES AND DISPLAYS CURSER POSITION
        self.cursorPosition()
        # TO STORE IF ANY CHANGES ARE MADE IN OPENED FILE
        self.changesDone = False
        self.connect(self.zoomSlider, SIGNAL("valueChanged(int)"), self.zoom)
        self.connect(self.textArea, SIGNAL("cursorPositionChanged()"),
                     self.cursorPosition)

    def zoom(self):
        value = self.zoomSlider.value()
        if self.curZoomValue > value:
            self.textArea.zoomOut((self.curZoomValue - value))
        else:
            self.textArea.zoomIn((value - self.curZoomValue))
        self.curZoomValue = value

    def cursorPosition(self):
        self.changesDone = True
        cursor = self.textArea.textCursor()
        curLine = str(cursor.blockNumber() + 1)
        curCol = str(cursor.columnNumber())
        # #print curLine, curCol
        self.positionLabel.setText(curLine + ',' + curCol)
        self.wordSymbolCount()

    def wordSymbolCount(self):
        selectedText = self.textArea.textCursor().selectedText()
        if selectedText == '':
            text = self.textArea.toPlainText()
            wordCount = len(text.split(' '))
            symbolCount = len(text)
        else:
            wordCount = len(selectedText.split(' '))
            symbolCount = len(selectedText)
        # #print wordCount, symbolCount
        self.countLabel.setText("Word: " + str(wordCount) + ", " +
                                "Symbols: " + str(symbolCount))

    def updateToolBar(self):
        # NEW DOCUMENT
        self.new = QAction(QIcon("icons/new.png"), "New", self)
        self.new.setStatusTip("Create a new document")
        self.new.setShortcut("Ctrl+N")
        self.new.triggered.connect(self.new_doc)
        # OPEN EXISTING DOCUMENT
        self.open = QAction(QIcon("icons/open.png"), "Open file", self)
        self.open.setStatusTip("Open the existing document")
        self.open.setShortcut("Ctrl+O")
        self.open.triggered.connect(self.open_doc)
        # SAVE FILE
        self.save = QAction(QIcon("icons/save.png"), "Save current file", self)
        self.save.setStatusTip("Save the current document")
        self.save.setShortcut("Ctrl+S")
        self.save.triggered.connect(self.save_doc)
        # EXPORT TO PDF
        self.pdf = QAction(QIcon("icons/pdf.jpg"), "Export as PDF", self)
        self.pdf.setStatusTip("Converting file to pdf")
        self.pdf.triggered.connect(self.exportPdf)
        # PRINT
        self.Print = QAction(QIcon("icons/print.svg"), "Print document", self)
        self.Print.setStatusTip("Print the document")
        self.Print.setShortcut("Ctrl+P")
        self.Print.triggered.connect(self.print_doc)
        # PRINT PREVIEW
        self.preview = QAction(QIcon("icons/preview.png"), "Page view", self)
        self.preview.setStatusTip("Preview page before printing")
        self.preview.setShortcut("Ctrl+Shift+O")
        self.preview.triggered.connect(self.preview_doc)
        # UNDO
        self.undo = QAction(QIcon("icons/undo.png"), "Undo last action", self)
        self.undo.setStatusTip("Undo the document")
        self.undo.setShortcut("Ctrl+Z")
        self.undo.triggered.connect(self.textArea.undo)
        # REDO
        self.redo = QAction(QIcon("icons/redo.jpg"), "Redo last undone action",
                            self)
        self.redo.setStatusTip("Redo the document")
        self.redo.setShortcut("Ctrl+Y")
        self.redo.triggered.connect(self.textArea.redo)
        # CUT
        self.cut = QAction(QIcon("icons/cut.png"), "Cut the selection", self)
        self.cut.setStatusTip("Delete and Copy text")
        self.cut.setShortcut("Ctrl+X")
        self.cut.triggered.connect(self.textArea.cut)
        # COPY
        self.copy = QAction(QIcon("icons/copy.png"), "Copy the selection",
                            self)
        self.copy.setStatusTip("Copy text")
        self.copy.setShortcut("Ctrl+C")
        self.copy.triggered.connect(self.textArea.copy)
        # PASTE
        self.paste = QAction(QIcon("icons/paste.png"), "Paste the clipboard",
                             self)
        self.paste.setStatusTip("Paste text from clipboard")
        self.paste.setShortcut("Ctrl+V")
        self.paste.triggered.connect(self.textArea.paste)
        # SEARCH
        self.search = QAction(QIcon("icons/search.png"), "Search for text",
                              self)
        self.search.setStatusTip("Search text from clipboard")
        self.search.setShortcut("Ctrl+Q")
        self.search.triggered.connect(find.Search(self).show)
        # FIND & REPLACE
        self.find = QAction(QIcon("icons/find.png"), "Find & replace text",
                            self)
        self.find.setStatusTip("Find and replace the text from clipboard")
        self.find.setShortcut("Ctrl+F")
        self.find.triggered.connect(find_n_replace.FindandReplace(self).show)
        # BULLET LIST
        bulletlist = QAction(QIcon("icons/bullet.svg"), "Insert bullet List",
                             self)
        bulletlist.setStatusTip("Insert bullet list")
        bulletlist.setShortcut("Ctrl+Shift+B")
        bulletlist.triggered.connect(self.bulletList)
        # NUMBERED LIST
        numberlist = QAction(QIcon("icons/number.png"), "Insert numbered List",
                             self)
        numberlist.setStatusTip("Insert numbered list")
        numberlist.setShortcut("Ctrl+Shift+L")
        numberlist.triggered.connect(self.numberedList)
        # closing the file
        self.clos = QAction(QIcon("icons/close.png"), "Close the File", self)
        self.clos.setStatusTip("Closing the file")
        self.clos.setShortcut(QKeySequence(Qt.Key_Escape))
        self.clos.triggered.connect(self.close_doc)
        # ADDING ACTIONS TO TOOLBAR
        self.toolbar.addAction(self.new)
        self.toolbar.addAction(self.open)
        self.toolbar.addAction(self.save)
        # separating line
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.pdf)
        self.toolbar.addAction(self.Print)
        self.toolbar.addAction(self.preview)
        # separating
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undo)
        self.toolbar.addAction(self.redo)
        # separating
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.cut)
        self.toolbar.addAction(self.copy)
        self.toolbar.addAction(self.paste)
        # separating
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.search)
        self.toolbar.addAction(self.find)
        # separating
        self.toolbar.addSeparator()
        self.toolbar.addAction(bulletlist)
        self.toolbar.addAction(numberlist)
        # separating
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.clos)
        self.addToolBarBreak()

    def updateFormatBar(self):
        self.formatBar.setMovable(False)
        self.formatBar.setFloatable(False)
        fontnames = QFontComboBox(self)
        fontnames.currentFontChanged.connect(self.fontFamily)
        # different font sizes
        fontSize = QComboBox(self)
        fontSize.setEditable(True)
        # Minimum number of chars displayed
        fontSize.setMinimumContentsLength(3)
        fontSize.activated.connect(self.FontSize)
        # Typical font sizes
        fsizelist = ['6', '7', '8', '9', '10', '10.5', '11', '12',
                     '13', '14', '15', '16', '18', '20', '22', '24',
                     '26', '28', '32', '36', '40', '44', '48', '54',
                     '60', '66', '72', '80', '88', '96']

        for i in fsizelist:
                fontSize.addItem(i)
        # set text colour
        fontcolor = QAction(QIcon("icons/fontcolor.png"), "Font Color", self)
        fontcolor.setStatusTip("Change font color")
        fontcolor.triggered.connect(self.fontColor)
        # set background colour
        backcolor = QAction(QIcon("icons/bckcolor.png"), "Background Color",
                            self)
        backcolor.setStatusTip("Change background color")
        backcolor.triggered.connect(self.backColor)
        # bold text
        boldtext = QAction(QIcon("icons/bold.png"), "Bold", self)
        boldtext.triggered.connect(self.bold)
        # italic text
        italictext = QAction(QIcon("icons/italic.png"), "Italic", self)
        italictext.triggered.connect(self.italic)
        # underline the text
        underltext = QAction(QIcon("icons/under.png"), "Underline", self)
        underltext.triggered.connect(self.underline)
        # strike action
        strike = QAction(QIcon("icons/strike.png"), "Strike-out", self)
        strike.triggered.connect(self.strike)

        superscript = QAction(QIcon("icons/super.png"), "Superscript", self)
        superscript.triggered.connect(self.superScript)

        subscript = QAction(QIcon("icons/sub.jpg"), "Subscript", self)
        subscript.triggered.connect(self.subScript)
        # different alignments
        alignLeft = QAction(QIcon("icons/left.png"), "Align left", self)
        alignLeft.setShortcut("Ctrl+L")
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QAction(QIcon("icons/center.png"), "Centered", self)
        alignCenter.setShortcut("Ctrl+E")
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QAction(QIcon("icons/right.png"), "Align Right", self)
        alignRight.setShortcut("Ctrl+R")
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QAction(QIcon("icons/justify.png"), "Justified", self)
        alignJustify.setShortcut("Ctrl+J")
        alignJustify.triggered.connect(self.alignJustify)
        # Increase the indent of area
        indent = QAction(QIcon("icons/indent.png"), "Increase Indent", self)
        indent.setShortcut("Ctrl+Tab")
        indent.triggered.connect(self.indent)
        # Decrease the indent of area
        dedent = QAction(QIcon("icons/dedent.png"), "Decrease Indent", self)
        dedent.setShortcut("Shift+Tab")
        dedent.triggered.connect(self.dedent)
        # Change case
        case = QAction(QIcon("icons/case.png"), "Changing case", self)
        case.triggered.connect(self.changeCase)

        self.formatBar.addWidget(fontnames)
        self.formatBar.addSeparator()
        self.formatBar.addWidget(fontSize)
        # separating
        self.formatBar.addSeparator()
        self.formatBar.addAction(boldtext)
        self.formatBar.addAction(italictext)
        self.formatBar.addAction(underltext)
        # separating
        self.formatBar.addSeparator()
        self.formatBar.addAction(strike)
        self.formatBar.addAction(superscript)
        self.formatBar.addAction(subscript)
        # separating
        self.formatBar.addSeparator()
        self.formatBar.addAction(alignLeft)
        self.formatBar.addAction(alignCenter)
        self.formatBar.addAction(alignRight)
        self.formatBar.addAction(alignJustify)
        # separating
        self.formatBar.addSeparator()
        self.formatBar.addAction(case)
        self.formatBar.addAction(indent)
        self.formatBar.addAction(dedent)
        # separating
        self.formatBar.addSeparator()
        self.formatBar.addAction(fontcolor)
        self.formatBar.addAction(backcolor)
        self.formatBar.addSeparator()

    def updateMenuBar(self):
        self.fileMenu = self.menubar.addMenu('&File')
        self.updateFileMenu()
        self.editMenu = self.menubar.addMenu('&Edit')
        self.updateEditMenu()
        self.viewMenu = self.menubar.addMenu('&View')
        self.updateViewMenu()
        self.insertMenu = self.menubar.addMenu('&Insert')
        self.updateInsertMenu()

    def updateFileMenu(self):
        self.fileMenu.addAction(self.new)
        self.fileMenu.addAction(self.open)
        self.fileMenu.addAction(self.save)
        self.fileMenu.addAction(self.pdf)
        self.fileMenu.addAction(self.Print)
        self.fileMenu.addAction(self.preview)
        self.fileMenu.addAction(self.clos)

    def updateEditMenu(self):
        self.editMenu.addAction(self.undo)
        self.editMenu.addAction(self.undo)
        self.editMenu.addAction(self.redo)
        self.editMenu.addAction(self.cut)
        self.editMenu.addAction(self.copy)
        self.editMenu.addAction(self.paste)
        self.editMenu.addAction(self.search)
        self.editMenu.addAction(self.find)

    def updateViewMenu(self):
        fullScreenAction = QAction(QIcon(''), 'Full Screen', self,
                                   checkable=True)
        fullScreenAction.setShortcut(QKeySequence(Qt.Key_F11))
        self.connect(fullScreenAction, SIGNAL("triggered()"), self.fullScreen)
        self.viewMenu.addAction(fullScreenAction)
        self.toolbarAction = QAction(QIcon(''), 'Toolbar', self,
                                     checkable=True)
        self.toolbarAction.setChecked(True)
        self.connect(self.toolbarAction, SIGNAL("triggered()"),
                     self.showHideToolbar)
        self.viewMenu.addAction(self.toolbarAction)

    def updateInsertMenu(self):
        self.imageAction = QAction(QIcon(''), "Image", self)
        self.connect(self.imageAction, SIGNAL("triggered()"), self.insertImage)
        self.insertMenu.addAction(self.imageAction)

    def showHideToolbar(self):
        if self.toolbarAction.isChecked() is True:
            self.formatBar.show()
        else:
            self.formatBar.hide()

    def fullScreen(self):
        if self.isFullScreen() is True:
            self.showNormal()
        else:
            self.showFullScreen()

    def insertImage(self):
        filename = QFileDialog.getOpenFileName(self, 'Insert image', ".",
                                               "Images(*.png *.xpm *.jpg *.bmp\
                                               *.gif)")
        if filename:
            image = QImage(filename)
            if image.isNull():
                popup = QMessageBox(QMessageBox.Critical, "Image load error",
                                    "Could not load image file!",
                                    QMessageBox.Ok, self)
                popup.show()
            else:
                cursor = self.textArea.textCursor()
                cursor.insertImage(image, filename)

    def new_doc(self):
        # self.textArea.clear()
        newfile = Editor(self)
        newfile.show()

    def open_doc(self):
        self.changesDone = False
        self.filenm = QFileDialog.getOpenFileName(self, 'Open File', ".")
        if self.filenm:
            with open(self.filenm, "r+") as file:
                self.textArea.setText(file.read())

    def save_doc(self):
        if self.changesDone is True:
            if not self.filenm:
                self.filenm = QFileDialog.getSaveFileName(self, 'Save File')
            if self.filenm:
                with open(self.filenm, "w+") as file:
                    file.write(self.textArea.toHtml())
                    self.changesDone = False

    def exportPdf(self):
        printer = QPrinter()
        printer.setOutputFormat(printer.NativeFormat)
        dialog = QPrintDialog(printer)
        dialog.setOption(dialog.PrintToFile)
        if dialog.exec_() == QDialog.Accepted:
            self.textArea.document().print_(dialog.printer())

    def print_doc(self):
        # opening print dialog
            dialog_box = QPrintDialog()
            if dialog_box.exec_() == QDialog.Accepted:
                self.textArea.document().print_(dialog_box.printer())

    def preview_doc(self):
        pageview = QPrintPreviewDialog()
        pageview.paintRequested.connect(self.textArea.print_)
        pageview.exec_()

    def bulletList(self):
        textcursor = self.textArea.textCursor()
        textcursor.insertList(QTextListFormat.ListDisc)

    def numberedList(self):
        textcursor = self.textArea.textCursor()
        textcursor.insertList(QTextListFormat.ListDecimal)

    def close_doc(self):
            self.close()

    def closeEvent(self, event):
        if self.changesDone is True:
            msg_box = QMessageBox.question(self,
                                           'Save the document before closing?',
                                           "Changes will lost. Wanna Save?",
                                           QMessageBox.Yes | QMessageBox.No |
                                           QMessageBox.Cancel, QMessageBox.No)

            if msg_box == QMessageBox.Yes:
                event.accept()
                self.save_doc()
            elif msg_box == QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()

    def fontFamily(self, font):
        font = QFont(font)
        self.textArea.setCurrentFont(font)

    def FontSize(self, fontsize):
        self.textArea.setFontPointSize(int(fontsize))

    def fontColor(self):
        # select colour from color dialog
            textcolor = QColorDialog.getColor()
        # Setting new text color
            self.textArea.setTextColor(textcolor)

    def backColor(self):
        bckcolor = QColorDialog.getColor()
        # after selecting,setting new bckcolor
        self.textArea.setTextBackgroundColor(bckcolor)

    def bold(self):
        b = self.textArea.fontWeight()
        if b == QFont.Normal:
            self.textArea.setFontWeight(QFont.Bold)
        else:
            self.textArea.setFontWeight(QFont.Normal)

    def italic(self):
        i = self.textArea.fontItalic()
        if i is False:
            self.textArea.setFontItalic(True)
        else:
            self.textArea.setFontItalic(False)

    def underline(self):
        u = self.textArea.fontUnderline()
        if u is False:
            self.textArea.setFontUnderline(True)
        else:
            self.textArea.setFontUnderline(False)

    def strike(self):
        ftxt = self.textArea.currentCharFormat()
        ftxt.setFontStrikeOut(not ftxt.fontStrikeOut())
        self.textArea.setCurrentCharFormat(ftxt)

    def superScript(self):
        ftxt = self.textArea.currentCharFormat()
        alignment = ftxt.verticalAlignment()
        if alignment is QTextCharFormat.AlignNormal:
            ftxt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
        else:
            ftxt.setVerticalAlignment(QTextCharFormat.AlignNormal)
            self.textArea.setCurrentCharFormat(ftxt)

    def subScript(self):
        ftxt = self.textArea.currentCharFormat()
        alignment = ftxt.verticalAlignment()
        if alignment is QTextCharFormat.AlignNormal:
            ftxt.setVerticalAlignment(QTextCharFormat.AlignSubScript)
        else:
            ftxt.setVerticalAlignment(QTextCharFormat.AlignNormal)
            self.textArea.setCurrentCharFormat(ftxt)

    def alignLeft(self):
        self.textArea.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.textArea.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.textArea.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.textArea.setAlignment(Qt.AlignJustify)

    def changeCase(self):
        fmt1 = QTextCharFormat()
        fmt1.setFontCapitalization(QFont.AllUppercase)
        self.textArea.setCurrentCharFormat(fmt1)

    def indent(self):
        cur = self.textArea.textCursor()
        if cur.hasSelection():
            temp = cur.blockNumber()
            cur.setPosition(cur.selectionEnd())
            # Calculate range of selection
            diff = cur.blockNumber() - temp

            for n in range(diff + 1):
                cur.movePosition(QTextCursor.StartOfLine)
                cur.insertText("\t")
                # move back up
                cur.movePosition(QTextCursor.Up)

            else:
                cur.insertText("\t")

    def dedent(self):
        cur = self.textArea.textCursor()
        if cur.hasSelection():
            temp = cur.blockNumber()
            cur.setPosition(cur.selectionEnd())
            # Calculate range of selection
            diff = cur.blockNumber() - temp

            for n in range(diff + 1):
                self.handleDedent(cur)
                cur.movePosition(QTextCursor.Up)

            else:
                self.handleDedent(cur)

    def handleDedent(self, cur):
        cur.movePosition(QTextCursor.StartOfLine)
        # Grab the current line
        line = cur.block().text()
        # If the line starts with a tab character, delete it
        if line.startsWith("\t"):
            # Delete next character
            cur.deleteChar()
        else:
            for char in line[:8]:
                if char != " ":
                    break
                cur.deleteChar()


def main():
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
