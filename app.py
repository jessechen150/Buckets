import os
import pickle
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from src.helpWindow import HelpWindow
from src.tabDialog import TabDialog
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
        self.resize(QSize(1000, 500))

        # Setup bucket list
        # self.bucket = BucketList("My Bucket List")
        self.buckets = []
        self.lists = []
        self.tabs = QTabWidget()

        # Setup widgets
        if os.path.exists(path := "data/save.pickle"):
            self.load_saved(path)
        else:
            self.setup_lists()
            self.setup_tabs()
        self.setup_toolbar()
        self.setup_inspector()
        self.setup_layout()

        self.MainWidget = QWidget()
        self.MainWidget.setLayout(self.layout)
        self.setCentralWidget(self.MainWidget)

    def setup_lists(self):
        self.buckets.append(BucketList("New bucket list"))
        self.lists.append(QListWidget())
        self.lists[-1].clicked.connect(self.item_clicked)

    def setup_tabs(self):
        self.tabs.addTab(self.lists[-1], QIcon(""), self.buckets[-1].title)
        self.tabs.currentChanged.connect(self.clear_inspector)
        self.tabs.tabBarDoubleClicked.connect(self.edit_tab_name)

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
        add_tab_button = QAction(QIcon("icons/plus.png"), "Add a new bucket list", self)
        cut_tab_button = QAction(QIcon("icons/cross.png"), "Remove current bucket list", self)
        add_item_button = QAction(QIcon("icons/pencil-plus.png"), "Add a new item", self)
        cut_item_button = QAction(QIcon("icons/scissors.png"), "Remove current item", self)
        up_button = QAction(QIcon("icons/arrow-up.png"), "Shift item up", self)
        down_button = QAction(QIcon("icons/arrow-down.png"), "Shift item down", self)
        help_button = QAction(QIcon("icons/question.png"), "Help", self)

        # Action shortcuts
        add_tab_button.setShortcut(QKeySequence("Ctrl+t"))
        cut_tab_button.setShortcut(QKeySequence("Ctrl+w"))
        add_item_button.setShortcut(QKeySequence("Ctrl+a"))
        cut_item_button.setShortcut(QKeySequence("Ctrl+x"))
        up_button.setShortcut(QKeySequence("Shift+Up"))
        down_button.setShortcut(QKeySequence("Shift+Down"))
        help_button.setShortcut(QKeySequence("Ctrl+h"))

        # Toolbar action connects
        add_tab_button.triggered.connect(self.add_tab)
        cut_tab_button.triggered.connect(self.cut_tab)
        add_item_button.triggered.connect(self.add_item)
        cut_item_button.triggered.connect(self.cut_item)
        up_button.triggered.connect(self.shift_up)
        down_button.triggered.connect(self.shift_down)
        help_button.triggered.connect(self.show_help_window)

        # Add to toolbar
        toolbar.addAction(add_tab_button)
        toolbar.addAction(cut_tab_button)
        toolbar.addAction(add_item_button)
        toolbar.addAction(cut_item_button)
        toolbar.addAction(up_button)
        toolbar.addAction(down_button)
        toolbar.addAction(help_button)
        toolbar.setMovable(False)

    def load_saved(self, path):
        saved_buckets = pickle.load(open(path, "rb"))
        

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
        self.save_button.setEnabled(False)
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

    def clear_inspector(self):
        self.titleEdit.clear()
        self.titleEdit.setEnabled(False)
        self.descriptionEdit.clear()
        self.descriptionEdit.setEnabled(False)
        self.itemStatus.clear()
        self.itemStatus.setEnabled(False)
        self.lastModified.setText("")

    def setup_layout(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.inspector)
        self.layout.setStretch(0, 2)
        self.layout.setStretch(1, 1)

    def add_tab(self):
        self.setup_lists()
        self.tabs.addTab(self.lists[-1], QIcon(""), self.buckets[-1].title)

    def cut_tab(self):
        i = self.tabs.currentIndex()
        if i >= 0:
            self.buckets.pop(i)
            self.lists.pop(i)
            self.tabs.removeTab(i)

            self.clear_inspector()

    def add_item(self):
        tab_i = self.tabs.currentIndex()
        if tab_i >= 0:
            item = self.buckets[tab_i].add_item("New item")
            self.lists[tab_i].addItem(item.title)

    def cut_item(self):
        tab_i = self.tabs.currentIndex()
        if tab_i >= 0:
            i = self.lists[tab_i].currentRow()
            if i >= 0:
                self.buckets[tab_i].remove_index(i)
                self.lists[tab_i].takeItem(i)

                self.clear_inspector()

    def shift_up(self):
        tab_i = self.tabs.currentIndex()
        if tab_i >= 0:
            i = self.lists[tab_i].currentRow()
            if i > 0:
                item = self.lists[tab_i].takeItem(i)
                self.lists[tab_i].insertItem(i-1, item)
                self.lists[tab_i].setCurrentRow(i-1)

    def shift_down(self):
        tab_i = self.tabs.currentIndex()
        if tab_i >= 0:
            i = self.lists[tab_i].currentRow()
            if i >= 0 and i+1 < len(self.buckets[tab_i]):
                item = self.lists[tab_i].takeItem(i)
                self.lists[tab_i].insertItem(i+1, item)
                self.lists[tab_i].setCurrentRow(i+1)

    def show_help_window(self):
        self.help_window = HelpWindow()
        self.help_window.show()

    def item_clicked(self):
        tab_i = self.tabs.currentIndex()
        if tab_i >= 0:
            i = self.lists[tab_i].currentRow()
            self.titleEdit.clear()
            self.titleEdit.setEnabled(True)
            self.titleEdit.insert(self.buckets[tab_i].items[i].title)
            self.descriptionEdit.clear()
            self.descriptionEdit.setEnabled(True)
            self.descriptionEdit.setText(self.buckets[tab_i].items[i].description)
            self.itemStatus.setEnabled(True)
            self.itemStatus.clear()
            self.itemStatus.addItems(["Not Started", "In Progress", "Completed"])
            self.itemStatus.setCurrentIndex(self.buckets[tab_i].items[i].status)
            self.lastModified.setText(self.buckets[tab_i].items[i].last_modified)
            self.save_button.setEnabled(True)

    def inspector_save(self):
        tab_i = self.tabs.currentIndex()
        if tab_i >= 0:
            i = self.lists[tab_i].currentRow()
            
            if i >= 0:
                self.buckets[tab_i].items[i].set_title(self.titleEdit.text())
                self.lists[tab_i].currentItem().setText(self.titleEdit.text())
                self.buckets[tab_i].items[i].set_description(self.descriptionEdit.toPlainText())
                self.buckets[tab_i].items[i].set_status(self.itemStatus.currentIndex())

                self.lastModified.setText(self.buckets[tab_i].items[i].last_modified)
            else:
                self.save_button.setEnabled(False)

    def edit_tab_name(self):
        dialog = TabDialog(self)
        if dialog.exec():
            if len(new_name := dialog.editor.text()):
                tab_i = self.tabs.currentIndex()
                self.tabs.setTabText(tab_i, new_name)
            else:
                return
        else:
            return
        
    def closeEvent(self, event):
        pickle.dump(self.buckets, open("data/save.pickle", "wb"))
        event.accept()

app = QApplication([])

window = MainWindow()
window.show()

app.exec()