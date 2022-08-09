import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from src.helpWindow import HelpWindow
from src.bucketList import *
from src.color import *


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
        self.resize(QSize(1000, 500))

        # Setup bucket list
        self.bucket = BucketList("My Bucket List")

        # Setup widgets
        self.setup_lists()
        self.setup_toolbar()
        self.setup_tabs()
        self.setup_inspector()
        self.setup_layout()

        self.MainWidget = QWidget()
        self.MainWidget.setLayout(self.layout)
        self.setCentralWidget(self.MainWidget)

    def setup_lists(self):
        self.listWidget = QListWidget()
        self.listWidget.clicked.connect(self.item_clicked)

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

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self.listWidget, QIcon(""), self.bucket.title)

    def setup_inspector(self):
        self.titleEdit = QLineEdit()
        self.titleEdit.setEnabled(False)

        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.setEnabled(False)
        
        self.itemStatus = QComboBox()
        self.itemStatus.setPlaceholderText(" ")
        self.itemStatus.setEnabled(False)
        self.itemStatus.addItems(["Not Started", "In Progress", "Completed"])

        self.lastModified = QLabel("")

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.inspector_save)

        self.inspector = QGroupBox("Inspector")
        self.inspector_layout = QVBoxLayout()
        self.inspector_form = QWidget()
        self.inspector_form_layout = QFormLayout()
        self.inspector_form_layout.addRow("Title:", self.titleEdit)
        self.inspector_form_layout.addRow("Description:", self.descriptionEdit)
        self.inspector_form_layout.addRow("Status:", self.itemStatus)
        self.inspector_form_layout.addRow("Last Modified:", self.lastModified)
        self.inspector_form.setLayout(self.inspector_form_layout)

        self.inspector_layout.addWidget(self.inspector_form)
        self.inspector_layout.addWidget(self.save_button)
        self.inspector.setLayout(self.inspector_layout)

    def setup_layout(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.inspector)
        self.layout.setStretch(0, 2)
        self.layout.setStretch(1, 1)

    def add(self):
        item = self.bucket.add_item("New item")
        self.listWidget.addItem(item.title)

    def undo(self):
        print("Undo")

    def redo(self):
        print("Redo")

    def cut(self):
        i = self.listWidget.currentRow()
        if i >= 0:
            self.bucket.remove_index(i)
            self.listWidget.takeItem(i)

            self.titleEdit.clear()
            self.titleEdit.setEnabled(False)
            self.descriptionEdit.clear()
            self.descriptionEdit.setEnabled(False)
            self.itemStatus.clear()
            self.itemStatus.setEnabled(False)
            self.lastModified.setText("")

    def show_help_window(self):
        self.help_window = HelpWindow()
        self.help_window.show()

    def item_clicked(self):
        i = self.listWidget.currentRow()
        self.titleEdit.clear()
        self.titleEdit.setEnabled(True)
        self.titleEdit.insert(self.bucket.items[i].title)
        self.descriptionEdit.clear()
        self.descriptionEdit.setEnabled(True)
        self.descriptionEdit.setText(self.bucket.items[i].description)
        self.itemStatus.setEnabled(True)
        self.itemStatus.clear()
        self.itemStatus.addItems(["Not Started", "In Progress", "Completed"])
        self.itemStatus.setCurrentIndex(self.bucket.items[i].status)
        self.lastModified.setText(self.bucket.items[i].last_modified)

    def inspector_save(self):
        i = self.listWidget.currentRow()
        
        self.bucket.items[i].set_title(self.titleEdit.text())
        self.listWidget.currentItem().setText(self.titleEdit.text())
        self.bucket.items[i].set_description(self.descriptionEdit.toPlainText())
        self.bucket.items[i].set_status(self.itemStatus.currentIndex())

        self.lastModified.setText(self.bucket.items[i].last_modified)
        
        


app = QApplication([])
window = MainWindow()
window.show()

app.exec()