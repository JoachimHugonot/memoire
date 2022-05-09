# Core imports
import sys
import urllib
from urllib import request
import json

# Project imports
from cnn import *
from utils import pt_to_pixel, pixel_to_pt, resource_path

# 3rd parties imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

CONFIG = json.load(open('config.json'))
global FONT, DELAY_FADE, ELEMENT_BY_ELEMENT, IMAGE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, WIDTH_PERCENTAGE
ELEMENT_BY_ELEMENT = True

FONT = QFont('Helvetica', pixel_to_pt(CONFIG['TEXT_SIZE']))
FONT_TITLE = QFont('Helvetica', pixel_to_pt(CONFIG['TITLE_SIZE']))



class Padding(QLabel):
    def __init__(self, height):
        super().__init__()
        self.setFixedHeight(height)


class Title(QLabel):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
        self.setFont(FONT_TITLE)
        self.setFixedHeight(170)
        color_str = 'rgb'+str(tuple(CONFIG['TITLE_COLOR']))
        self.setStyleSheet('margin-top: 100px; margin-bottom: 10px; color:'+color_str)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedWidth(int(CONFIG['WIDTH_PERCENTAGE'] * SCREEN_WIDTH))


class Text(QLabel):
    def __init__(self, text):
        super().__init__()

        self.setText(text)

        self.setFont(FONT)
        self.setWordWrap(True)

        n_lines = text.count('<br>') + text.count('<ol>') + text.count('<ul>') + text.count('<li>') + 1
        self.setFixedHeight(int(50 * n_lines + pt_to_pixel(CONFIG['LINE_HEIGHT']) / 100 * (n_lines - 1)))
        self.setFixedWidth(int(CONFIG['WIDTH_PERCENTAGE'] * SCREEN_WIDTH))
        self.setAlignment(Qt.AlignCenter)
        color_str = 'rgb' + str(tuple(CONFIG['TEXT_COLOR']))
        self.setStyleSheet('color:'+color_str)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        formLayout = QVBoxLayout()
        groupBox = QLabel()
        groupBox.setLayout(formLayout)

        self.ELEMENTS = []
        self.scroll = QScrollArea()

        self.vsb = self.scroll.verticalScrollBar()
        self.scroll.setWidget(groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.horizontalScrollBar().setEnabled(False)
        self.scroll.setStyleSheet('background:lightgrey')

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

        # Creation of the elements
        self.layout = QVBoxLayout()
        WIDGETS_ONE = [
            # [Title('Que peuvent révéler mes données ?'),
            # QPixmap('ASSETS/LOGO2.png'),
            # QPixmap('ASSETS/COOP.jpg'),

            #   Text('<p style="line-height:'+str(line_height)+';">Imaginez vous en train d\'acheter un produit de beauté à la Coop.<br>'
            #    'Vous réglez vos achats avec votre supercard.<br>'
            #    'Le magasin a donc accès à votre historique d’achats.</p>'),

            #   QPixmap('ASSETS/SUPER_CARD.PNG')]
            # ,
            Title('1 - Que disent mes données sur moi ?'),
            # QPixmap('ASSETS/LOGO2.png'),
            # QPixmap('ASSETS/COOP.jpg'),

            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">Vous êtes en train d\'acheter un shampoing.<br>'
                               'Vous réglez vos achats avec votre carte de fidélité.<br>'
                               'Le magasin a donc accès à votre historique d’achats.</p>'),
            Padding(5),
            QPixmap(resource_path('./ASSETS/LOYALTY_CARD.png'))
            ,
            Title('2 - Que sait le magasin sur vous ?'),
            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">Le magasin sait quel shampoing vous venez d\'acheter.<br>'

                               "Est-ce que vous pensez que cette information personelle révèle beaucoup à votre sujet ?<br>"
                               "<span style=\"color:rgb(0,175,0)\">Non, pas du tout </span>  <br>"
                               "<span style=\"color:rgb(175,127,0)\">Un peu, rien d'important</span>  <br>"
                               "<span style=\"color:rgb(175,0,0)\">Oui, beaucoup trop</span>  </p>"),

            Title('3 - Un simple achat peut en dire beaucoup sur vous !'),
            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">En 2012, un magasin a appris qu’une adolescente était enceinte avant que sa famille ne l\'apprenne.<br>'
                               'Elle a juste acheté un shampoing sans parfum et le magasin en a déduit qu\'elle était enceinte.<br>'
                               'En effet, les femmes enceintes préfèrent acheter des produits sans parfum.<br>'
                 # 'L\'adolescente qui achetait des produits très parfumé a subitement commencé à acheter des produits aux parfums neutres.<br>'
                               '<a href=\"https://ladigitale.dev/digiread/#/a/6262819b4f474\">Je veux en savoir plus</a><br>'
                 # 'Un simple achat peut en dire beaucoup sur vous</p>'
                 ),
            Padding(5),
            QPixmap(resource_path('./ASSETS/SHAMPOO.png')),
            # QPixmap("ASSETS/MONEY.png"),
            Title("4 - Pourquoi les entreprises veulent mes données ?"),
            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">Les entreprises gagnent de l\'argent avec vos informations personnelles<br>'
                               'Le magasin les a utilisées pour personnaliser la publicité envoyée à l\'adolescente : des couches et des berceaux.<br>'
                               'Une carte de fidélité nous fait économiser de l\'argent, mais en échange, nous payons avec nos informations personelles...<br>'
                               '... afin que les entreprises gagnent encore plus d\'argent !</p>'),
            Padding(5),
            QPixmap(resource_path("./ASSETS/MONEY.png")),
            Title("5 - Comment est-ce possible ?"),
            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">Grâce à l\'historique d\'achats de ses 2 millions de clients quotidiens.<br>'
                               'Un humain ne peut pas analyser toutes ces données à la main. Un ordinateur, oui.<br>'
                               'Avez-vous déjà entendu parler d\'intelligence artificielle, de réseaux de neurones ou de deep learning ? <br>'
                               'C\'est ce qui permet aux entreprises de transformer vos données en argent.</p>'),

            QPixmap(resource_path("./ASSETS/COMPUTER.png")),
            Title('6 - Un réseau de neurones ? Essayez !'),
            Text('<p style="line-height:' + str(
                CONFIG['LINE_HEIGHT']) + ';">Maintenant, vous allez analyser des photos avec un réseau de neurones. <br>'
                 # 'Vous pouvez utiliser une image de votre ordinateur, ou le lien d\'une image sur internet<br>'
                               'N\'hésitez pas à analyser vos photos personelles : nous garantissons que nous ne gardons aucune image.</p>'),

            secondTab(),
            Title("7 - Et alors ?"),
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
            if type(widget) == Text or type(widget) == Title:
                # widget.setWordWrap(False)
                # widget.setAlignment(Qt.AlignCenter)
                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)

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
                # widget.setFixedHeight(50)
                # widget.setFixedWidth(1600)

                widget.setWordWrap(True)

                widget.setAlignment(Qt.AlignCenter)
                self.ELEMENTS.append(widget)
                formLayout.addWidget(widget, alignment=Qt.AlignCenter)
                if "href" in widget.text():
                    widget.setTextFormat(Qt.RichText)
                    widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
                    widget.setOpenExternalLinks(True)
            elif type(widget) == list:
                title, text, image = widget

                assert type(title) == Title
                assert type(text) == Text
                assert type(image) == QPixmap

                lay = QVBoxLayout()
                pane = QLabel()
                subPane = QLabel()
                sublay = QHBoxLayout()

                lay.setSizeConstraint(QLayout.SetFixedSize)

                pane.setLayout(lay)
                subPane.setLayout(sublay)
                lay.addWidget(title)
                lay.addWidget(subPane)

                sublay.addWidget(text)
                text.setAlignment(Qt.AlignRight)
                text.setFixedWidth(int(SCREEN_WIDTH * 0.75))
                image = image.scaledToWidth(int(SCREEN_WIDTH * 0.20))

                image_ph = QLabel()
                image_ph.setPixmap(image)

                sublay.addWidget(image_ph)

                self.ELEMENTS.append(pane)
                formLayout.addWidget(pane, alignment=Qt.AlignCenter)
        for el in self.ELEMENTS:
            if ELEMENT_BY_ELEMENT:
                el.hide()
        formLayout.setContentsMargins(0, 0, 0, 0)
        formLayout.setSizeConstraint(QLayout.SetFixedSize)

    def mousePressEvent(self, event):
        event.accept()

    def keyPressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if Qt.Key_N == event.key():

            for idx, el in enumerate(self.ELEMENTS):
                if not el.isVisible():

                    el.show()

                    if idx != len(self.ELEMENTS) - 1 and type(self.ELEMENTS[idx + 1]) in [Title]:
                        break
            # self.vsb.setValue(self.vsb.maximum() + 200)
            QTimer.singleShot(100, self.handle_timeout)
        if Qt.Key_W == event.key() and modifiers == Qt.ControlModifier:
            sys.exit()

    def handle_timeout(self):
        x = self.vsb.maximum()
        self.vsb.setValue(x + 200)


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

        self.from_url_button = QPushButton('Télécharger depuis un lien')
        self.from_url_button.setFont(FONT)
        self.from_url_button.setFocusPolicy(Qt.NoFocus)
        self.from_url_button.clicked.connect(self.select_files_from_url)

        self.from_analyse_button = QPushButton('Analyser')
        self.from_analyse_button.setFont(FONT)
        self.from_analyse_button.setFocusPolicy(Qt.NoFocus)
        self.from_analyse_button.clicked.connect(self.analyse)

        self.show_hide_button = QPushButton('Voir l\'image')
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

        self.from_url_edit.setFixedWidth(int(SCREEN_WIDTH * CONFIG['WIDTH_PERCENTAGE'] / 3.0))
        self.from_url_button.setFixedWidth(int(SCREEN_WIDTH * CONFIG['WIDTH_PERCENTAGE'] / 3.0))
        self.from_drive_button.setFixedWidth(int(SCREEN_WIDTH * CONFIG['WIDTH_PERCENTAGE'] / 3.0))

        self.from_url_edit.setFixedHeight(60)
        self.from_url_edit.setStyleSheet('background:white')
        self.from_url_button.setFixedHeight(40)

        self.from_drive_button.setFixedHeight(40)

        self.grid_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.IMAGE_PH = QLabel('abc')
        self.IMAGE_PH_LAYOUT = QHBoxLayout()
        self.IMAGE_PH.setLayout(self.IMAGE_PH_LAYOUT)

        self.image_ph = QLabel()
        self.image_ph.setFixedHeight(600)

        self.labels_ph = QLabel()
        self.labels_ph.setFont(FONT_TITLE)
        self.labels_ph.setAlignment(Qt.AlignCenter)
        self.labels_ph.setFixedHeight(50)

        self.fileselect.setFixedHeight(60)
        self.main_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.main_layout.addWidget(self.fileselect, 1)
        self.main_layout.addWidget(self.image_ph, 5, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.labels_ph, 1)  # padding
        self.main_layout.addWidget(self.from_analyse_button, 1)  # padding
        self.main_layout.addWidget(self.show_hide_button, 1)  # padding
        # self.main_layout.addWidget(QLabel(''), 1)  # padding
        self.displaying_results = False
        self.setLayout(self.main_layout)
        self.file_to_analyse = cv2.imread(resource_path('SAMPLES/01.jpeg'))
        self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
        self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(CONFIG['IMAGE_HEIGHT'])
        self.image_ph.setPixmap(self.file_to_analyse_pixmap)

    def show_hide(self):
        if self.displaying_results:
            self.displaying_results = False
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)
            self.show_hide_button.setText('Voir les résultats')

        else:
            self.displaying_results = True
            self.image_ph.setPixmap(self.file_analysed_pixmap)

            labels = []

            if self.SEEN == []:
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
        if check:
            self.file_to_analyse = cv2.imread(file)
            self.file_to_analyse_pixmap = self.convert_cv_qt(self.file_to_analyse)
            self.file_to_analyse_pixmap = self.file_to_analyse_pixmap.scaledToHeight(CONFIG['IMAGE_HEIGHT'])
            self.image_ph.setPixmap(self.file_to_analyse_pixmap)

            self.displaying_results = False
            self.labels_ph.setText('')
            self.show_hide_button.setEnabled(False)

    def convert_cv_qt(self, cv_img):
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
    SCREEN_WIDTH = app.primaryScreen().size().width()
    SCREEN_HEIGHT = app.primaryScreen().size().height()

    window = QWidget()
    w1 = MainWindow()
    layout = QGridLayout(window)
    layout.addWidget(w1, 0, 0, 1, 3)
    window.showMaximized()
    w1.setFocus()
    app.setWindowIcon(QIcon('./ASSETS/SHAMPOO.png'))
    sys.exit(app.exec_())
