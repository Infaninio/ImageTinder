from PySide6.QtWidgets import QDialog, QVBoxLayout, QDateEdit, QDialogButtonBox
from PySide6.QtCore import QDate
import os
from PIL import Image
from datetime import datetime

class CustomDateRangeDialog(QDialog):
    
    def __init__(self, start_date: QDate, end_date: QDate, parent=None):
        super(CustomDateRangeDialog, self).__init__(parent)

        self.setWindowTitle("Custom Date Range Dialog")

        layout = QVBoxLayout()
        self.start_date_edit = QDateEdit()
        self.end_date_edit = QDateEdit()
        
        self.start_date_edit.setDate(start_date)
        self.end_date_edit.setDate(end_date)
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit.setCalendarPopup(True)



        layout.addWidget(self.start_date_edit)
        layout.addWidget(self.end_date_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_date_range(self):
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()
        return start_date, end_date
    
    @staticmethod
    def get_data_range_dialog(start_date, end_date, parent=None):
        dialog = CustomDateRangeDialog(start_date=start_date, end_date=end_date, parent=parent)
        result = dialog.exec_()

        if result:
            return dialog.get_date_range()
        
        return None


def get_image_creation_date(file_path):

    with Image.open(file_path) as img:
        # Get the creation timestamp from the image's Exif data
        try:
            exif_info = img._getexif()
            if exif_info and 36867 in exif_info:
                creation_timestamp = exif_info[36867]
            else:
                creation_timestamp = None
        except:
            creation_timestamp = None

    if creation_timestamp:
        creation_date = datetime.strptime(creation_timestamp, "%Y:%m:%d %H:%M:%S")
    else:
        creation_date = datetime.fromtimestamp(os.path.getmtime(file_path))
    return QDate(creation_date)
