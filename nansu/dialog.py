from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QDateTimeEdit,
    QMessageBox,
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QDateTime, Qt


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
        self.data = []
        if not self.name_field.text():
            QMessageBox.critical(
                self,
                "Error!",
                f"You must provide an account's {self.name_field.objectName()}",
            )
            self.data = None  # reset data
            return

        self.data.append(self.name_field.text())

        if not self.data:
            return

        super().accept()


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

        super().accept()


    # def accept(self):
    #     """
    #     accept data provided through dialog
    #     """
    #     self.data = []
    #     for field in (self.amount_field, self.date_field, self.description_field):
    #         if not field.text():
    #             QMessageBox.critical(
    #                 self,
    #                 "Error!",
    #                 f"You must provide a transaction's {field.objectName()}",
    #             )
    #             self.data = None  # reset data
    #             return

    #         self.data.append(field.text())

    #     if not self.data:
    #         return

    #     super().accept()
