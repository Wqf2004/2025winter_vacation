"""
主程序入口
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog
from data_manager import DataManager
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_manager = DataManager(base_dir)

    # 登录
    login_dialog = LoginDialog(data_manager)
    if login_dialog.exec_() == QDialog.Accepted:
        # 显示主窗口
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
