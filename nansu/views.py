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
    QTabWidget,
)
from PyQt5 import QtCore
from .dialog import AddAccountDialog, AddPaymentDialog, AddTransactionDialog
from .model import TableType, CustomModel, CustomTransactionModel

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 550


class MainWindow(QMainWindow):
    """
    Main Window of application
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_account_id = -1
        self.current_payment_id = -1
        self.setWindowTitle("Nansu Finance App")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # initialize subwidgets
        self.central_widget = QStackedWidget(parent=self)
        self.accounts_widget = AccountsWidget(parent=self.central_widget)
        self.tabs_widget = TabsWidget(parent=self.central_widget)
        # add subwidgets to central widget
        self.central_widget.addWidget(self.accounts_widget)
        self.central_widget.addWidget(self.tabs_widget)
        self.setCentralWidget(self.central_widget)

    def _createMenu(self):
        """
        create the menu
        """
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def switchWidget(self, index):
        if index == 1:  # go to payments
            query_str = f"SELECT name FROM accounts WHERE id={self.current_account_id}"
            row_data = self.tabs_widget.payments_tab.payments_model.getRowData(query_str)
            if len(row_data) > 0:
                self.tabs_widget.payments_tab.setTitle(f"{row_data[0]}")
            else:
                self.tabs_widget.payments_tab.setTitle("")
            self.tabs_widget.payments_tab.payments_model.setFilter("accountID", self.current_account_id)
            self.tabs_widget.transactions_tab.transactions_model.setFilter("accountID", self.current_account_id)

        self.central_widget.setCurrentIndex(index)


class AccountsWidget(QWidget):
    """
    View for manipulating accounts
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_window = self.parent().parent()
        self.accounts_model = CustomModel("accounts", ["ID", "CreateDate", "Name"], TableType.NonRelational)
        self.outer_layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()
        self.btns_layout = QVBoxLayout()
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
        # create the title
        self.title = QLabel("<h1>Accounts</h1>")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setWordWrap(True)
        # create buttons
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.openAddDialog)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete)
        self.view_button = QPushButton("View")
        self.view_button.clicked.connect(self.view)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clear)
        # lay out the buttons GUI
        self.btns_layout.addWidget(self.add_button)
        self.btns_layout.addWidget(self.delete_button)
        self.btns_layout.addStretch()
        self.btns_layout.addWidget(self.view_button)
        self.btns_layout.addWidget(self.clearAllButton)
        # lay out the main GUI
        self.outer_layout.addWidget(self.title)
        self.outer_layout.addLayout(self.inner_layout)
        self.inner_layout.addWidget(self.table)
        self.inner_layout.addLayout(self.btns_layout)

    def openAddDialog(self):
        """
        open the add account dialog
        """
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.accounts_model.add(dialog.data)
            self.table.resizeColumnsToContents()

    def delete(self):
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

    def clear(self):
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

    
    def view(self):
        """
        view the selected account
        """
        # get current account id
        row =  self.table.currentIndex().row()
        if row < 0:
            return
        current_index = self.table.model().index(row, 0)
        self.main_window.current_account_id = self.table.model().data(current_index)
        # switch views
        self.main_window.switchWidget(self.parent().currentIndex() + 1)


class PaymentsWidget(QWidget):
    """
    View for manipulating payments
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.central_widget = self.parent().parent()
        self.main_window = self.central_widget.parent()
        self.payments_model = CustomModel(
            "payments", 
            ["ID", "CreateDate", "StartDate", "EndDate", "Frequency", "Description", "Account"], 
            TableType.Relational
            )
        self.payments_model.setRelation("Account", self.main_window.accounts_widget.accounts_model, "ID", "Name")
        self.transactions_model = CustomTransactionModel(  # transaction model for adding new transactions based on new payments
            "transactions", 
            ["ID", "Amount", "Unit", "PaidDate", "DueDate", "Payment", "Account"], 
            TableType.Relational
            )
        self.transactions_model.setRelation("Payment", self.payments_model, "ID", "Description")
        self.transactions_model.setRelation("Account", self.main_window.accounts_widget.accounts_model, "ID", "Name")
        self.outer_layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()
        self.btns_layout = QVBoxLayout()
        self._setupUI()
        self.setLayout(self.outer_layout)
        

    def _setupUI(self):
        """
        setup payments view gui
        """
        # create table view widget
        self.table = QTableView()
        self.table.setModel(self.payments_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(6, True)
        # create the title
        self.title = QLabel("<h1>Payments</h1>")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        # create buttons
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.openAddDialog)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)
        self.view_button = QPushButton("View")
        self.view_button.clicked.connect(self.view)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clear)
        # lay out the buttons GUI
        self.btns_layout.addWidget(self.add_button)
        self.btns_layout.addWidget(self.delete_button)
        self.btns_layout.addStretch()
        self.btns_layout.addWidget(self.view_button)
        self.view_button.setEnabled(False)
        self.btns_layout.addWidget(self.back_button)
        self.btns_layout.addWidget(self.clearAllButton)
        # lay out the main GUI
        self.outer_layout.addWidget(self.title)
        self.outer_layout.addLayout(self.inner_layout)
        self.inner_layout.addWidget(self.table)
        self.inner_layout.addLayout(self.btns_layout)

    def openAddDialog(self):
        """
        open the add payment dialog
        """
        dialog = AddPaymentDialog(self.main_window.current_account_id, self)
        if dialog.exec() == QDialog.Accepted:
            self.payments_model.add(dialog.data)
            self.transactions_model.addFromPayment(dialog.data)
            self.table.resizeColumnsToContents()

    def delete(self):
        """
        delete the selected payment from the database
        """
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected Payment?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.payments_model.delete(row)

    def clear(self):
        """
        remove all payments from the database
        """
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your Payments?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.payments_model.clear()

    
    def view(self):
        """
        view the selected account
        """
         # get current account id
        row =  self.table.currentIndex().row()
        if row < 0:
            return
        current_index = self.table.model().index(row, 0)
        self.main_window.current_payment_id = self.table.model().data(current_index)
        # switch views
        self.main_window.switchWidget(self.central_widget.currentIndex() + 1)

    def back(self):
        """
        go back to previous index
        """
        self.main_window.current_account_id = -1
        self.main_window.switchWidget(self.central_widget.currentIndex() - 1)

    def setTitle(self, title, max_length=16):
        """
        set and format the title of the view
        """
        if len(title) > max_length:
            self.title.setToolTip(title)
            title = title[:max_length-3] + "..."
            self.title.setText(f"<h1>\"{title}\" Payments</h>")
        elif len(title) == 0:
            self.title.setToolTip(None)
            self.title.setText(f"<h1>Payments</h>")
        else:
            self.title.setToolTip(None)
            self.title.setText(f"<h1>\"{title}\" Payments</h>")


class TransactionsWidget(QWidget):
    """
    View for manipulating transactions
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.central_widget = self.parent().parent()
        self.main_window = self.central_widget.parent()
        self.transactions_model = CustomModel(
            "transactions", 
            ["ID", "Amount", "Unit", "PaidDate", "DueDate", "Payment", "Account"], 
            TableType.Relational
            )
        self.transactions_model.setRelation("Payment", self.parent().payments_tab.payments_model, "ID", "Description")
        self.transactions_model.setRelation("Account", self.main_window.accounts_widget.accounts_model, "ID", "Name")
        self.outer_layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()
        self.btns_layout = QVBoxLayout()
        self._setupUI()
        self.setLayout(self.outer_layout)
        

    def _setupUI(self):
        """
        setup payments view gui
        """
        # create table view widget
        self.table = QTableView()
        self.table.setModel(self.transactions_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnHidden(0, True)
        # create the title
        self.title = QLabel("<h1>Transactions</h1>")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        # create buttons
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.openAddDialog)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)
        self.view_button = QPushButton("View")
        self.view_button.clicked.connect(self.view)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clear)
        # lay out the buttons GUI
        layout = QVBoxLayout()
        self.btns_layout.addWidget(self.add_button)
        self.btns_layout.addWidget(self.delete_button)
        self.btns_layout.addStretch()
        self.btns_layout.addWidget(self.view_button)
        self.btns_layout.addWidget(self.back_button)
        self.btns_layout.addWidget(self.clearAllButton)
        # lay out the main GUI
        self.outer_layout.addWidget(self.title)
        self.outer_layout.addLayout(self.inner_layout)
        self.inner_layout.addWidget(self.table)
        self.inner_layout.addLayout(self.btns_layout)

    def openAddDialog(self):
        """
        open the add payment dialog
        """
        dialog = AddPaymentDialog(self.main_window.current_payment_id, self)
        if dialog.exec() == QDialog.Accepted:
            self.transactions_model.add(dialog.data)
            self.table.resizeColumnsToContents()

    def delete(self):
        """
        delete the selected payment from the database
        """
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected Transaction?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.transactions_model.delete(row)

    def clear(self):
        """
        remove all payments from the database
        """
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your Transactions?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.transactions_model.clear()

    
    def view(self):
        """
        view the selected account
        """
         # get current account id
        row =  self.table.currentIndex().row()
        if row < 0:
            return
        current_index = self.table.model().index(row, 0)
        self.main_window.current_payment_id = self.table.model().data(current_index)
        # switch views
        self.main_window.switchWidget(self.central_widget.currentIndex() + 1)

    def back(self):
        """
        go back to previous index
        """
        self.main_window.current_payment_id = -1
        self.main_window.switchWidget(self.central_widget.currentIndex() - 1)


class TabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.main_window = self.parent().parent()
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.payments_tab = PaymentsWidget(parent=self)
        self.transactions_tab = TransactionsWidget(parent=self)
        self.tabs.resize(300,200)
        self.tabs.addTab(self.payments_tab, "Payments")
        self.tabs.addTab(self.transactions_tab, "Transactions")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    @QtCore.pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
