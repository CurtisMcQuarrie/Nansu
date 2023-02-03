"""

This module provides Nansu application.

"""

import sys
from PyQt5.QtWidgets import QApplication

from .database import createConnection
from .views import MainWindow


def main():
    """
    Nansu main function
    """
    # create application
    nansu_app = QApplication([])
    # connect to the database
    if not createConnection("transactions.sqlite"):
        sys.exit(1)
    # create main window
    window = MainWindow()
    window.show()
    # run event loop
    sys.exit(nansu_app.exec())
