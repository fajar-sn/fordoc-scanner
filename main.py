import sys

from PySide6.QtWidgets import QApplication

from fordoc_scanner.views.main_window.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.ui.show()

    sys.exit(app.exec())