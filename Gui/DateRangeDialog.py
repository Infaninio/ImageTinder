from datetime import datetime
from typing import Tuple

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateEdit, QDialog, QDialogButtonBox, QVBoxLayout


class CustomDateRangeDialog(QDialog):
    """A custom dialog to select a date range."""

    def __init__(self, start_date: QDate, end_date: QDate, parent=None):
        """Create custom Data dialog.

        Parameters
        ----------
        start_date : QDate
            Starting date for the range selection
        end_date : QDate
            End/Max date for the range selection
        parent : _type_, optional
            Parent window, by default None
        """
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

    def get_date_range(self) -> Tuple[datetime, datetime]:
        start_date = self.start_date_edit.date().toPython()
        end_date = self.end_date_edit.date().toPython()

        return datetime.combine(start_date, datetime.min.time()), datetime.combine(
            end_date, datetime.max.time()
        )

    @staticmethod
    def get_data_range_dialog(
        start_date, end_date, parent=None
    ) -> Tuple[datetime, datetime]:
        dialog = CustomDateRangeDialog(
            start_date=start_date, end_date=end_date, parent=parent
        )
        result = dialog.exec_()

        if result:
            return dialog.get_date_range()

        return None
