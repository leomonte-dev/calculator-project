# QSS - Estilos do QT for Python
# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
# Dark Theme
# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html
import qdarktheme
from variables import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR, YELLOW_COLOR, GOLD_COLOR, RED_COLOR,
                       DARKED_RED_COLOR, CRIMSON_COLOR)

qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}


    QPushButton[cssClass="nButton"]:hover {{
        background: {YELLOW_COLOR};
    }}
    QPushButton[cssClass="nButton"]:pressed {{
        color: #FF7F50;
        background: #FF7F50;
    }}
    QPushButton[cssClass="nButton"] {{
        color: black;
        background: {GOLD_COLOR};
    }}

    

    QPushButton[cssClass="backspaceButton"] {{
        background: {CRIMSON_COLOR};
        text-align: center;
        color: black;
    }}
    QPushButton[cssClass="backspaceButton"]:hover {{
        background: {RED_COLOR};
    }}
    QPushButton[cssClass="backspaceButton"]:pressed {{
        color: {DARKED_RED_COLOR};
        background: {DARKED_RED_COLOR};
    }}



"""


def setupTheme():
    qdarktheme.setup_theme(
        theme='dark',
        corner_shape='rounded',
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=qss
    )