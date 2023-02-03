from PyQt6.QtWidgets import (
    QAbstractItemView,
    QTableView,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton, 
    QWidget,
    QMainWindow,
    QStatusBar,
    QToolBar, 
)
from .dialogs import CreateTransactionDialog

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
        self._setupUI()

    def _setupUI(self):
        """
        setup the main window's GUI
        """
        # create table view widget
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.resizeColumnsToContents()
        # create buttons
        self.addButton = QPushButton("Add")
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

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

        # transaction_menu = self.menuBar().addMenu("&Transactions")
        # create_transaction_dialog = CreateTransactionDialog(self)
        # transaction_menu.addAction("&Create", create_transaction_dialog.show)
    
