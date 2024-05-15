from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt
from typing import Optional

class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None)-> None:
        super().__init__(text, parent)
        self.configStyle()
        
    def configStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
