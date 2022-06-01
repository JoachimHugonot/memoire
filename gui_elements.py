from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from utils import pt_to_pixel


class Padding(QLabel):
    def __init__(self, height, config):
        super().__init__()
        self.setFixedHeight(height)

        self.setFont(config['FONT'])
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignCenter)


class Title(QLabel):
    def __init__(self, text, config):
        super().__init__()

        self.setText(text)
        self.setFont(config['FONT_TITLE'])
        self.setFixedHeight(170)
        color_str = 'rgb' + str(tuple(config['TITLE_COLOR']))
        self.setStyleSheet('margin-top: 100px; margin-bottom: 10px; color:' + color_str)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedWidth(int(config['WIDTH_PERCENTAGE'] * config['SCREEN_WIDTH']))


class Text(QLabel):
    def __init__(self, text, config):
        super().__init__()

        self.setText(text)

        self.setFont(config['FONT'])
        self.setWordWrap(True)

        n_lines = text.count('<br>') + text.count('<ol>') + text.count('<ul>') + text.count('<li>') + 1
        self.setFixedHeight(int(50 * n_lines + pt_to_pixel(config['LINE_HEIGHT']) / 100 * (n_lines - 1)))

        self.setFixedWidth(int(config['WIDTH_PERCENTAGE'] * config['SCREEN_WIDTH']))
        self.setAlignment(Qt.AlignCenter)
        color_str = 'rgb' + str(tuple(config['TEXT_COLOR']))
        self.setStyleSheet('color:' + color_str)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)


class Button(QPushButton):
    def __init__(self, text, color, config):
        super().__init__()
        self.setText(text),
        self.setFont(config['FONT'])

        color_str = 'color:rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
        self.setStyleSheet(color_str)

        self.setFixedWidth(int(config['WIDTH_PERCENTAGE'] * config['SCREEN_WIDTH']))

        self.setFixedWidth(500)

        self.setFixedHeight(30)
