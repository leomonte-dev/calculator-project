from PySide6.QtWidgets import QApplication, QMainWindow, \
QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtGui import QIcon 

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Configurando o layout 
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)
        


        # Titulo da janela
        self.setWindowTitle('Calculadora')


    def adjustFixedSize(self):
        # Ultima coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
        
    
    def addButtonsGrid(self, buttonsGrid):
        self.vLayout.addLayout(buttonsGrid)
        

    def makeMsgBox(self):
        return QMessageBox(self)
        

        
        
            