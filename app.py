from PyQt5 import QtWidgets
from downloader import Ui_MainWindow


class DownloadApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        h = 332
        w = 388
        self.setFixedSize(w, h)


app = QtWidgets.QApplication([])
window_main = DownloadApp()
window_main.show()
app.exec()
