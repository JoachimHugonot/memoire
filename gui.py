from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from cnn import *
import sys
import os
from urllib import request

global FONT, DELAY_FADE
FONT = QFont('Helvetica', 30)
DELAY_FADE = 333


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        formLayout = QVBoxLayout()
        groupBox = QGroupBox()



        groupBox.setLayout(formLayout)
        self.ELEMENTS = []
        self.scroll = QScrollArea()
        self.vsb = self.scroll.verticalScrollBar()
        self.scroll.setWidget(groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.horizontalScrollBar().setEnabled(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

        # Creation of the elements
        self.layout = QVBoxLayout()
        WIDGETS_ONE = [
            QPixmap('ASSETS/LOGO2.png'),
            QLabel('Imaginez vous en train d\'acheter un produit de beauté à la Coop...'),
            QPixmap('ASSETS/COOP.jpg'),
            QLabel('… vous réglez vos achats avec votre supercard.'),
            QPixmap('ASSETS/SUPER_CARD.PNG'),
            QLabel('Le magasin a donc votre historique d’achats.'),
            QLabel('Mais quel genre d’information l’enseigne peut-elle déduire à votre sujet? '),
            QLabel('Sur une échelle de 1 à 10, …, estimez à quel point l’achat d’une produit de beauté peut donner des informations personnelles à votre sujet'),
            QSlider(Qt.Horizontal),
            QPixmap('ASSETS/10.png'),
            QLabel('En effet en 2012, une chaîne d’hypermarché à appris qu’une adolescente était enceinte et ce avant même que le père soit au courant !'),
            QLabel('Les femmes enceintes achètent plus facilement des produits avec des parfums neutres.'),
            QLabel('Ce qu’a fait cette adolescente !'),
            QLabel("<a href=\"https://ladigitale.dev/digiread/#/a/6262819b4f474\">Le lien vers l'article</a>"),
            QLabel("Mais pourquoi ont-ils cherché à obtenir cette information ?"),
            QPixmap("ASSETS/MONEY.png"),
            QLabel("Les entreprises ne sont pas intéressées par nos informations personnelles mais bien par gagner de l’argent !"),
            QLabel("Target en estimant que l’adolescente était enceinte lui a envoyé des publicités pour des couches et des berceaux. Une carte de fidélité nous fait économiser des sous, mais nous donnons des informations en échanges qui seront utilisées par l’entreprise pour faire de la publicité ciblée"),
            QLabel("Comment ont-ils fait cela ?"),
            QLabel("Avec les données des historiques d’achats de ses clientes ! 2 millions de clients font leurs courses quotidiennement chez Target"),
            QLabel("C’est énormément de données à analyser, il n’est pas envisageable de les analyser à la main. Pensez-vous à quelque chose qui pourrait facilement analyser d’énormes quantités de données ?"),
            QPixmap("ASSETS/COMPUTER.png"),
            QLabel("Un ordinateur ! Plus spécifiquement en utilisant l’intelligence artificielle. Ces termes vous seront peut-être familiers :"),
            QLabel("I.A.(Intelligence artificielle)"),
            QLabel("Réseau de neurones / Neural networks"),
            QLabel("Deep learning / apprentissage en profondeur"),
            QLabel("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),

            QLabel("Avez-vous déjà effectué une recherche sur internet et vu une publicité en rapport immédiatement après ?"),
            QLabel("Comment Google et Facebook gagnent t-ils de l’argent ? Avec la publicité, notre profil est transmis à des entreprises qui payent google pour nous afficher de la publicité. "),
            QLabel("Google et Facebook ne sont pas des entreprises qui font des logiciels, mais bien des entreprises de publicité, qui est la première source de leurs revenus"),
            QLabel("Nos ordinateurs sont désormais capables d’analyser automatiquement les photos et les vidéos grâce à l’intelligence artificielle"),
            QLabel("Qui a accès à vos photos/vidéos et à le droit de les utiliser afin d’en tirer des informations vous concernant ? Probablement tous les services que vous utilisez sur vos smartphones"),
            QLabel("Un simple achat d’un produit de beauté peut permettre à un inconnu de savoir si vous êtes enceinte. Maintenant imaginez ce que les géants du domaine (Google et Facebook) savent sur vous. "),
            QLabel("La gratuité de votre expérience sur vos smartphones à un coût"),
            secondTab(),
            #QLabel("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),
            #QLabel("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),

        ]


        for widget in WIDGETS_ONE:
            if type(widget) == QLabel:
                #widget.setWordWrap(True)
                widget.setFont(FONT)
                widget.setFixedHeight(150)
                widget.setFixedWidth(1200)
                #widget.setWidgetResizable(False)
                widget.setWordWrap(True)
                widget.setAlignment(Qt.AlignCenter)
                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)
                if "href" in widget.text():
                    widget.setTextFormat(Qt.RichText)
                    widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
                    widget.setOpenExternalLinks(True)
            elif type(widget) == QPixmap:
                print('Pixmap')
                image_ph = QLabel()
                widget = widget.scaledToHeight(500)
                image_ph.setPixmap(widget)



                self.ELEMENTS.append(image_ph)
                formLayout.addWidget(image_ph, alignment=Qt.AlignCenter)
            elif type(widget) == QSlider:
                widget.setMinimum(1)
                widget.setMaximum(10)
                widget.setFixedWidth(1200)
                widget.setFixedHeight(150)
                widget.setTickInterval(1)

                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)
            elif type(widget) == secondTab:
                widget.setFixedWidth(1200)
                widget.setFixedHeight(900)
                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)




        for el in self.ELEMENTS:
            el.hide()


    def mousePressEvent(self, event):
        print('Click')
        event.accept()

    def keyPressEvent(self, event):
        print('Key')
        if Qt.Key_N:
            for el in self.ELEMENTS:
                if not el.isVisible():
                    el.show()
                    break
            print(self.vsb.maximum())
            self.vsb.setValue(self.vsb.maximum() + 200)
            QTimer.singleShot(0, self.handle_timeout)

    def handle_timeout(self):
        x = self.vsb.maximum()
        self.vsb.setValue(x)

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
        self.grid_layout = QGridLayout()

        #self.fileselect_layout = QHBoxLayout()
        #self.from_url_layout = QVBoxLayout()
        self.fileselect = QLabel()
        self.fileselect.setLayout(self.grid_layout)

        self.from_url_button = QPushButton('Télécharger depuis le lien')
        self.from_url_button.setFont(FONT)
        self.from_url_button.setFocusPolicy(Qt.NoFocus)
        self.from_url_button.clicked.connect(self.select_files_from_url)

        self.from_analyse_button = QPushButton('Analyser')
        self.from_analyse_button.setFont(FONT)
        self.from_analyse_button.setFocusPolicy(Qt.NoFocus)
        self.from_analyse_button.clicked.connect(self.analyse)

        self.from_url_edit = QTextEdit()

        #self.from_url = QLabel()
        #self.from_url.setLayout(self.from_url_layout)

        self.from_drive_button = QPushButton("Choisir un fichier sur l'ordinateur")
        self.from_drive_button.setFont(FONT)
        self.from_drive_button.clicked.connect(self.select_files)
        self.from_drive_button.setFocusPolicy(Qt.NoFocus)

        # Composition of the element
        #self.fileselect.setLayout(self.fileselect_layout)

        self.grid_layout.addWidget(self.from_url_edit, 0, 1)
        self.grid_layout.addWidget(self.from_url_button, 1, 1)
        self.grid_layout.addWidget(self.from_drive_button, 1, 0)


        #self.fileselect_layout.addWidget(self.from_drive_button, 3, alignment=Qt.AlignBottom)
        #self.fileselect_layout.addWidget(QLabel(''), 1)  # padding
       # self.fileselect_layout.addWidget(self.from_url, 3)

        self.image_ph = QLabel()

        self.main_layout.addWidget(self.fileselect, 1)
        self.main_layout.addWidget(self.image_ph, 5, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.from_analyse_button, 1)  # padding
        #self.main_layout.addWidget(QLabel(''), 1)  # padding

        self.setLayout(self.main_layout)

    def select_files(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        print(type(file))
        if check:
            print(file)
            self.file_to_analyse = file
            pm = QPixmap(file)
            pm = pm.scaledToHeight(600)
            self.image_ph.setPixmap(pm)

    def analyse(self):
        image = instance_segmentation_api(self.file_to_analyse, 'temp2.png')
        from collections import Counter

        pm =QPixmap('temp2.png')
        pm = pm.scaledToHeight(600)
        # pixmap.scaledToWidth(1200)
        self.image_ph.setPixmap(pm)


    def select_files_from_url(self):

        fp = os.path.join(os.getcwd(), 'temp.jpg')
        request.urlretrieve(self.from_url_edit.toPlainText(), fp)
        pm = QPixmap(fp)
        pm = pm.scaledToHeight(600)
        self.file_to_analyse = fp
        # pixmap = pixmap.scaledToWidth(1200)

        self.image_ph.setPixmap(pm)

    def keyPressEvent(self, event):
        0

class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):

        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        #self.timeline = QTimeLine()
        #self.timeline.valueChanged.connect(self.animate)
        #self.timeline.finished.connect(self.close)
        #self.timeline.setDuration(DELAY_FADE)
        #self.timeline.start()

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
        #self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def set_page1(self):
        self.setCurrentIndex(0)
        w1.setFocus()

    def set_page2(self):
        self.setCurrentIndex(1)
        w2.setFocus()

    def set_page3(self):
        self.setCurrentIndex(2)
        w3.setFocus()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(1500, 750)

    w1 = firstTab()
    w2 = secondTab()
    w3 = MainWindow()



    stack = StackedWidget()

    stack.addWidget(w3)
    stack.addWidget(w2)
    stack.addWidget(w1)

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
    app.setWindowIcon(QIcon('ASSETS/LOGO2.png'))

    sys.exit(app.exec_())
