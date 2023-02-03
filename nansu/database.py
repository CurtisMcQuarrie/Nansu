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
            dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
            date DATETIME NOT NULL,
            description VARCHAR(255)
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

    _createTransactionsTable()
    return True
