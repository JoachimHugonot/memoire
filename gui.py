from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from cnn import *
import sys
import os
from urllib import request

global FONT, DELAY_FADE
FONT = QFont('Helvetica', 20)
DELAY_FADE = 333


class firstTab(QLabel):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Creation of the elements
        self.layout = QVBoxLayout()

        self.text_1 = QLabel('Imaginez vous en train d\'acheter un produit de beauté à la Coop...')
        self.text_1.setFont(FONT)

        self.image_1 = QPixmap('ASSETS/COOP.jpg')
        self.image_1 = self.image_1.scaledToWidth(1200)

        self.image_ph1 = QLabel()
        self.image_ph1.setPixmap(self.image_1)

        # Composition of the elements
        self.layout.addWidget(self.text_1, 1, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.image_ph1, 10, alignment=Qt.AlignCenter)
        self.layout.addWidget(QLabel(), 100)  # Padding
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        print('Click')
        event.accept()

    def keyPressEvent(self, event):
        print('Key')
        event.accept()


class secondTab(QLabel):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Creation of the elements
        self.main_layout = QVBoxLayout()
        self.fileselect_layout = QHBoxLayout()
        self.from_url_layout = QVBoxLayout()
        self.fileselect = QLabel()

        self.from_url_button = QPushButton('Télécharger depuis le lien')
        self.from_url_button.setFont(FONT)
        self.from_url_button.setFocusPolicy(Qt.NoFocus)
        self.from_url_button.clicked.connect(self.select_files_from_url)

        self.from_analyse_button = QPushButton('Analyser')
        self.from_analyse_button.setFont(FONT)
        self.from_analyse_button.setFocusPolicy(Qt.NoFocus)
        self.from_analyse_button.clicked.connect(self.analyse)

        self.from_url_edit = QTextEdit()

        self.from_url = QLabel()
        self.from_url.setLayout(self.from_url_layout)

        self.from_drive_button = QPushButton("Choisir un fichier sur l'ordinateur")
        self.from_drive_button.setFont(FONT)
        self.from_drive_button.clicked.connect(self.select_files)
        self.from_drive_button.setFocusPolicy(Qt.NoFocus)

        # Composition of the element
        self.fileselect.setLayout(self.fileselect_layout)

        self.from_url_layout.addWidget(self.from_url_edit)
        self.from_url_layout.addWidget(self.from_url_button)

        self.fileselect_layout.addWidget(self.from_drive_button, 3, alignment=Qt.AlignBottom)
        self.fileselect_layout.addWidget(QLabel(''), 1)  # padding
        self.fileselect_layout.addWidget(self.from_url, 3)

        self.image_ph = QLabel()

        self.main_layout.addWidget(self.fileselect, 1)
        self.main_layout.addWidget(self.image_ph, 5, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.from_analyse_button, 1)  # padding
        self.main_layout.addWidget(QLabel(''), 1)  # padding

        self.setLayout(self.main_layout)

    def select_files(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        print(type(file))
        if check:
            print(file)
            self.file_to_analyse = file
            self.image_ph.setPixmap(QPixmap(file))

    def analyse(self):
        image = instance_segmentation_api(self.file_to_analyse, 'temp2.png')
        from collections import Counter

        pixmap =QPixmap('temp2.png')

        # pixmap.scaledToWidth(1200)
        self.image_ph.setPixmap(pixmap)


    def select_files_from_url(self):

        fp = os.path.join(os.getcwd(), 'temp.jpg')
        request.urlretrieve(self.from_url_edit.toPlainText(), fp)
        pixmap = QPixmap(fp)
        self.file_to_analyse = fp
        # pixmap = pixmap.scaledToWidth(1200)

        self.image_ph.setPixmap(pixmap)

    def keyPressEvent(self, event):
        0

class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):

        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(DELAY_FADE)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


class StackedWidget(QStackedWidget):

    def __init__(self, parent = None):
        QStackedWidget.__init__(self, parent)

    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def set_page1(self):
        self.setCurrentIndex(0)
        w1.setFocus()

    def set_page2(self):
        self.setCurrentIndex(1)
        w2.setFocus()

    def set_page3(self):
        self.setCurrentIndex(2)
        editor3.setFocus()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(1500, 750)

    w1 = firstTab()
    w2 = secondTab()

    editor3 = QLabel()
    editor3.setText("Page 3 ! " * 100)
    editor3.setWordWrap(True)
    editor3.setFont(FONT)

    editor2 = QLabel()
    editor2.setText("Page 2 ! " * 100)
    editor2.setWordWrap(True)
    editor2.setFont(FONT)

    stack = StackedWidget()

    stack.addWidget(w1)
    stack.addWidget(w2)
    stack.addWidget(editor3)

    page1Button = QPushButton("Page 1")
    page1Button.setFocusPolicy(Qt.NoFocus)
    page2Button = QPushButton("Page 2")
    page2Button.setFocusPolicy(Qt.NoFocus)

    page3Button = QPushButton("Page 3")
    page3Button.setFocusPolicy(Qt.NoFocus)

    page1Button.setFont(FONT)
    page2Button.setFont(FONT)
    page3Button.setFont(FONT)

    page1Button.clicked.connect(stack.set_page1)
    page2Button.clicked.connect(stack.set_page2)
    page3Button.clicked.connect(stack.set_page3)

    layout = QGridLayout(window)
    layout.addWidget(stack, 0, 0, 1, 3)
    layout.addWidget(page1Button, 1, 0)
    layout.addWidget(page2Button, 1, 1)
    layout.addWidget(page3Button, 1, 2)


    window.showMaximized()
    w1.setFocus()

    window.setWindowIcon(QIcon('ASSETS/LOGO2.png'))

    sys.exit(app.exec_())
