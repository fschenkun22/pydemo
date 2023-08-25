from PySide6.QtWidgets import QApplication,QWidget, QMainWindow, QPushButton
from Ui_calculator import Ui_MainWindow

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bind()
        self.res = ''
        
    def bind(self):
        self.ui.pushButton_0.clicked.connect(lambda: self.addNum('0'))
        self.ui.pushButton_1.clicked.connect(lambda: self.addNum('1'))
        self.ui.pushButton_2.clicked.connect(lambda: self.addNum('2'))
        self.ui.pushButton_3.clicked.connect(lambda: self.addNum('3'))
        self.ui.pushButton_4.clicked.connect(lambda: self.addNum('4'))
        self.ui.pushButton_5.clicked.connect(lambda: self.addNum('5'))
        self.ui.pushButton_6.clicked.connect(lambda: self.addNum('6'))
        self.ui.pushButton_7.clicked.connect(lambda: self.addNum('7'))
        self.ui.pushButton_8.clicked.connect(lambda: self.addNum('8'))
        self.ui.pushButton_9.clicked.connect(lambda: self.addNum('9'))
        self.ui.pushButton_add.clicked.connect(lambda: self.addNum('+'))
        self.ui.pushButton_count.clicked.connect(self.count)
        
    def addNum (self,num):
        self.res += num
        self.ui.textEdit.setText(self.res)

    def count (self):
        self.ui.textEdit.setText(str(eval(self.res)))
        self.res = ''
        

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()