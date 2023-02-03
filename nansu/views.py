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
        self.table.resizeColumnsToContents()
        # create buttons
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.openAddTransactionDialog)
        self.deleteButton = QPushButton("Delete")
        self.clearAllButton = QPushButton("Clear All")
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

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)


