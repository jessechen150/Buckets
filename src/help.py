from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon("icons/question.png"))
        self.resize(QSize(450, 250))