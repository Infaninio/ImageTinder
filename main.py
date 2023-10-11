
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QBasicTimer
from PySide6.QtGui import QPixmap

from pillow_heif import register_heif_opener
from PIL import Image
from PIL.ImageQt import ImageQt


class Slides(QMainWindow):
    def __init__(self, image_files, parent=None):
        register_heif_opener()
        QMainWindow.__init__(self, parent)
        self.image_files = image_files
        main_layout = QHBoxLayout()
        main_layout.setStretch(1,3)

        self.button_reject = QPushButton("Image to Trash", self)
        main_layout.addWidget(self.button_reject)
        upper_layout = QVBoxLayout()
        upper_layout.setStretch(1,2)

        s = '<>'*10
        self.label = QLabel(s, self)
        main_layout.addWidget(self.label)

        self.button_use = QPushButton("Image to images", self)
        main_layout.addWidget(self.button_use)

        self.button = QPushButton("Start Slide Show",self)
        # self.button.setGeometry(10, 10, 140, 30)
        self.button.clicked.connect(self.timerEvent)

        self.timer = QBasicTimer()
        self.step = 0
        self.delay = 5000  # milliseconds

        widget = QWidget()
        upper_layout.addWidget(self.button)
        upper_layout.addLayout(main_layout)
        widget.setLayout(upper_layout) 
        self.setCentralWidget(widget)
        sf = "Slides are shown {} seconds apart"
        self.setWindowTitle(sf.format(self.delay/1000.0))

    def timerEvent(self, e=None):
        if self.step >= len(self.image_files):
            self.timer.stop()
            self.button.setText('Slide Show Finished')
            return
        self.timer.start(self.delay, self)
        file = self.image_files[self.step]
        pil_image = Image.open(file)

        factor = min(1, self.label.size().width() / pil_image.width, self.label.size().height() / pil_image.height)
        pil_image = pil_image.resize((int(pil_image.width * factor), int(pil_image.height * factor)))

        image = QPixmap.fromImage(ImageQt(pil_image))
        self.label.setPixmap(image)
        self.setWindowTitle("{} --> {}".format(str(self.step), file))
        self.step += 1


# pick image files you have in the working folder
# or give full path name
image_files = [
"C:/Users/mengel/Downloads/sample1.heic",
"C:/Users/mengel/Downloads/agil_v_model.png",
"C:/Users/mengel/Downloads/Changemanagement.png",
"C:/Users/mengel/Downloads/hw_development.png",
"C:/Users/mengel/Downloads/v_model.png",
]

app = QApplication([])
w = Slides(image_files)
# setGeometry(x, y, w, h)  x,y = upper left corner coordinates
w.setGeometry(100, 100, 700, 500)
w.show()
app.exec()