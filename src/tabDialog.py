from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class TabDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buckets")
        self.setWindowIcon(QIcon("icons/list.png"))
        self.resize(QSize(250, 125))

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.editor = QLineEdit()
        self.editor.setPlaceholderText("New tab name")
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)