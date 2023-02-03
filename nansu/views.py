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
from .dialog import AddTransactionDialog
from .model import TransactionsModel

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
        self.transactions_model = TransactionsModel()
        self._setupUI()

    def _setupUI(self):
        """
        setup the main window's GUI
        """
        # create table view widget
        self.table = QTableView()
        self.table.setModel(self.transactions_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(3, True)
        # create buttons
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.openAddTransactionDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteTransaction)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearTransactions)
        # lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def openAddTransactionDialog(self):
        """
        open the add transaction dialog
        """
        dialog = AddTransactionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.transactions_model.addTransaction(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteTransaction(self):
        """
        delete the selected transaction from the database
        """
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected transaction?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.transactions_model.deleteTransaction(row)

    def clearTransactions(self):
        """
        remove all transactions from the database
        """
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contacts?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.transactions_model.clearTransactions()

    def _createMenu(self):
        """
        create the menu
        """
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)
