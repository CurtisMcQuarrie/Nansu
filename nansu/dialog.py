from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QDateTimeEdit,
    QMessageBox,
    QComboBox,
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QDateTime, Qt
from .model import PaymentFrequency


class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Nansu - Add Account")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        """
        setup the add account dialog's GUI
        """
        self.name_field = QLineEdit()
        self.name_field.setObjectName("Name")

        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.name_field)
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
        self.data = {}
        if not self.name_field.text():
            QMessageBox.critical(
                self,
                "Error!",
                f"You must provide an account's {self.name_field.objectName()}",
            )
            self.data = None  # reset data
            return

        self.data["Name"] = self.name_field.text()

        if not self.data:
            return

        super().accept()


class AddTransactionDialog(QDialog):
    def __init__(self, account_id, parent=None):
        super().__init__(parent=parent)
        self.account_id = account_id
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

        formLayout = QFormLayout()
        formLayout.addRow("Amount:", self.amount_field)
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
        if not self.amount_field.text():
            QMessageBox.critical(
                self,
                "Error!",
                f"You must provide a transaction's {self.amount_field.objectName()}",
            )
            self.data = None  # reset data
            return

        self.data.append(self.amount_field.text())

        if not self.data:
            return
        else:
            self.data["Account"] = self.account_id

        super().accept()


class AddPaymentDialog(QDialog):
    def __init__(self, account_id, parent=None):
        super().__init__(parent=parent)
        self.account_id = account_id
        self.setWindowTitle("Nansu - Add Payment")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        """
        setup the add payment dialog's GUI
        """
        self.form_fields = list()

        self.amount_field = QLineEdit()
        self.amount_field.setValidator(QIntValidator())
        self.amount_field.setObjectName("Amount")
        self.form_fields.append(self.amount_field)

        self.start_date_field = QDateTimeEdit(calendarPopup=True)
        self.start_date_field.setDateTime(QDateTime.currentDateTime())
        self.start_date_field.setObjectName("StartDate")
        self.form_fields.append(self.start_date_field)

        self.end_date_field = QDateTimeEdit(calendarPopup=True)
        self.end_date_field.setDateTime(QDateTime.currentDateTime())
        self.end_date_field.setObjectName("EndDate")
        self.form_fields.append(self.end_date_field)

        self.frequency_field = QComboBox()
        for freq in PaymentFrequency:
            self.frequency_field.addItem(freq.value)
        self.frequency_field.setObjectName("Frequency")
        self.form_fields.append(self.frequency_field)

        self.description_field = QLineEdit()
        self.description_field.setObjectName("Description")
        self.form_fields.append(self.description_field)

        formLayout = QFormLayout()
        formLayout.addRow("Amount:", self.amount_field)
        formLayout.addRow("Start Date:", self.start_date_field)
        formLayout.addRow("End Date:", self.end_date_field)
        formLayout.addRow("Frequency:", self.frequency_field)
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
        self.data = {}
        for field in self.form_fields:
            if isinstance(field, QComboBox):
                text = field.currentText()
            else:
                text = field.text()
            if not text:
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a payment's {field.objectName()}",
                )
                self.data = None  # reset data
                return

            self.data[field.objectName()] = text

        if not self.data:
            return
        else:
            self.data["Account"] = self.account_id

        super().accept()