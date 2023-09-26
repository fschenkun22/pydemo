
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QThread, Signal, Slot, QSize


class MyWindow(QWidget):
    
    send_msg = Signal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        



    def initUI(self):        


        self.setWindowTitle("My Window")
        self.setGeometry(300, 300, 300, 400)
        
        self.btnCls = QPushButton("send to ", self)
        self.btnCls.clicked.connect(lambda: self.sub.close())

        self.btnOpen = QPushButton("Open Sub Window", self)
        self.btnOpen.move(0, 30)
        self.btnOpen.clicked.connect(lambda: self.sub.show())
        self.show() 
        self.bind()
        self.sendval("Hello World")
    
    def bind(self):
        self.sub = SubWindow()
        self.sub.show()
        self.send_msg.connect(self.sub.lineEdit.setText)

    def sendval (self, val):
        self.send_msg.emit(val)



class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lineEdit = QLineEdit(self)
        self.setWindowTitle("Sub Window")
        self.setGeometry(300, 300, 300, 400)
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    app.exec_()