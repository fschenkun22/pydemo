import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


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


    def on_button_click(self):
        print("Button clicked1111!")
        print(f"Text in text box: ")
        self.ui.textEdit.append("hello world")

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    sys.exit(app.exec_())
