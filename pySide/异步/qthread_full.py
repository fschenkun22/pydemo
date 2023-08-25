import time
from PySide6.QtCore import QThread, Signal, Slot, QSize
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton


class MyThread_1(QThread):
    signal_tuple = Signal(tuple)
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            time.sleep(1)
            # 当前时间戳
            timestamp = time.time()
            self.signal_tuple.emit((timestamp, '子线程里完成，我自定义'))
            print('子线程运行时')

class MyThread_2(QThread):
    signal_tuple = Signal(tuple)
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            time.sleep(3)
            # 当前时间戳
            timestamp = time.time()
            self.signal_tuple.emit((timestamp, '这里是mythred2有信号时'))
            print('子线程运行时')

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.button.clicked.connect(self.setup_thread_1)
        self.button2.clicked.connect(self.setup_thread_2)
        self.button3.clicked.connect(self.terminate_1)
        self.button4.clicked.connect(self.terminate_2)


    def setup_ui(self):
        self.setWindowTitle("My App")
        self.resize(QSize(400, 300))
        layout = QVBoxLayout()
        self.label = QLabel("0")
        
        layout.addWidget(self.label)
        self.label2 = QLabel("0")
        layout.addWidget(self.label2)

        self.button = QPushButton("Send Request")
        layout.addWidget(self.button)
        self.button2 = QPushButton("Send Request2")
        layout.addWidget(self.button2)
        self.button3 = QPushButton("stop")
        layout.addWidget(self.button3)
        self.setLayout(layout)
        self.button4 = QPushButton("stop2")
        layout.addWidget(self.button4)
        self.setLayout(layout)


    def setup_thread_1(self):
        self.thread_1 = MyThread_1()
        self.thread_1.signal_tuple.connect(self.thread_1_finished)
        self.thread_1.start()

    def setup_thread_2(self):
        self.thread_2 = MyThread_2()
        self.thread_2.signal_tuple.connect(self.thread_2_finished)
        self.thread_2.start()

    # 终止进程
    def terminate_1(self):
        self.thread_1.terminate()
    
    def terminate_2(self):
        self.thread_2.terminate()

    @Slot(tuple)
    def thread_1_finished(self, item):
        print('接收到子线程1结束信号:',item)
        self.label.setText('this is a lable'+str(item))
    
    @Slot(tuple)
    def thread_2_finished(self, item):
        print('接收到子线程2结束信号:',item)
        self.label2.setText('this is a lable2'+str(item))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
