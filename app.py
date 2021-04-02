from PyQt5 import QtWidgets
from downloader import Ui_MainWindow
import download
import time
from ticker import stopWatch


class DownloadApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        h = 332
        w = 388

        self.setFixedSize(w, h)

        self.pushButton.pressed.connect(self.add_queue)

    def add_queue(self):
        start = time.time()
        # self.lineEdit.setText('http://tiktok.mix.tj/video/7/46/6034ec9eca6a4.mp4')
        self.lineEdit.setText('https://mobile-review.com/articles/2020/image/skillfactory-python/3.jpg')
        url = self.lineEdit.text()
        file_name = self.lineEdit_2.text()
        resp = download.add_queue(url)
        if resp['code'] != 200:
            self.textBrowser.append('error: ' + str(resp['code']))
            self.textBrowser.append('')
        else:
            self.textBrowser.append(str(resp['payload']))
            self.textBrowser.append('')

        # self.lineEdit.clear()
        a = download.download(file_name, url, resp['payload'])

        end = time.time()
        d, h, m, s = stopWatch(end - start)

        self.textBrowser.append('days: ' + str(d) + ' hours: ' + str(h) +
                                ' minute: ' + str(m) + ' second: ' + str(s))
        self.textBrowser.append('')
        self.textBrowser.append(str(a))


app = QtWidgets.QApplication([])
window_main = DownloadApp()
window_main.show()
app.exec()
