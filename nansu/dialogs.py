import sys
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QDateEdit,
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDateTime


class CreateTransactionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWindowTitle("Nansu - Create Transaction")
        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()

        amount_input = QLineEdit()
        amount_input.setValidator(QIntValidator())

        start_date_picker = QDateEdit(calendarPopup=True)
        start_date_picker.setDateTime(QDateTime.currentDateTime())

        end_date_picker = QDateEdit(calendarPopup=True)
        end_date_picker.setDateTime(QDateTime.currentDateTime())

        formLayout.addRow("Amount [$]", amount_input)
        formLayout.addRow("Start Date", start_date_picker)
        formLayout.addRow("End Date", end_date_picker)
        # formLayout.addRow("Frequency", )
        formLayout.addRow("Description", QLineEdit())
        dialogLayout.addLayout(formLayout)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Save
        )
        # buttons.accepted.
        dialogLayout.addWidget(buttons)
        self.setLayout(dialogLayout)
