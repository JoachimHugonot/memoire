# Core imports
import sys
import os
import urllib
from urllib import request

# Project imports
from cnn import *

# 3rd parties imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

global FONT, DELAY_FADE,ELEMENT_BY_ELEMENT, IMAGE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, WIDTH_PERCENTAGE
ELEMENT_BY_ELEMENT = False

def pixel_to_pt(pixel):
    return int(pixel * 12 / 16)

FONT = QFont('Helvetica', pixel_to_pt(30))
FONT_TITLE = QFont('Helvetica', pixel_to_pt(50))
IMAGE_HEIGHT = 600
WIDTH_PERCENTAGE = 0.8
class Padding(QLabel):
    def __init__(self, height):
        super().__init__()
        self.setMinimumHeight(height)

class Title(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setFont(FONT_TITLE)
        self.setFixedHeight(260)
        self.setStyleSheet('margin-top: 200px; margin-bottom: 10px;')
        print(int(WIDTH_PERCENTAGE * SCREEN_WIDTH))
        self.setFixedWidth(int(WIDTH_PERCENTAGE * SCREEN_WIDTH))

class Text(QLabel):
    def __init__(self, text):
        super().__init__()
        #self.layout = QHBoxLayout()
        #self.setLayout(self.layout)

        self.setText(text)
        self.setFont(FONT)
        self.setWordWrap(True)

        self.setFixedHeight(120)
        self.setFixedWidth(int(WIDTH_PERCENTAGE * SCREEN_WIDTH))
        #self.label.setStyleSheet("line-height: 2.5;")
        #image_ph = QLabel()
        #widget = QPixmap('ASSETS/LOGO.PNG').scaledToHeight(200)
        #image_ph.setPixmap(widget)
        #self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        #self.layout.addWidget(image_ph,1)



        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)



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
            Padding(300),
            Title('Que peuvent révéler mes données ?'),
            QPixmap('ASSETS/LOGO2.png'),
            Text('Imaginez vous en train d\'acheter un produit de beauté à la Coop...'),
            QPixmap('ASSETS/COOP.jpg'),
            Text('… vous réglez vos achats avec votre supercard.'),
            QPixmap('ASSETS/SUPER_CARD.PNG'),
            Text('Le magasin a donc votre historique d’achats.'),
            Title('Mais quel genre d’information l’enseigne peut-elle déduire à votre sujet? '),
            Text('Sur une échelle de 1 à 10, …, estimez à quel point l’achat d’une produit de beauté peut donner des informations personnelles à votre sujet'),
            QSlider(Qt.Horizontal),
            QPixmap('ASSETS/10.png'),
            Text('En effet en 2012, une chaîne d’hypermarché à appris qu’une adolescente était enceinte et ce avant même que le père soit au courant !'),
            Text('Les femmes enceintes achètent plus facilement des produits avec des parfums neutres.'),
            Text('Ce qu’a fait cette adolescente !'),
            Text("<a href=\"https://ladigitale.dev/digiread/#/a/6262819b4f474\">Le lien vers l'article</a>"),
            Title("Mais pourquoi ont-ils cherché à obtenir cette information ?"),
            QPixmap("ASSETS/MONEY.png"),
            Text("Les entreprises ne sont pas intéressées par nos informations personnelles mais bien par gagner de l’argent !"),
            Text("Target en estimant que l’adolescente était enceinte lui a envoyé des publicités pour des couches et des berceaux."),
            Text("Une carte de fidélité nous fait économiser des sous, mais nous donnons des informations en échanges qui seront utilisées par l’entreprise pour faire de la publicité ciblée"),
            Padding(50),
            Title("Comment ont-ils fait cela ?"),
            Text("Avec les données des historiques d’achats de ses clientes ! 2 millions de clients font leurs courses quotidiennement chez Target"),
            Text("C’est énormément de données à analyser, il n’est pas envisageable de les analyser à la main."),
            Text("Pensez-vous à quelque chose qui pourrait facilement analyser d’énormes quantités de données ?"),
            QPixmap("ASSETS/COMPUTER.png"),
            Text("Un ordinateur ! Plus spécifiquement en utilisant l’intelligence artificielle."),
            Text(" Ces termes vous seront peut-être familiers :<ul>"
                 "<li>I.A.(Intelligence artificielle)</li>"
                    "<li>Réseau de neurones / Neural networks</li>"
                    "<li>Deep learning / apprentissage en profondeur</li>"
                 "</ul>"),
            Text("Réseau de neurones / Neural networks"),
            Text("Deep learning / apprentissage en profondeur"),
            Text("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),
            Text("Avez-vous déjà effectué une recherche sur internet et vu une publicité en rapport immédiatement après ?"),
            Text("Comment Google et Facebook gagnent t-ils de l’argent ? Avec la publicité, notre profil est transmis à des entreprises qui payent google pour nous afficher de la publicité. "),
            Text("Google et Facebook ne sont pas des entreprises qui font des logiciels, mais bien des entreprises de publicité, qui est la première source de leurs revenus"),
            Text("Nos ordinateurs sont désormais capables d’analyser automatiquement les photos et les vidéos grâce à l’intelligence artificielle"),
            Text("Qui a accès à vos photos/vidéos et à le droit de les utiliser afin d’en tirer des informations vous concernant ? Probablement tous les services que vous utilisez sur vos smartphones"),
            Text("Un simple achat d’un produit de beauté peut permettre à un inconnu de savoir si vous êtes enceinte."),

            Text("Maintenant imaginez ce que les géants du domaine (Google et Facebook) savent sur vous. "),
            Text("La gratuité de votre expérience sur vos smartphones à un coût"),
            secondTab(),
            #QLabel("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),
            #QLabel("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),

        ]
        for widget in WIDGETS_ONE:
            if type(widget) == Text or type(widget) == Title:
                #widget.setWordWrap(False)
                #widget.setAlignment(Qt.AlignCenter)
                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignLeft)


            elif type(widget) == QPixmap:
                image_ph = QLabel()
                widget = widget.scaledToHeight(200)
                image_ph.setPixmap(widget)
                self.ELEMENTS.append(image_ph)
                formLayout.addWidget(image_ph, alignment=Qt.AlignCenter)


            elif type(widget) == QSlider:
                widget.setMinimum(1)
                widget.setMaximum(10)
                widget.setFixedWidth(1200)
                widget.setFixedHeight(20)
                widget.setTickInterval(1)

                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)
            elif type(widget) == secondTab:
                widget.setFixedWidth(1200)
                widget.setFixedHeight(900)
                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)
            elif type(widget) == Padding:
                # widget.setWordWrap(True)
                widget.setFont(FONT)
                widget.setFixedHeight(50)
                # widget.setFixedWidth(1600)
                print(widget.size())
                print(widget.minimumSize())
                widget.setWordWrap(True)
                print(widget.size())
                print(widget.minimumSize())
                widget.setAlignment(Qt.AlignCenter)
                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)
                if "href" in widget.text():
                    widget.setTextFormat(Qt.RichText)
                    widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
                    widget.setOpenExternalLinks(True)


        for el in self.ELEMENTS:
            if ELEMENT_BY_ELEMENT :
                el.hide()
            else:
                if type(el) == Text:
                    print(QFontMetrics(FONT).boundingRect(el.text()))
        print('_')



    def mousePressEvent(self, event):
        event.accept()

    def keyPressEvent(self, event):
        if Qt.Key_N:
            for el in self.ELEMENTS:
                if not el.isVisible():
                    el.show()
                    break
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
        event.accept()

    def keyPressEvent(self, event):
        event.accept()


class secondTab(QLabel):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.file_to_analyse = None
        self.file_to_analyse_pixmap = None
        self.file_analysed = None
        self.file_analysed_pixmap = None

        # Creation of the elements
        self.main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.image_area_layout = QGridLayout()

        self.image_area = QLabel('ABC')
        self.image_area.setLayout(self.image_area_layout)
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

        self.show_hide_button = QPushButton('Montrer / Cacher les résultats')
        self.show_hide_button.setFont(FONT)
        self.show_hide_button.setFocusPolicy(Qt.NoFocus)
        self.show_hide_button.clicked.connect(self.show_hide)
        self.show_hide_button.setEnabled(False)

        self.from_url_edit = QTextEdit()

        self.from_drive_button = QPushButton("Choisir un fichier sur l'ordinateur")
        self.from_drive_button.setFont(FONT)
        self.from_drive_button.clicked.connect(self.select_files)
        self.from_drive_button.setFocusPolicy(Qt.NoFocus)

        # Composition of the element
        self.grid_layout.addWidget(QLabel(''), 0, 0)
        self.grid_layout.addWidget(self.from_url_edit, 1, 1)
        self.grid_layout.addWidget(self.from_url_button, 2, 1)
        self.grid_layout.addWidget(self.from_drive_button, 2, 0)

        self.image_ph = QLabel()

        self.main_layout.addWidget(self.fileselect, 1)
        self.main_layout.addWidget(self.image_ph, 5, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.from_analyse_button, 1)  # padding
        self.main_layout.addWidget(self.show_hide_button, 1)  # padding
        #self.main_layout.addWidget(QLabel(''), 1)  # padding

        self.setLayout(self.main_layout)

    def show_hide(self):
        if self.displaying_results:
            self.displaying_results = False
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)

        else:
            self.displaying_results = True
            self.image_ph.setPixmap(self.file_analysed_pixmap)


    def select_files(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "Image Files (*.png *.jpg *.bmp *.jpeg)")
        if check:
            self.file_to_analyse = cv2.imread(file)
            self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
            self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(IMAGE_HEIGHT)
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        return QPixmap.fromImage(convert_to_Qt_format)

    def analyse(self):
        self.file_analysed, SEEN, COLORS = instance_segmentation_api(self.file_to_analyse, 'temp2.png')
        print(SEEN)
        print(COLORS)
        print(type(self.file_analysed))
        from collections import Counter

        self.file_analysed_pixmap = self.convert_cv_qt(self.file_analysed)
        self.file_analysed_pixmap = self.file_analysed_pixmap.scaledToHeight(IMAGE_HEIGHT)
        self.image_ph.setPixmap(self.file_analysed_pixmap)

        self.show_hide_button.setEnabled(True)
        self.displaying_results = True


    def select_files_from_url(self):

        try:
            req = urllib.request.urlopen(self.from_url_edit.toPlainText())
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)
            self.file_to_analyse = img

            self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
            self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(IMAGE_HEIGHT)
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)
        except:
            self.from_url_edit.setText('Invalid URL')

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
    SCREEN_WIDTH = app.primaryScreen().size().width()
    SCREEN_HEIGHT = app.primaryScreen().size().height()


    window = QWidget()
    #window.resize(1500, 750)

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
    #layout.addWidget(page1Button, 1, 0)
    #layout.addWidget(page2Button, 1, 1)
    #layout.addWidget(page3Button, 1, 2)


    window.showMaximized()


    w1.setFocus()

    app.setWindowIcon(QIcon('ASSETS/LOGO2.png'))

    sys.exit(app.exec_())
