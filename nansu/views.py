from PyQt5.QtWidgets import (
    QAbstractItemView,
    QTableView,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QDialog,
    QMessageBox,
    QWidget,
    QMainWindow,
    QStatusBar,
    QToolBar,
)
from .dialog import AddAccountDialog
from .model import AccountsModel, AccountField

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 550


class MainWindow(QMainWindow):
    """
    Main Window of application
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nansu Finance App")
        self._createMenu()
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.accounts_model = AccountsModel()
        self._setupUI()

    def _setupUI(self):
        """
        setup the main window's GUI
        """
        # create table view widget
        self.table = QTableView()
        self.table.setModel(self.accounts_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnHidden(AccountField.Id.value, True)
        # create buttons
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.openAddAccountDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteAccount)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearAccounts)
        # lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def openAddAccountDialog(self):
        """
        open the add account dialog
        """
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.accounts_model.addAccount(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteAccount(self):
        """
        delete the selected account from the database
        """
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected Account?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.accounts_model.deleteAccount(row)

    def clearAccounts(self):
        """
        remove all accounts from the database
        """
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your Accounts?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.accounts_model.clearAccounts()

    def _createMenu(self):
        """
        create the menu
        """
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)
