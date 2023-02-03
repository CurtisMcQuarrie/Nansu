from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QDateEdit,
    QMessageBox,
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QDateTime, Qt


class AddTransactionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Nansu - Add Transaction")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()
        

    def setupUI(self):
        """
        setup the add transaction dialog's GUI
        """
        self.amount_field = QLineEdit()
        self.amount_field.setValidator(QIntValidator())
        self.amount_field.setObjectName("Amount")

        self.date_field = QDateEdit(calendarPopup=True)
        self.date_field.setDateTime(QDateTime.currentDateTime())
        self.date_field.setObjectName("Date")

        self.description_field = QLineEdit()
        self.description_field.setObjectName("Description")

        formLayout = QFormLayout()
        formLayout.addRow("Amount:", self.amount_field)
        formLayout.addRow("Date:", self.date_field)
        formLayout.addRow("Description:", self.description_field)
        self.layout.addLayout(formLayout)

        self.buttons_box = QDialogButtonBox(self)
        self.buttons_box.setOrientation(Qt.Horizontal)
        self.buttons_box.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Save
        )
        self.buttons_box.accepted.connect(self.accept)
        self.buttons_box.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons_box)

    def accept(self):
        """
        accept data provided through dialog
        """
        self.data = []
        for field in (self.amount_field, self.date_field, self.description_field):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a transaction's {field.objectName()}",
                )
                self.data = None  # reset data
                return

            self.data.append(field.text())
        
        if not self.data:
            return
        
        super().accept()


