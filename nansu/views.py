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
        self.accounts_widget = AccountsWidget(parent=self)
        self.payments_widget = PaymentsWidget(parent=self)
        self.transactions_widget = TransactionsWidget(parent=self)
        self.central_widget = QStackedWidget()
        self.central_widget.addWidget(self.accounts_widget)
        self.central_widget.addWidget(self.payments_widget)
        self.central_widget.addWidget(self.transactions_widget)
        self.setCentralWidget(self.central_widget)

    def _createMenu(self):
        """
        create the menu
        """
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def switchWidget(self, index):
        if index == 1:  # go to payments
            self.payments_widget.payments_model.setFilter("accountID", self.current_account_id)
        elif index == 2:  # go to transactions
            self.transactions_widget.transactions_model.setFilter("paymentID", self.current_payment_id)

        self.central_widget.setCurrentIndex(index)


class AccountsWidget(QWidget):
    """
    View for manipulating accounts
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.accounts_model = CustomModel("accounts", ["ID", "CreateDate", "Name"], TableType.NonRelational)
        self.outer_layout = QHBoxLayout()
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
        # self.table.setColumnHidden(0, True)
        # create buttons
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete)
        self.viewButton = QPushButton("View")
        self.viewButton.clicked.connect(self.view)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clear)
        # lay out the GUI
        layout = QVBoxLayout()
        self.inner_layout.addWidget(self.addButton)
        self.inner_layout.addWidget(self.deleteButton)
        self.inner_layout.addStretch()
        self.inner_layout.addWidget(self.viewButton)
        self.inner_layout.addWidget(self.clearAllButton)
        self.outer_layout.addWidget(self.table)
        self.outer_layout.addLayout(self.inner_layout)

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
        self.parent().parent().current_account_id = self.table.model().data(current_index)
        print(self.parent().parent().current_account_id)
        # switch views
        self.parent().parent().switchWidget(self.parent().currentIndex() + 1)


class PaymentsWidget(QWidget):
    """
    View for manipulating accounts
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.payments_model = CustomModel(
            "payments", 
            ["ID", "CreateDate", "StartDate", "EndDate", "Frequency", "Description", "Account"], 
            TableType.Relational
            )
        self.payments_model.setRelation("Account", self.parent().accounts_widget.accounts_model, "ID", "Name")
        self.transactions_model = CustomTransactionModel(  # transaction model for adding new transactions based on new payments
            "transactions", 
            ["ID", "Amount", "Unit", "PaidDate", "DueDate", "Payment"], 
            TableType.Relational
            )
        self.transactions_model.setRelation("Payment", self.payments_model, "ID", "Description")
        self.outer_layout = QHBoxLayout()
        self.inner_layout = QVBoxLayout()
        self._setupUI()
        self.setLayout(self.outer_layout)
        

    def _setupUI(self):
        """
        setup accounts view gui
        """
        # create table view widget
        self.table = QTableView()
        self.table.setModel(self.payments_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnHidden(0, True)
        # create buttons
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete)
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.back)
        self.viewButton = QPushButton("View")
        self.viewButton.clicked.connect(self.view)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clear)
        # lay out the GUI
        layout = QVBoxLayout()
        self.inner_layout.addWidget(self.addButton)
        self.inner_layout.addWidget(self.deleteButton)
        self.inner_layout.addStretch()
        self.inner_layout.addWidget(self.viewButton)
        self.inner_layout.addWidget(self.backButton)
        self.inner_layout.addWidget(self.clearAllButton)
        self.outer_layout.addWidget(self.table)
        self.outer_layout.addLayout(self.inner_layout)

    def openAddDialog(self):
        """
        open the add payment dialog
        """
        dialog = AddPaymentDialog(self.parent().parent().current_account_id, self)
        if dialog.exec() == QDialog.Accepted:
            self.payments_model.add(dialog.data)
            self.transactions_model.addFromPayment(dialog.data)  # add transactions from payment
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
        self.parent().parent().current_payment_id = self.table.model().data(current_index)
        print(self.parent().parent().current_payment_id)
        # switch views
        self.parent().parent().switchWidget(self.parent().currentIndex() + 1)

    def back(self):
        """
        go back to previous index
        """
        self.parent().parent().current_account_id = -1
        print(self.parent().parent().current_account_id)
        self.parent().parent().switchWidget(self.parent().currentIndex() - 1)


class TransactionsWidget(QWidget):
    """
    View for manipulating accounts
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.transactions_model = CustomModel(
            "transactions", 
            ["ID", "Amount", "Unit", "PaidDate", "DueDate", "Payment"], 
            TableType.Relational
            )
        self.transactions_model.setRelation("Payment", self.parent().payments_widget.payments_model, "ID", "Description")
        self.outer_layout = QHBoxLayout()
        self.inner_layout = QVBoxLayout()
        self._setupUI()
        self.setLayout(self.outer_layout)
        

    def _setupUI(self):
        """
        setup accounts view gui
        """
        # create table view widget
        self.table = QTableView()
        self.table.setModel(self.transactions_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnHidden(0, True)
        # create buttons
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete)
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.back)
        self.viewButton = QPushButton("View")
        self.viewButton.clicked.connect(self.view)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clear)
        # lay out the GUI
        layout = QVBoxLayout()
        self.inner_layout.addWidget(self.addButton)
        self.inner_layout.addWidget(self.deleteButton)
        self.inner_layout.addStretch()
        self.inner_layout.addWidget(self.viewButton)
        self.inner_layout.addWidget(self.backButton)
        self.inner_layout.addWidget(self.clearAllButton)
        self.outer_layout.addWidget(self.table)
        self.outer_layout.addLayout(self.inner_layout)

    def openAddDialog(self):
        """
        open the add payment dialog
        """
        dialog = AddPaymentDialog(self.parent().parent().current_payment_id, self)
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
        self.parent().parent().current_payment_id = self.table.model().data(current_index)
        print(self.parent().parent().current_payment_id)
        # switch views
        self.parent().switchWidget(self.parent().currentIndex() + 1)

    def back(self):
        """
        go back to previous index
        """
        self.parent().parent().current_payment_id = -1
        print(self.parent().parent().current_payment_id)
        self.parent().parent().switchWidget(self.parent().currentIndex() - 1)