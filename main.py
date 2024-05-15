from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, \
QPushButton, QLineEdit, QGridLayout, QSizePolicy
from main_window import MainWindow
from display import Display
from PySide6.QtGui import QIcon
from info import Info
from PySide6.QtCore import Qt
from variables import  WINDOW_ICON_PATH
import sys
import qdarktheme
from styles import setupTheme
from buttons import Button, ButtonsGrid


if __name__ == '__main__':
    # Cria a aplicacao
    
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()
    

    # Define o icone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)


    # Cria o display
    display = Display()
    window.addWidgetToVLayout(display)
    
    

    # Grid de botoes
    buttonsGrid = ButtonsGrid(display, info, window)
    window.addButtonsGrid(buttonsGrid)

    # Buttons


    # Exxecuta tudo
    window.adjustFixedSize()
    window.show()
    app.exec()