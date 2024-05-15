from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QKeyEvent
from variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from PySide6.QtCore import Qt, Signal
from utils import isEmpty, isNumrOrDot

class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
    
    def configStyle(self):
        self.setStyleSheet(f'''background-color: white; 
                           color: black; 
                           font-size: {BIG_FONT_SIZE}px; 
                           border: 1px solid black; 
                           border-radius: 5px; 
                           padding: 5px;
                           ''')
        
        self.setMinimumHeight(BIG_FONT_SIZE)
        self.setMinimumWidth(MINIMUM_WIDTH - 180 )
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN]*4)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [
            KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Asterisk, KEYS.Key_Slash,
            KEYS.Key_P
        ]

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
    
        if isDelete:
            self.delPressed.emit()
            return event.ignore()
    
        if isEsc:
            self.clearPressed.emit()
            return event.ignore()
        
        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()
                
        # Nao passar daqui se nao tiver texto
        if isEmpty(text):
            return event.ignore()

        if isNumrOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()
