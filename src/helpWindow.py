from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon("icons/question.png"))
        self.resize(QSize(500, 250))

        # Help message
        m = """
        To create a new bucket list, click the leftmost
        green plus icon. Click on the newly created tab,
        and double click on the tab to rename it.
        
        To add a new item, click the writing icon. Click on
        the newly created item, and its properties will
        appear in the Inspector.

        Edit the item's name, description, and status and
        click Save to lock in those changes.

        Use the up and down arrow keys to shift the ordering
        of the items.

        Click the red X icon or scissor icon to remove
        a tab or an item, respectively.

        Hover over an icon to see its shortcut key combination.
        """
        label = QLabel(m)
        self.setCentralWidget(label)