import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from src.helpWindow import HelpWindow
from src.bucketList import *


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the main window by setting up
        the toolbar and tabs.
        """
        # Setup window
        super().__init__()
        self.setWindowTitle("Buckets")
        self.setWindowIcon(QIcon("icons/list.png"))
        self.resize(QSize(900, 500))

        # Setup bucket list
        self.bucket = BucketList("My Bucket List")

        # Setup widgets
        self.setup_toolbar()
        self.setup_tabs()

    def setup_toolbar(self):
        """
        Sets up the toolbar by creating the
        necessary QActions.
        """
        # Create toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)

        # Toolbar actions
        add_button = QAction(QIcon("icons/plus.png"), "Add", self)
        undo_button = QAction(QIcon("icons/undo.png"), "Undo", self)
        redo_button = QAction(QIcon("icons/redo.png"), "Redo", self)
        cut_button = QAction(QIcon("icons/scissors.png"), "Cut", self)
        help_button = QAction(QIcon("icons/question.png"), "Help", self)

        # Action shortcuts
        add_button.setShortcut(QKeySequence("Ctrl+a"))
        undo_button.setShortcut(QKeySequence("Ctrl+z"))
        redo_button.setShortcut(QKeySequence("Ctrl+y"))
        cut_button.setShortcut(QKeySequence("Ctrl+x"))
        help_button.setShortcut(QKeySequence("Ctrl+h"))

        # Toolbar connects
        add_button.triggered.connect(self.add)
        undo_button.triggered.connect(self.undo)
        redo_button.triggered.connect(self.redo)
        cut_button.triggered.connect(self.cut)
        help_button.triggered.connect(self.show_help_window)

        # Add to toolbar
        toolbar.addSeparator()
        toolbar.addAction(add_button)
        toolbar.addAction(undo_button)
        toolbar.addAction(redo_button)
        toolbar.addAction(cut_button)
        toolbar.addAction(help_button)
        toolbar.setMovable(False)

    def add(self):
        print("Add")
        self.test.addItem("hello")

    def undo(self):
        print("Undo")

    def redo(self):
        print("Redo")

    def cut(self):
        print("Cut")

    def show_help_window(self):
        """
        Shows the help window when the
        help QAction is clicked.
        """
        self.help_window = HelpWindow()
        self.help_window.show()

    def setup_tabs(self):
        tabs = QTabWidget()
        layout = QHBoxLayout()

        self.test = QListWidget()

        layout.addWidget(self.test)
        layout.addWidget(Color('green'))
        layout.setStretch(0, 2)
        layout.setStretch(1, 1)

        widget = QWidget()
        widget.setLayout(layout)
        tabs.addTab(widget, QIcon(""), self.bucket.title)
        self.setCentralWidget(tabs)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

app = QApplication([])
window = MainWindow()
window.show()

app.exec()