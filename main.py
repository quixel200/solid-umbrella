#!/usr/bin/env python
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot
from components.dashboard import Dashboard
import ctypes
import sys
import os

def check_privileges(app):
    """Check for administrative privileges based on the operating system."""
    if os.name == 'nt':  # Windows
        if not ctypes.windll.shell32.IsUserAnAdmin():
            QMessageBox.critical(
                None,
                "Permission Error",
                "This application requires administrative privileges. Please run as administrator."
            )
            sys.exit(1)
    else:  # Assuming Linux or other POSIX systems
        if os.geteuid() != 0:  # Check if running as root
            QMessageBox.critical(
                None,
                "Permission Error",
                "This application requires root privileges. Please run as root."
            )
            sys.exit(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        main_layout = QHBoxLayout()

        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        self.stack = QStackedWidget()

        dashboard = Dashboard()
        page2 = QWidget()
        page2.setLayout(QVBoxLayout())
        page2.layout().addWidget(QLabel("This is a page 2 test"))

        self.stack.addWidget(dashboard)
        self.stack.addWidget(page2)

        button1 = QPushButton("Dashboard")
        button2 = QPushButton("Settings")

        button1.clicked.connect(lambda: self.change_page(0))
        button2.clicked.connect(lambda: self.change_page(1))

        sidebar_layout.addWidget(button1)
        sidebar_layout.addWidget(button2)
        sidebar_layout.addStretch(1)
        button1.setCheckable(True)
        button2.setCheckable(True)
        button1.setAutoExclusive(True)
        button2.setAutoExclusive(True)

        sidebar.setMinimumWidth(185)
        sidebar.setMaximumWidth(300)

        sidebar.setStyleSheet(u"QWidget{background-color:#3399ff;color:white;margin:0;padding:0}\n"
                              "QPushButton{border-radius:20px;padding:20px;font-size:16px}"
                              "QPushButton:checked{background-color:#FFFFFF;color:#1F95EF}")

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    @Slot(int)
    def change_page(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == "__main__":

    app = QApplication(sys.argv)  
    check_privileges(app)
    window = MainWindow() 
    window.resize(1098, 755)
    window.show()
    sys.exit(app.exec())