import math
from PySide6.QtWidgets import QPushButton, QGridLayout, QLineEdit
from PySide6.QtCore import Slot, Qt, Signal, QObject
from variables import MEDIUM_FONT_SIZE, SMALL_FONT_SIZE
from utils import isNumrOrDot, isEmpty, isValidNumber, convertToNumber
from typing import TYPE_CHECKING
from tkinter import messagebox
from tkinter.ttk import Style

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        
        
    

    def configStyle(self):
        font = self.font()
        font.setPixelSize(SMALL_FONT_SIZE) 
        font.setBold(False)
        self.setFont(font)
        self.setMinimumSize(60 , 60)

        

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow',
                  *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridmask_ = [
            ['C', 'Del', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-',  '0', '.', '='],
        ]

        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitial = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None


        self.equation = self._equationInitial
        self._makeGrid()
        


    @property
    def equation(self):
        return self._equation    
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)
    
    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for i, row in enumerate(self._gridmask_):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumrOrDot(buttonText) and not isEmpty(buttonText):
                    if buttonText == '+/-':
                        button.setProperty('cssClass', 'nButton')
                        self._connectButtonClicked(button, self._invertNumber)
                        self.display.setFocus()
                        

                    else:
                        button.setProperty('cssClass', 'specialButton')
                        self._configSpecialButton(button)
                
                    
                    
                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertToDisplay, buttonText,)
                self._connectButtonClicked(button, slot)
                

                

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)
    
    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)
            # button.clicked.connect(self.display.clear)
        
        # Botao N retorna o numero negativo
            

        if text in '=':
            self._connectButtonClicked(button, self._eq)

        if text in 'Del':
            self._connectButtonClicked(button, self._backspace)
            button.setProperty('cssClass', 'backspaceButton')
            
                    
        if text in ['+', '-', '*', '/' , '^']:
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._configLeftOp, text)
                )


    @Slot()                   
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return
        
        number = convertToNumber(displayText) * -1
        self.display.setText(str(number))
    
    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitial
        self.display.clear()
        self.display.setFocus()
        
        
    @Slot()
    def _configLeftOp(self, text):# + - * /
        displayText = self.display.text() # Devera ser o meu numero _left
        self.display.clear() # Limpar o display
        self.display.setFocus() # Focar no display

        # Se a pessoa clicou no operador sem
        # configurar qualquer numero
        if not isValidNumber(displayText) and self._left is None:
            self._showError('Conta incompleta')
            return
            
        # Se houver algo no numero da esquerda,
        # nao fazemos nada. Aguararemos o numero da direita.

        if self._left is None:
            self._left =  convertToNumber(displayText)
            
        self._op = text
        self.equation = f'{self._left} {self._op} ??'


    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._op is None:
            self._showError('Conta incompleta')
            return
        
        if self._left is None:
            self._showError('Conta incompleta')
            return
        
        self._right =  convertToNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left,  float | int):
                result = math.pow(self._left, self._right)
                result = convertToNumber(str(result))
                
            
            else:
                result = eval(self.equation)
                

        except ZeroDivisionError:
            self._showError('Divisao por zero')

        except OverflowError:
            self._showError('Numero muito grande')         
            
        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self.display.insert(str(result))
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()


    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox
      
    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        #Mensagem da caixa de dialogo
        msgBox.setWindowTitle('Erro')
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        #Mensagem da caixa de dialogo
        msgBox.setWindowTitle('Info')
        msgBox.exec()
        self.display.setFocus()
        

       
