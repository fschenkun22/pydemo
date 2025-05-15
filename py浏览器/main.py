import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtWebKitWidgets import QWebView, QWebPage

class CustomWebPage(QWebPage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def certificateError(self, error):
        error.ignore()
        return True

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.resize(1920, 1080)  # 设置主窗口大小为1920x1080

        self.browser_container = QWidget()
        self.browser_layout = QVBoxLayout(self.browser_container)

        self.browser = QWebView(self.browser_container)
        self.browser.setPage(CustomWebPage(self))
        self.browser.setUrl(QUrl("https://ns2.alphagm.top:65168/2411/2411bxyqemsd_page/"))

        self.browser_layout.addWidget(self.browser)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)

        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.browser_container)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())