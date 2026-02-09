"""
俄罗斯方块游戏 - PyQt5桌面版
主程序入口
"""
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import TetrisGame


def main():
    app = QApplication(sys.argv)
    game = TetrisGame()
    game.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
