from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5. QtWidgets import QApplication, QMainWindow, QLabel, \
    QDesktopWidget, QProgressBar, QHBoxLayout, QVBoxLayout, QWidget, QPushButton


class ClickProgressBar(QProgressBar):
    clicked = pyqtSignal(int)

    def mousePressEvent(self, event):
        click_pos = event.pos().x()
        total_width = self.width()
        value = int(self.minimum() + click_pos / total_width * (self.maximum() - self.minimum()))

        self.clicked.emit(value)


class VideoPlayer(QMainWindow):
    cap_changed = pyqtSignal(int)
    toggle_changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.initUI()
        self.setWindowTitle('Dx Profiler')

    def initUI(self) -> None:
        self.video_label = QLabel()
        self.video_label.setScaledContents(True)
        self.video_label.setAlignment(Qt.AlignCenter)

        self.progress_bar = ClickProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)

        self.play_button = QPushButton("II")
        self.play_button.setGeometry(10, 10, 100, 30)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.progress_bar)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        desktop = QDesktopWidget().screenGeometry()
        self.setMinimumSize(800, 600)
        self.setMaximumSize(desktop.width(), desktop.height())
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.toggle_changed.emit()
        
        elif event.key() == Qt.Key_Q:  # 이전 프레임으로 이동
            self.cap_changed.emit(-2)

        elif event.key() == Qt.Key_E:  # 다음 프레임으로 이동
            self.cap_changed.emit(0)

        elif event.key() == Qt.Key_A:
            self.cap_changed.emit(-11)

        elif event.key() == Qt.Key_D:
            self.cap_changed.emit(9)
        
    @pyqtSlot(QPixmap)
    def on_frame_changed(self, pixmap):
        self.video_label.setPixmap(pixmap)
    
    @pyqtSlot(int)
    def on_progress_changed(self, progress):
        self.progress_bar.setValue(progress)
    
    @pyqtSlot(bool)
    def on_play_state_changed(self, playing):
        if playing:
            self.play_button.setText("II")
        else:
            self.play_button.setText("▶")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())