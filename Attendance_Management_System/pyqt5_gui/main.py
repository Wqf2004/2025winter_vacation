"""
出勤管理系统 - PyQt5桌面版
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager
from ui.main_window import run

if __name__ == '__main__':
    run()
