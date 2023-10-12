import glob
import shutil
from pathlib import Path

from PIL import Image
from PIL.ImageQt import ImageQt
from pillow_heif import register_heif_opener
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ImageViewer(QMainWindow):
    """Simple Image viewr to decide wether to keep a photo or not."""

    def __init__(self, parent=None):
        """Create the image viewer."""
        register_heif_opener()
        QMainWindow.__init__(self, parent)
        main_layout = QHBoxLayout()

        self.button_reject = QPushButton("Image to Trash", self)
        self.button_reject.clicked.connect(self.trash_button)
        main_layout.addWidget(self.button_reject)
        general_layout = QVBoxLayout()
        general_layout.addStretch()

        self.scroll = QScrollArea(self)
        s = "<>" * 10
        self.label = QLabel(s, self)
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.scroll.setWidget(self.label)
        main_layout.addWidget(self.scroll)

        self.button_use = QPushButton("Image to images", self)
        self.button_use.clicked.connect(self.good_button)
        main_layout.addWidget(self.button_use)

        self.button = QPushButton("Useless Button", self)
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.button)

        widget = QWidget()
        general_layout.addLayout(upper_layout)
        general_layout.addLayout(main_layout, 1)
        general_layout.addStretch()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)
        self.show()
        self.setWindowTitle("Show vacation images")

        self.image_files: [Path] = []
        self.currentImage: Path = ""
        self.load_images(Path("C:/Users/mengel/Pictures/NewYork/Bilder"))

    def load_images(self, dir_path: Path):
        """Load the image files of the specified path.

        Parameters
        ----------
        dir_path : Path
            Path to the image directory.
        """
        self.image_files.clear()
        types = ["*.png", "*.heic", "*.jpg", "*.jpeg"]
        for type in types:
            self.image_files.extend(glob.glob(str(dir_path) + "\\" + type))

        self.image_files = [
            Path(file) for file in self.image_files if "_checked" not in file
        ]

    def set_new_Image(self) -> None:
        """Set a new Image to the UI."""
        self.currentImage = self.image_files.pop()
        pil_image = Image.open(self.currentImage)

        factor = min(
            1,
            self.scroll.viewport().size().width() / pil_image.width,
            self.scroll.viewport().size().height() / pil_image.height,
        )
        pil_image = pil_image.resize(
            (int(pil_image.width * factor), int(pil_image.height * factor))
        )
        self.label.resize(self.scroll.viewport().size())
        image = QPixmap.fromImage(ImageQt(pil_image))
        self.label.setPixmap(image)
        self.setWindowTitle(f"City:  Image: {self.currentImage}")

    def trash_button(self) -> None:
        """Move the image to the trash folder."""
        shutil.move(
            self.currentImage,
            Path(self.currentImage.parent.parent, "Trash", self.currentImage.name),
        )
        self.set_new_Image()

    def good_button(self) -> None:
        """Mark the image as checked and keep it in the same folder."""
        new_name = self.currentImage.stem + "_checked"
        shutil.move(self.currentImage, self.currentImage.with_stem(new_name))
        self.set_new_Image()


if __name__ == "__main__":
    app = QApplication([])
    w = ImageViewer()
    w.setGeometry(100, 100, 700, 500)
    w.show()
    w.set_new_Image()
    app.exec()
