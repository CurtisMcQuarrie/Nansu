from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation
from enum import Enum


# class TransactionField(Enum):
#     Id = 0
#     Amount = 1
#     Unit = 2
#     PaidDate = 3
#     DueDate = 4
#     Payment = 5


# class TransactionsModel:
#     def __init__(self):
#         self.model = self._createModel()

#     @staticmethod
#     def _createModel():
#         """
#         create and set up model
#         """
#         tableModel = QSqlRelationalTableModel()
#         tableModel.setTable("transactions")
#         tableModel.setRelation(
#             TransactionField.Payment.value, 
#             QSqlRelation("payments", "id", "description")
#         )
#         tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
#         tableModel.select()
#         headers = ("ID", "Amount", "Unit", "PaidDate", "DueDate", "Payment")
#         for columnIndex, header in enumerate(headers):
#             tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
#         tableModel.setSort(TransactionField.DueDate.value, Qt.AscendingOrder)

#         return tableModel

#     def addTransaction(self, data):
#         """
#         add a transaction to the database
#         """
#         rows = self.model.rowCount()
#         self.model.insertRows(rows, 1)

#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 TransactionField.Amount.value
#             ), data[0]
#         )
#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 TransactionField.Date.value
#             ), data[1]
#         )
#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 TransactionField.Description.value
#             ), data[2]
#         )

#         self.model.submitAll()
#         self.model.setSort(TransactionField.DueDate.value, Qt.AscendingOrder)
#         self.model.select()

#     def deleteTransaction(self, row):
#         """
#         remove a transaction from the database
#         """
#         self.model.removeRow(row)
#         self.model.submitAll()
#         self.model.setSort(TransactionField.DueDate.value, Qt.AscendingOrder)
#         self.model.select()

#     def clearTransactions(self):
#         """
#         remove all transactions from the database
#         """
#         self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
#         self.model.removeRows(0, self.model.rowCount())
#         self.model.submitAll()
#         self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
#         self.model.setSort(TransactionField.DueDate.value, Qt.AscendingOrder)
#         self.model.select()


# class PaymentField(Enum):
#     Id = 0
#     CreateDate = 1
#     StartDate = 2
#     EndDate = 3
#     Frequency = 4
#     Description = 5
#     Account = 6


# class Frequency(Enum):
#     Daily = 0
#     Weekly = 1
#     BiWeekly = 2
#     Monthly = 3
#     SemiAnnually = 4
#     Annually = 5


# class PaymentModel:
#     def __init__(self):
#         self.model = self._createModel()

#     @staticmethod
#     def createModel():
#         """
#         create and set up model
#         """
#         tableModel = QSqlRelationalTableModel()
#         tableModel.setTable("payments")
#         model.setRelation(
#             PaymentField.Payment.value,
#             QSqlRelation("accounts", "id", "name")
#         )
#         tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
#         tableModel.select()
#         headers = ("ID", "CreateDate", "StartDate", "EndDate", "Frequency", "Description", "PaymentID")
#         for columnIndex, header in enumerate(headers):
#             tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
#         tableModel.setSort(PaymentField.StartDate.value, Qt.AscendingOrder)

#         return tableModel

#     def addPayment(self, data):
#         """
#         add an account to the database
#         """
#         rows = self.model.rowCount()
#         self.model.insertRows(rows, 1)

#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 PaymentField.StartDate.value
#             ), data[0]
#         )
#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 PaymentField.EndDate.value
#             ), data[1]
#         )
#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 PaymentField.Frequency.value
#             ), data[2]
#         )
#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 PaymentField.Description.value
#             ), data[3]
#         )
#         self.model.setData(
#             self.model.index(
#                 rows, 
#                 PaymentField.Account.value
#             ), data[4]
#         )

#         self.model.submitAll()
#         self.model.setSort(PaymentField.Id.value, Qt.AscendingOrder)
#         self.model.select()

# def deletePayment(self, row):
#         """
#         remove an account from the database
#         """
#         self.model.removeRow(row)
#         self.model.submitAll()
#         self.model.setSort(AccountField.Id.value, Qt.AscendingOrder)
#         self.model.select()

#     def clearPayment(self):
#         """
#         remove all accounts from the database
#         """
#         self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
#         self.model.removeRows(0, self.model.rowCount())
#         self.model.submitAll()
#         self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
#         self.model.setSort(AccountField.Id.value, Qt.AscendingOrder)
#         self.model.select()


class AccountField(Enum):
    Id = 0
    CreateDate = 1
    Name = 2


class AccountsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """
        create and set up model
        """
        tableModel = QSqlTableModel()
        tableModel.setTable("accounts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "CreateDate", "Name")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        tableModel.setSort(AccountField.Id.value, Qt.AscendingOrder)

        return tableModel

    def addAccount(self, data):
        """
        add an account to the database
        """
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        self.model.setData(
            self.model.index(
                rows, 
                AccountField.Name.value
            ), data[0]
        )

        self.model.submitAll()
        self.model.setSort(AccountField.Id.value, Qt.AscendingOrder)
        self.model.select()

    def deleteAccount(self, row):
        """
        remove an account from the database
        """
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.setSort(AccountField.Id.value, Qt.AscendingOrder)
        self.model.select()

    def clearAccounts(self):
        """
        remove all accounts from the database
        """
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setSort(AccountField.Id.value, Qt.AscendingOrder)
        self.model.select()
