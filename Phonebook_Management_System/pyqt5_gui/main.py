"""
电话簿管理系统 - PyQt5桌面版
主程序入口
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from data_manager import DataManager
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow


def main():
    """主函数"""
    # 创建应用
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle('Fusion')

    # 创建数据管理器
    data_manager = DataManager()

    # 显示登录对话框
    login_dialog = LoginDialog(data_manager)
    if login_dialog.exec() == LoginDialog.Accepted:
        # 登录成功，显示主窗口
        main_window = MainWindow(data_manager, login_dialog.password)
        main_window.show()
        sys.exit(app.exec_())
    else:
        # 登录失败或取消
        sys.exit(0)


if __name__ == '__main__':
    main()
