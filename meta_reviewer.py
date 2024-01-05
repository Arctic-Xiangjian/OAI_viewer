import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QProcess

from slice_reviewer import main as slice_main
from art_reviewer import main as art_main



def get_file_path(filename):
    """get the absolute path of the file"""
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, filename)


def create_pyqt_window():
    # 创建一个PyQt应用程序实例
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("OAI Viewer")

    # 创建两个按钮来分别启动slice_reviewer和art_reviewer模块中的GUI
    btn_gui1 = QPushButton('Slice based measure', window)
    btn_gui1.clicked.connect(lambda: QProcess.startDetached('python', [get_file_path('slice_reviewer.py')]))
    btn_gui1.resize(btn_gui1.sizeHint())
    btn_gui1.move(50, 50)

    btn_gui2 = QPushButton('Artary based measure', window)
    btn_gui2.clicked.connect(lambda: QProcess.startDetached('python', [get_file_path('art_reviewer.py')]))
    btn_gui2.resize(btn_gui2.sizeHint())
    btn_gui2.move(50, 100)

    # 设置窗口的大小和位置
    window.setGeometry(300, 300, 300,300)

    # 显示窗口
    window.show()

    # 开始PyQt应用程序的事件循环
    sys.exit(app.exec_())

if __name__ == '__main__':
    create_pyqt_window()
