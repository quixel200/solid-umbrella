#!/usr/bin/env python
import os
import sys
import ctypes
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QStackedWidget, QMessageBox
from PySide6.QtCore import Slot, QTimer, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from dashboard import Dashboard  
from PySide6.QtWebEngineWidgets import QWebEngineView


def is_admin():
    """Return True if the user has administrative/root privileges, False otherwise."""
    if os.name == 'nt':  
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except AttributeError:
            return False  
    else:
        return os.geteuid() == 0


def ensure_admin_privileges():
    """Ensure the application is running with admin privileges; if not, attempt to restart as admin."""
    if os.name == 'nt' and not ctypes.windll.shell32.IsUserAnAdmin():
        app = QApplication(sys.argv)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Admin Access Required")
        msg_box.setText("This application needs to be run as an administrator. Click OK to restart as admin.")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        if msg_box.exec() == QMessageBox.Ok:
            params = ' '.join([f'"{arg}"' for arg in sys.argv])  
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)  
        else:
            sys.exit("User opted not to run with admin privileges.")


class MainWindow(QMainWindow):
    """Main application window that displays access level information and embedded HTML reports."""
    def __init__(self, admin_access):
        super().__init__()
        self.setWindowTitle("Dashboard")

     
        self.setGeometry(100, 100, 1200, 700)

        main_layout = QHBoxLayout()
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

      
        self.stack = QStackedWidget()

       
        dashboard = Dashboard()

        
        self.generate_report_page = QWidget()
        generate_report_layout = QVBoxLayout()
        self.generate_report_view = QWebEngineView()
        self.generate_report_view.setStyleSheet("background-color: white;")
        generate_report_layout.addWidget(self.generate_report_view)
        self.generate_report_page.setLayout(generate_report_layout)

        self.remediation_page = QWidget()
        remediation_layout = QVBoxLayout()
        self.remediation_view = QWebEngineView()
        self.remediation_view.setStyleSheet("background-color: white;")
        remediation_layout.addWidget(self.remediation_view)
        self.remediation_page.setLayout(remediation_layout)

    
        self.stack.addWidget(dashboard)               
        self.stack.addWidget(self.generate_report_page)  
        self.stack.addWidget(self.remediation_page)      

        button1 = QPushButton("Dashboard")
        button2 = QPushButton("Generate Report")
        button3 = QPushButton("Remediation")

        button1.clicked.connect(lambda: self.change_page(0))
        button2.clicked.connect(self.load_generate_report)
        button3.clicked.connect(self.load_remediation_report)

        sidebar_layout.addWidget(button1)
        sidebar_layout.addWidget(button2)
        sidebar_layout.addWidget(button3)
        sidebar_layout.addStretch(1)

        button1.setCheckable(True)
        button2.setCheckable(True)
        button3.setCheckable(True)
        button1.setAutoExclusive(True)
        button2.setAutoExclusive(True)
        button3.setAutoExclusive(True)

        sidebar.setMinimumWidth(185)
        sidebar.setMaximumWidth(300)
        sidebar.setStyleSheet(
            "QWidget{background-color:#3399ff;color:white;margin:0;padding:0}\n"
            "QPushButton{border-radius:20px;padding:20px;font-size:16px} "
            "QPushButton:checked{background-color:#FFFFFF;color:#1F95EF}"
        )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        access_label = QLabel(f"Access Level: {'Administrator' if admin_access else 'Standard User'}")
        access_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;" if admin_access else "font-size: 18px; font-weight: bold; color: red;")

        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.addWidget(access_label)
        main_vertical_layout.addLayout(main_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_vertical_layout)
        self.setCentralWidget(central_widget)

       
        QTimer.singleShot(3000, access_label.hide)

    @Slot()
    def change_page(self, index):
        """Switch to the page at the given index in the stack."""
        self.stack.setCurrentIndex(index)

    @Slot()
    def load_generate_report(self):
        """Load the merged report HTML into the Generate Report page and run rep.py in the background."""
    
        # Ensure any previous report (newone.html) is removed before running rep.py
        report_file = os.path.abspath('newone.html')
        if os.path.exists(report_file):
            os.remove(report_file)

        # Run rep.py in the background using subprocess
        subprocess.Popen(['python', 'rep.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the report to be generated, or implement a better check if necessary
        # Create a QWebEngineView widget to display the HTML content
        report_view = QWebEngineView()

        # Load the generated report (newone.html) into the QWebEngineView
        report_view.setUrl(QUrl.fromLocalFile(report_file))

        # Add the report_view to your layout or window
        # Assuming self.layout is your current layout, or use the appropriate parent widget or layout:
        self.layout.addWidget(report_view)  # You can replace 'self.layout' with your actual layout
    
        # Change the page to show the report in the same window (instead of navigating away)
        self.change_page(1)

    @Slot()
    def load_remediation_report(self):
        """Load the remediation report HTML into the Remediation page and apply red-issue filtering."""
        report_path = QUrl.fromLocalFile(os.path.abspath('remnew.html'))
        self.remediation_view.setUrl(report_path)
        self.apply_red_filter()
        self.change_page(2)

    def apply_red_filter(self):
        """Inject JavaScript to show only red-colored issues in the HTML."""
        script = """
        document.querySelectorAll('body *').forEach(el => {
            if (window.getComputedStyle(el).color !== 'rgb(255, 0, 0)') { 
                el.style.display = 'none'; 
            }
        });
        """
        self.remediation_view.page().runJavaScript(script)


if __name__ == "__main__":
    ensure_admin_privileges()
    admin_access = is_admin()
    app = QApplication(sys.argv)
    window = MainWindow(admin_access)
    window.resize(1200, 700)
    window.show()
    sys.exit(app.exec())
