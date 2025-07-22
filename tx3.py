from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QAction, QFileDialog, QStatusBar, QMenuBar, QMenu
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont
import sys
import cv2
import numpy as np
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Real Time')
        
        self.button = QPushButton('Real-Time', self)
        self.button.move(100, 100)
        self.button.clicked.connect(self.show_real)

        self.button1 = QPushButton('Video', self)
        self.button1.move(100, 140)
        self.button1.clicked.connect(self.show_video)

        # Menu bar
        self.createMenuBar()
        
        self.w = None
        self.x = None
        self.y = None

        self.show()

    def createMenuBar(self):
        aboutAct = QAction('About', self)
        aboutAct.setShortcut('Ctrl+1')
        aboutAct.setStatusTip('About Page')
        aboutAct.triggered.connect(self.show_about)

        helpAct = QAction('Help', self)
        helpAct.setShortcut('Ctrl+2')
        helpAct.setStatusTip('Help Page')
        helpAct.triggered.connect(self.show_help)

        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Files')
        fileMenu.addAction(aboutAct)
        fileMenu.addAction(helpAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

    def show_real(self):
        global custom_video_source
        custom_video_source = 0
        if self.y is None:
            self.y = RealTime()
        self.y.show()

    def show_video(self):
        global custom_video_source
        custom_video_source = str(self.openFileNameDialog())
        if self.y is None:
            self.y = RealTime()
        self.y.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        return fileName

    def show_about(self):
        if self.w is None:
            self.w = About()
        self.w.show()

    def show_help(self):
        if self.x is None:
            self.x = Help()
        self.x.show()


class RealTime(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 840)
        self.setWindowTitle('Human Activity Recognition')
        self.setMinimumSize(QSize(1000, 840))
        self.setMaximumSize(QSize(1000, 840))
        self.initUI()

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.label_2.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def initUI(self):
        self.label = QLabel(self)
        self.label.setText("Real Time Recognition")
        self.label.setGeometry(0, 20, 1000, 41)
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.label_2 = QLabel(self)
        self.display_width = 960
        self.display_height = 720
        self.label_2.setGeometry(
            20, 80, self.display_width, self.display_height)
        self.label_2.setFrameShape(QLabel.WinPanel)
        self.label_2.setLineWidth(0)
        self.label_2.setText("")
        self.label_2.resize(self.display_width, self.display_height)
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.show()

    def closeEvent(self, event):
        cv2.destroyAllWindows()
        event.accept()


class About(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle('About Page')
        self.setGeometry(0, 0, 640, 360)
        self.setMinimumSize(QSize(640, 360))
        self.setMaximumSize(QSize(640, 360))

        self.label = QLabel(self)
        self.label.setText("About")
        self.label.setGeometry(0, 10, 641, 41)
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(20, 70, 151, 191)
        self.label_2.setPixmap(QPixmap(
            "img\Image1.jpg"))
        self.label_2.setFrameShape(QLabel.WinPanel)
        self.label_2.setScaledContents(True)

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(190, 70, 431, 261)
        self.label_3.setFrameShape(QLabel.Panel)
        self.label_3.setText("")
        self.label_3.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(200, 80, 411, 121)
        font = QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setText(
            "The activity recognition app is designed to analyze the input video and classify the identified activities. This app currently supports only one user.")

        self.label_5 = QLabel(self)
        self.label_5.setGeometry(200, 230, 141, 21)
        font = QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setText("Authors:")

        self.label_6 = QLabel(self)
        self.label_6.setGeometry(200, 250, 221, 31)
        font = QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setText("John Doe\nJane Smith")

        self.show()


class Help(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Help Page')
        self.setGeometry(0, 0, 640, 360)
        self.setMinimumSize(QSize(640, 360))
        self.setMaximumSize(QSize(640, 360))

        self.label = QLabel(self)
        self.label.setText("Help")
        self.label.setGeometry(0, 10, 641, 41)
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(20, 70, 601, 261)
        self.label_2.setFrameShape(QLabel.Panel)
        self.label_2.setText("")
        self.label_2.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(30, 80, 571, 181)
        font = QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)
        self.label_3.setText(
            "This application helps to classify human activities in real-time. To use the real-time feature, simply click on the 'Real-Time' button. For video classification, click on the 'Video' button and select a video file. For more information, refer to the documentation.")

        self.show()


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(custom_video_source)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            time.sleep(0.1)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
