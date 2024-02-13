import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image
from PIL.ImageQt import ImageQt
from pillow_heif import register_heif_opener
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeyEvent, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QProgressDialog,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from DateRangeDialog import CustomDateRangeDialog
from image_selector import ImageSelector


class ImageViewer(QMainWindow):
    """Simple Image viewr to decide wether to keep a photo or not."""

    def __init__(self, parent=None):
        """Create the image viewer."""
        self.available_images = {}
        self.user_name: Optional[str] = None
        register_heif_opener()
        QMainWindow.__init__(self, parent)
        main_layout = QHBoxLayout()

        self.button_reject = QPushButton("Image to Trash", self)
        self.button_reject.clicked.connect(self.trash_button)
        self.button_reject.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.button_reject.setStyleSheet("background-color: #A44A3F")
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
        self.button_use.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.button_use.setStyleSheet("background-color: #82D943")
        main_layout.addWidget(self.button_use)

        widget = QWidget()
        general_layout.addLayout(main_layout, 1)
        general_layout.addStretch()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)
        self.show()
        self.setWindowTitle("Show vacation images")

        self.image_files: [Path] = []
        self.currentImage: Path = ""
        self.create_menu_bar()
        self.selector = ImageSelector()

    def open_image_dialog(self):
        base_dir = Path(
            QFileDialog.getExistingDirectory(
                self, "Choose your directory for the images"
            )
        )

        progress = QProgressDialog("Analysing files...", "Abort", 0, 1, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        self.selector.load_images(
            base_dir, progress.setMaximum, progress.setValue, progress.wasCanceled
        )
        date_range = CustomDateRangeDialog.get_data_range_dialog(
            self.selector._base_date_range[0], self.selector._base_date_range[1], self
        )

        self.filter_available_images(date_range[0], date_range[1])
        self.selector.store_progress(
            Path(__file__).with_name("tmp.itsf"), absolute=True
        )

        self.user_name = QInputDialog.getText(
            self, "Enter name", "Please enter your name:"
        )
        self.selector.user = self.user_name
        pass

    def load_configuration(self):

        config_file = QFileDialog.getOpenFileName(
            self, "Choose your directory for the images", filter="*.itsf"
        )
        if not config_file[0]:
            return
        self.selector.load_configuration(Path(config_file[0]))

        self.user_name = QInputDialog.getText(
            self, "Enter name", "Please enter your name:"
        )
        self.selector.user = self.user_name
        self.set_next_image()

    def set_next_image(self):
        next(iter(self.selector))
        pass

    def save_configuration(self):
        config_file = QFileDialog.getSaveFileName(
            self,
            "Choose your directory for the storage of the configuration",
            filter="*.itsf",
        )
        if not config_file[0]:
            return

        self.selector.store_progress(Path(config_file[0]))

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        # File menu
        file_menu = menu_bar.addMenu("File")

        # Create action
        open_action = QAction("Create new Configuration", self)
        open_action.triggered.connect(self.open_image_dialog)
        file_menu.addAction(open_action)

        # load configuration
        load_action = QAction("Load a Configuration", self)
        load_action.triggered.connect(self.load_configuration)
        file_menu.addAction(load_action)

        # Save configuration
        save_action = QAction("Save current Configuration", self)
        save_action.triggered.connect(self.save_configuration)
        file_menu.addAction(save_action)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_A:
            self.trash_button()
            event.accept()
            return
        if key == Qt.Key.Key_D:
            self.good_button()
            event.accept()
            return
        return super().keyPressEvent(event)

    def filter_available_images(self, start_date: datetime, end_date: datetime):
        for key, value in self.available_images.items():
            check_date = datetime.fromisoformat(value["date"])
            if start_date <= check_date <= end_date:
                self.available_images.pop(key)

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
    app.exec()
