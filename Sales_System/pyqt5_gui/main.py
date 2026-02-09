"""
销售系统 - PyQt5 GUI 版本
"""
import sys
import os
from PyQt5.QtWidgets import QApplication

from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from data_manager import DataManager


def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_manager = DataManager(base_dir)

    login_dialog = LoginDialog(data_manager)
    if login_dialog.exec_() == LoginDialog.Accepted:
        main_window = MainWindow(data_manager, login_dialog.current_user)
        main_window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
