import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import QObject, Signal,QTimer
import time

class MySignal(QObject):
    # Define a signal with no arguments
    my_signal = Signal(str)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        qfui = QFile('./start1.ui')
        qfui.open(QFile.ReadOnly)
        qfui.close()

        self.ui = QUiLoader().load(qfui)
        # 绑定槽
        self.ui.pushButton.clicked.connect(self.on_button_click)
        # self.ui.textEdit.append("hello world")
                # Create an instance of the signal
        self.my_signal = MySignal()
        # Connect the signal to a slot
        self.my_signal.my_signal.connect(self.slot_function)

        # Create a timer to emit the signal every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.emit_signal)
        self.timer.start(2000)


    def on_button_click(self):
        print("Button clicked1111!")
        print(f"Text in text box: ")
        self.ui.textEdit.append("hello world")
        self.my_signal.my_signal.emit()

    def slot_function(self):
        print("Signal received!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    sys.exit(app.exec())
