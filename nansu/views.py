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
    QStackedWidget,
)
from .dialog import AddAccountDialog
from .model import AccountsModel, AccountField, TableType, CustomModel  #, PaymentsModel, PaymentField

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 550


class MainWindow(QMainWindow):
    """
    Main Window of application
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nansu Finance App")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # initialize subwidgets
        self.accounts_widget = AccountsWidget(parent=self)
        self.central_widget = QStackedWidget()
        self.central_widget.addWidget(self.accounts_widget)
        self.setCentralWidget(self.central_widget)

    def _createMenu(self):
        """
        create the menu
        """
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)


class AccountsWidget(QWidget):
    """
    View for manipulating accounts
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.accounts_model = CustomModel("accounts", ["ID", "CreateDate", "Name"], TableType.NonRelational)
        self.outer_layout = QHBoxLayout()
        # self.model = AccountsModel()
        self.inner_layout = QVBoxLayout()
        self._setupUI()
        self.setLayout(self.outer_layout)
        

    def _setupUI(self):
        """
        setup accounts view gui
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
        self.viewButton = QPushButton("View")
        self.viewButton.clicked.connect(self.viewAccount)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearAccounts)
        # lay out the GUI
        layout = QVBoxLayout()
        self.inner_layout.addWidget(self.addButton)
        self.inner_layout.addWidget(self.deleteButton)
        self.inner_layout.addStretch()
        self.inner_layout.addWidget(self.viewButton)
        self.inner_layout.addWidget(self.clearAllButton)
        self.outer_layout.addWidget(self.table)
        self.outer_layout.addLayout(self.inner_layout)

    def openAddAccountDialog(self):
        """
        open the add account dialog
        """
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.accounts_model.add(dialog.data)
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
            self.accounts_model.delete(row)

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
            self.accounts_model.clear()

    
    def viewAccount(self):
        """
        view the selected account
        """
        pass