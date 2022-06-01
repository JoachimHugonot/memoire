# Core imports
import sys
import os
import urllib
from urllib import request
import json
import cv2

# Project imports
from cnn import *
from utils import pixel_to_pt
from gui_elements import Padding, Title, Text, Button

# 3rd parties imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MasterWidget(QWidget):
    def press(self):
        self.but1.setFlat(False)
        self.but2.setFlat(False)
        self.but3.setFlat(False)
        self.sender().setFlat(True)

        for idx, el in enumerate(self.ELEMENTS):
            if not el.isVisible():
                el.show()
                if idx != len(self.ELEMENTS) - 1 and type(self.ELEMENTS[idx + 1]) in [Title]:
                    break
        QTimer.singleShot(100, self.handle_timeout)

        self.but1.setDisabled(True)
        self.but2.setDisabled(True)
        self.but3.setDisabled(True)

        self.STEP_COUNTER += 1

    def __init__(self, config):
        super().__init__()
        self.CONFIG = config

        form_layout = QVBoxLayout()
        group_box = QLabel()
        group_box.setLayout(form_layout)

        self.ELEMENTS = []
        self.scroll = QScrollArea()

        self.vsb = self.scroll.verticalScrollBar()
        self.scroll.setWidget(group_box)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.horizontalScrollBar().setEnabled(False)
        self.scroll.setStyleSheet('background:lightgrey')

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)

        self.STEP_COUNTER = 0
        self.but1 = Button('Non, pas du tout', (0, 175, 0), self.CONFIG)
        self.but2 = Button('Un peu, rien d\'important', (175, 127, 0), self.CONFIG)
        self.but3 = Button('Oui, beaucoup trop', (175, 0, 0), self.CONFIG)

        self.but1.clicked.connect(self.press)
        self.but2.clicked.connect(self.press)
        self.but3.clicked.connect(self.press)

        # Creation of the elements
        self.layout = QVBoxLayout()
        WIDGETS_ONE = [
            Title('1 - Que disent mes données sur moi ?', self.CONFIG),
            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">Vous êtes en train d\'acheter un shampoing.<br>'
                                         'Vous réglez vos achats avec votre carte de fidélité.<br>'
                                         'Le magasin a donc accès à votre historique d’achats.</p>', self.CONFIG),
            Padding(5, self.CONFIG),
            QPixmap('./ASSETS/LOYALTY_CARD.png'),

            Title('2 - Que sait le magasin sur vous ?', self.CONFIG),
            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">Le magasin sait quel shampoing vous venez d\'acheter.<br>'
                                         "Est-ce que vous pensez que cette information personelle révèle beaucoup à votre sujet ?</p>",
                 self.CONFIG),
            self.but1,
            self.but2,
            self.but3,
            Padding(10, self.CONFIG),

            Title('3 - Un simple achat peut en dire beaucoup sur vous !', self.CONFIG),
            Text('<p style="line-height:' + str(
                CONFIG[
                    'LINE_HEIGHT']) + ';">La bonne réponse est <span style=\"color:rgb(175,0,0)\">Oui, beaucoup trop</span>  </p><br>'
                                      'En 2012, un magasin a appris qu’une adolescente était enceinte avant que sa famille ne l\'apprenne.<br>'
                                      'Elle a juste acheté un shampoing sans parfum et le magasin en a déduit qu\'elle était enceinte.<br>'
                                      'En effet, les femmes enceintes préfèrent acheter des produits sans parfum.<br>'
                                      '<a href=\"https://ladigitale.dev/digiread/#/a/6262819b4f474\">Je veux en savoir plus</a><br>'

                 , self.CONFIG),
            Padding(5, self.CONFIG),
            QPixmap('./ASSETS/SHAMPOO.png'),
            # QPixmap("ASSETS/MONEY.png"),
            Title("4 - Pourquoi les entreprises veulent mes données ?", self.CONFIG),
            Text('<p style="line-height:' + str(
                CONFIG[
                    'LINE_HEIGHT']) + ';">Les entreprises gagnent de l\'argent avec vos informations personnelles<br>'
                                      'Le magasin les a utilisées pour personnaliser la publicité envoyée à l\'adolescente : des couches et des berceaux.<br>'
                                      'Une carte de fidélité nous fait économiser de l\'argent, mais en échange, nous payons avec nos informations personelles...<br>'
                                      '... afin que les entreprises gagnent encore plus d\'argent !</p>', self.CONFIG),
            Padding(5, self.CONFIG),
            QPixmap("./ASSETS/MONEY.png"),
            Title("5 - Comment est-ce possible ?", self.CONFIG),
            Text('<p style="line-height:' + str(
                CONFIG[
                    'LINE_HEIGHT']) + ';">Grâce à l\'historique d\'achats de ses 2 millions de clients quotidiens.<br>'
                                      'Un humain ne peut pas analyser toutes ces données à la main. Un ordinateur, oui.<br>'
                                      'Avez-vous déjà entendu parler d\'intelligence artificielle, de réseaux de neurones ou de deep learning ? <br>'
                                      'C\'est ce qui permet aux entreprises de transformer vos données en argent.</p>',
                 self.CONFIG),

            QPixmap("./ASSETS/COMPUTER.png"),
            Title('6 - Un réseau de neurones ? Essayez !', self.CONFIG),
            Text('<p style="line-height:' + str(
                CONFIG[
                    'LINE_HEIGHT']) + ';">Maintenant, vous allez analyser des photos avec un réseau de neurones. <br>'
                                      'N\'hésitez pas à analyser vos photos personelles : nous garantissons que nous ne gardons aucune image.</p>',
                 self.CONFIG),

            AIPanel(self.CONFIG),
            # Title("7 - Et alors ?"),
            # Text('<p style="line-height:'+str(line_height)+';">TODO <br>'
            #      "Photo analysée + problématique<br>"
            #      "Sur le marché du travail dans quelques années<br>"
            #      "Navigation privée + nom/prénom<br>"
            #      "Les services que vous utilisez peuvent utiliser, vos informations. Optionellement lien prochaine partie </p>"
            #      ),
            # Title("Vos informations"),
            # Text('<p style="line-height:'+str(line_height)+';">Avez-vous déjà effectué une recherche sur un moteur de recherche et vu une publicité en rapport immédiatement après ?<br>'
            #      'Savez-vous comment Google (et Facebook) gagnent t-ils de l’argent ? <br>'
            #   'Avec la publicité<br>'
            #  'notre profil est transmis à des entreprises qui payent Google pour nous afficher de la publicité.<br>'
            #      'Google et Facebook ne sont pas des entreprises qui développent des logiciels, mais bien des entreprises de publicité<br>'
            #      'En 2021, le chiffre d\'affaires de Google a été de 257 milliards, 80% de ces revenus proviennent de la publicité</p>')
            #
            #

            # Text('Nos ordinateurs sont désormais capables d’analyser automatiquement les photos et les vidéos grâce à l’intelligence artificielle'),
            # Text('Qui a accès à vos photos/vidéos et à le droit de les utiliser afin d’en tirer des informations vous concernant ? Probablement tous les services que vous utilisez sur vos smartphones'),
            # Text('Un simple achat d’un produit de beauté peut permettre à un inconnu de savoir si vous êtes enceinte.'),

            # Text("Maintenant imaginez ce que les géants du domaine (Google et Facebook) savent sur vous. "),
            # Text("La gratuité de votre expérience sur vos smartphones à un coût"),

            # QLabel("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),
            # QLabel("Ces algorithmes peuvent analyser une très grande quantité de données afin d’en tirer des informations précieuses"),

        ]
        for widget in WIDGETS_ONE:

            # if type(widget) == Text or type(widget) == Title:
            #     # widget.setWordWrap(False)
            #     # widget.setAlignment(Qt.AlignCenter)
            if type(widget) != QPixmap:
                self.ELEMENTS.append(widget)
                form_layout.addWidget(widget, alignment=Qt.AlignCenter)

            if type(widget) == QPixmap:
                image_ph = QLabel()
                widget = widget.scaledToHeight(200)
                image_ph.setPixmap(widget)
                self.ELEMENTS.append(image_ph)
                form_layout.addWidget(image_ph, alignment=Qt.AlignCenter)

            elif type(widget) == AIPanel:
                widget.setFixedWidth(1200)
                widget.setFixedHeight(900)
                # self.ELEMENTS.append(widget)
                # formLayout.addWidget(widget, alignment=Qt.AlignCenter)
            # elif type(widget) == Button:
            #
            #     self.ELEMENTS.append(widget)
            #     formLayout.addWidget(widget, alignment=Qt.AlignCenter)
            # elif type(widget) == Padding:
            #
            #     self.ELEMENTS.append(widget)
            #     formLayout.addWidget(widget, alignment=Qt.AlignCenter)

            # if "href" in widget.text():
            #     widget.setTextFormat(Qt.RichText)
            #     widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
            #     widget.setOpenExternalLinks(True)

        for el in self.ELEMENTS:
            if self.CONFIG['DEBUG']:
                el.hide()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSizeConstraint(QLayout.SetFixedSize)

    def mousePressEvent(self, event):
        event.accept()

    def keyPressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if Qt.Key_N == event.key():
            if self.STEP_COUNTER != 2:

                for idx, el in enumerate(self.ELEMENTS):
                    if not el.isVisible():

                        el.show()

                        if idx != len(self.ELEMENTS) - 1 and type(self.ELEMENTS[idx + 1]) in [Title]:
                            break
                # self.vsb.setValue(self.vsb.maximum() + 200)
                QTimer.singleShot(100, self.handle_timeout)
                self.STEP_COUNTER += 1
        if Qt.Key_W == event.key() and modifiers == Qt.ControlModifier:
            sys.exit()

    def handle_timeout(self):
        x = self.vsb.maximum()
        self.vsb.setValue(x + 200)


class AIPanel(QLabel):
    def webcam_feed(self):
        vid = cv2.VideoCapture(0)

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        if ret:
            self.file_to_analyse = frame
            self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
            self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(CONFIG['IMAGE_HEIGHT'])
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)
            self.displaying_results = False
            self.labels_ph.setText('')
            self.show_hide_button.setEnabled(False)

            # After the loop release the cap object
            vid.release()
            # Destroy all the windows
            cv2.destroyAllWindows()

    def __init__(self, config, parent=None):
        QWidget.__init__(self, parent)
        self.CONFIG = config

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

        self.from_url_button = QPushButton('Télécharger depuis un lien')
        self.from_url_button.setFont(self.CONFIG['FONT'])
        self.from_url_button.setFocusPolicy(Qt.NoFocus)
        self.from_url_button.clicked.connect(self.select_files_from_url)

        self.from_analyse_button = QPushButton('Analyser')
        self.from_analyse_button.setFont(self.CONFIG['FONT'])
        self.from_analyse_button.setFocusPolicy(Qt.NoFocus)
        self.from_analyse_button.clicked.connect(self.analyse)

        self.show_hide_button = QPushButton('Voir l\'image')
        self.show_hide_button.setFont(self.CONFIG['FONT'])
        self.show_hide_button.setFocusPolicy(Qt.NoFocus)
        self.show_hide_button.clicked.connect(self.show_hide)
        self.show_hide_button.setEnabled(False)

        self.webcam_button = QPushButton('Webcam')
        self.webcam_button.setFont(self.CONFIG['FONT'])
        self.webcam_button.setFocusPolicy(Qt.NoFocus)
        self.webcam_button.clicked.connect(self.webcam_feed)

        self.from_url_edit = QTextEdit()

        self.from_drive_button = QPushButton("Choisir un fichier sur l'ordinateur")
        self.from_drive_button.setFont(self.CONFIG['FONT'])
        self.from_drive_button.clicked.connect(self.select_files)
        self.from_drive_button.setFocusPolicy(Qt.NoFocus)

        # Composition of the element
        self.grid_layout.addWidget(QLabel(''), 0, 0)
        self.grid_layout.addWidget(self.from_url_edit, 1, 1)
        self.grid_layout.addWidget(self.from_url_button, 2, 1)
        self.grid_layout.addWidget(self.from_drive_button, 2, 0)
        self.grid_layout.addWidget(self.webcam_button, 2, 2)

        self.from_url_edit.setFixedWidth(int(self.CONFIG['SCREEN_WIDTH'] * self.CONFIG['WIDTH_PERCENTAGE'] / 3.0))
        self.from_url_button.setFixedWidth(int(self.CONFIG['SCREEN_WIDTH'] * self.CONFIG['WIDTH_PERCENTAGE'] / 3.0))
        self.from_drive_button.setFixedWidth(int(self.CONFIG['SCREEN_WIDTH'] * self.CONFIG['WIDTH_PERCENTAGE'] / 3.0))
        self.webcam_button.setFixedWidth(int(self.CONFIG['SCREEN_WIDTH'] * self.CONFIG['WIDTH_PERCENTAGE'] / 3.0))

        self.from_url_edit.setFixedHeight(60)
        self.from_url_edit.setStyleSheet('background:white')
        self.from_url_button.setFixedHeight(40)
        self.webcam_button.setFixedHeight(40)

        self.from_drive_button.setFixedHeight(40)

        self.grid_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.IMAGE_PH = QLabel('abc')
        self.IMAGE_PH_LAYOUT = QHBoxLayout()
        self.IMAGE_PH.setLayout(self.IMAGE_PH_LAYOUT)

        self.image_ph = QLabel()
        self.image_ph.setFixedHeight(600)

        self.labels_ph = QLabel()
        self.labels_ph.setFont(self.CONFIG['FONT_TITLE'])
        self.labels_ph.setAlignment(Qt.AlignCenter)
        self.labels_ph.setFixedHeight(50)

        self.fileselect.setFixedHeight(60)
        self.main_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.main_layout.addWidget(self.fileselect, 1)
        self.main_layout.addWidget(self.image_ph, 5, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.labels_ph, 1)  # padding
        self.main_layout.addWidget(self.from_analyse_button, 1)  # padding
        self.main_layout.addWidget(self.show_hide_button, 1)  # padding

        self.displaying_results = False
        self.setLayout(self.main_layout)
        self.file_to_analyse = cv2.imread('SAMPLES/01.jpeg')
        self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
        self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(CONFIG['IMAGE_HEIGHT'])
        self.image_ph.setPixmap(self.file_to_analyse_pixmap)

        self.SEEN = None
        self.COLORS = None
        self.message = None
        self.pixmap_opacity = None

    def show_hide(self):
        if self.displaying_results:
            self.displaying_results = False
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)
            self.show_hide_button.setText('Voir les résultats')

        else:
            self.displaying_results = True
            self.image_ph.setPixmap(self.file_analysed_pixmap)

            labels = []
            if not self.SEEN:
                self.SEEN.append('L\'algorithme n\'a rien trouvé !')
                self.COLORS.append([0, 0, 0])

            for a in zip(self.SEEN, self.COLORS):
                lab, col = a
                col = [col[2], col[1], col[0]]
                color_s = 'rgb' + str(tuple(col))
                s = '<span style ="color:' + color_s + '"> ' + lab + '</span>'
                labels.append(s)
            labels = ' '.join(labels)

            self.labels_ph.setText(labels)
            self.setWordWrap(True)
            self.labels_ph.setFixedHeight(60)
            self.show_hide_button.setText('Voir l\'image')

    def select_files(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "./SAMPLES", "Image Files (*.png *.jpg *.bmp *.jpeg)")

        if os.path.exists(file):
            image = cv2.imread(file)
            if image is not None:
                self.file_to_analyse = image

                self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
                self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(CONFIG['IMAGE_HEIGHT'])
                self.image_ph.setPixmap(self.file_to_analyse_pixmap)

                self.displaying_results = False
                self.labels_ph.setText('')
                self.show_hide_button.setEnabled(False)

    @staticmethod
    def convert_cv_qt(cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        return QPixmap.fromImage(convert_to_Qt_format)

    def handle_t(self):
        self.file_analysed, self.SEEN, self.COLORS = instance_segmentation_api(self.file_to_analyse)

        self.file_analysed_pixmap = self.convert_cv_qt(self.file_analysed)
        self.file_analysed_pixmap = self.file_analysed_pixmap.scaledToHeight(CONFIG['IMAGE_HEIGHT'])
        self.show_hide()

        self.show_hide_button.setEnabled(True)
        self.message.close()

    def analyse(self):
        self.message = QMessageBox()
        self.message.setWindowFlags(Qt.FramelessWindowHint)
        self.message.setIcon(QMessageBox.Information)
        self.message.setText('Analyse de la photo')
        self.message.show()

        QTimer.singleShot(100, self.handle_t)

    def select_files_from_url(self):

        try:
            req = urllib.request.urlopen(self.from_url_edit.toPlainText())
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)
            self.file_to_analyse = img

            self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
            self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(CONFIG['IMAGE_HEIGHT'])
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)
            self.displaying_results = False
            self.labels_ph.setText('')
            self.show_hide_button.setEnabled(False)
        except:
            self.from_url_edit.setText('Invalid URL')

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    CONFIG = json.load(open('config.json'))
    CONFIG['FONT'] = QFont('Helvetica', pixel_to_pt(CONFIG['TEXT_SIZE']))
    CONFIG['FONT_TITLE'] = QFont('Helvetica', pixel_to_pt(CONFIG['TITLE_SIZE']))
    CONFIG['SCREEN_WIDTH'] = app.primaryScreen().size().width()
    CONFIG['SCREEN_HEIGHT'] = app.primaryScreen().size().height()

    window = QWidget()
    w1 = MasterWidget(CONFIG)
    layout = QGridLayout(window)
    layout.addWidget(w1, 0, 0, 1, 3)
    window.showMaximized()
    w1.setFocus()
    app.setWindowIcon(QIcon('./ASSETS/SHAMPOO.png'))
    sys.exit(app.exec_())
