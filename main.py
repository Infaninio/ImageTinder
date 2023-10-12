
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QScrollArea, QSizePolicy
from PySide6.QtCore import QBasicTimer
from PySide6.QtGui import QPixmap

from pillow_heif import register_heif_opener
from PIL import Image
from PIL.ImageQt import ImageQt

import shutil
from pathlib import Path
import glob

class Slides(QMainWindow):
    def __init__(self, image_files, parent=None):
        register_heif_opener()
        QMainWindow.__init__(self, parent)
        self.image_files = image_files
        main_layout = QHBoxLayout()

        self.button_reject = QPushButton("Image to Trash", self)
        self.button_reject.clicked.connect(self.trash_button)
        main_layout.addWidget(self.button_reject)
        general_layout = QVBoxLayout()
        general_layout.addStretch()

        self.scroll = QScrollArea(self)
        s = '<>'*10
        self.label = QLabel(s, self)
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.scroll.setWidget(self.label)
        main_layout.addWidget(self.scroll)

        self.button_use = QPushButton("Image to images", self)
        self.button_use.clicked.connect(self.good_button)
        main_layout.addWidget(self.button_use)

        self.button = QPushButton("Useless Button",self)
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.button)

        widget = QWidget()
        general_layout.addLayout(upper_layout)
        general_layout.addLayout(main_layout,1)
        general_layout.addStretch()
        widget.setLayout(general_layout) 
        self.setCentralWidget(widget)
        self.show()
        self.setWindowTitle("Show vacation images")

        self.image_files: [Path] = []
        self.currentImage: Path = ""
        self.load_images(Path("C:/Users/mengel/Pictures/NewYork/Bilder"))
        self.set_new_Image()

    def load_images(self, dir_path: Path):
        self.image_files.clear()
        types = ["*.png", "*.heic", "*.jpg", "*.jpeg"]
        for type in types:
            self.image_files.extend(glob.glob(str(dir_path) + "\\" + type))

        self.image_files = [Path(file) for file in self.image_files if "_checked" not in file]


    def set_new_Image(self) -> None:

        self.currentImage = self.image_files.pop()
        pil_image = Image.open(self.currentImage)

        factor = min(1, self.scroll.viewport().size().width() / pil_image.width, self.scroll.viewport().size().height() / pil_image.height)
        pil_image = pil_image.resize((int(pil_image.width * factor), int(pil_image.height * factor)))
        self.label.resize(self.scroll.viewport().size())
        image = QPixmap.fromImage(ImageQt(pil_image))
        self.label.setPixmap(image)
        self.setWindowTitle(f"City:  Image: {self.currentImage}")

    def trash_button(self) -> None:
        shutil.move(self.currentImage, Path(self.currentImage.parent.parent, "Trash", self.currentImage.name))
        self.set_new_Image()

    def good_button(self) -> None:
        new_name = self.currentImage.stem + "_checked"
        shutil.move(self.currentImage, self.currentImage.with_stem(new_name))
        self.set_new_Image()

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