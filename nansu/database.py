from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def _createTransactionsTable():
    """
    Create the transactions table in the database
    """
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            amount INTEGER NOT NULL,
            unit VARCHAR(40) NOT NULL DEFAULT 'CAD$',
            paidDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            dueDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            paymentID INTEGER NOT NULL,
            FOREIGN KEY (paymentID) REFERENCES payments (id) 
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """
    )


def _createPaymentsTable():
    """
    Create the payments table in the database
    """
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            createDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            startDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            endDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            frequency VARCHAR(40) NOT NULL DEFAULT 'Daily',
            description VARCHAR(128),
            accountID INTEGER NOT NULL,
            FOREIGN KEY (accountID) REFERENCES accounts (id) 
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """
    )


def _createAccountsTable():
    """
    Create the accounts table in the database
    """
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            createDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            name VARCHAR(63) NOT NULL DEFAULT 'Chequing'
        )
        """
    )


def createConnection(databaseName):
    """
    Create and open a database connection
    """
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "Nansu Transaction",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    _createAccountsTable()
    _createPaymentsTable()
    _createTransactionsTable()
    return True
