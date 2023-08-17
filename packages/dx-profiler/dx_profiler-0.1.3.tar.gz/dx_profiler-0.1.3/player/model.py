from collections import defaultdict

import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class VideoPlayerModel(QObject):
    frame_changed = pyqtSignal(QPixmap)
    progress_changed = pyqtSignal(int)
    play_state_changed = pyqtSignal(bool)

    @property
    def cap(self):
        return self._cap
    
    @cap.setter
    def cap(self, cap):
        if cap is None:
            return
        self._cap = cap

        self._fps = int(self._cap.get(cv2.CAP_PROP_FPS))
        self._total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._now_frame = 0

        self._origin_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._origin_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    @property
    def now_frame(self):
        return self._now_frame
    
    @now_frame.setter
    def now_frame(self, now_frame):
        self._now_frame = now_frame
        self.progress_changed.emit(self._now_frame)

    @property
    def video_out(self):
        return self._video_out
    
    @video_out.setter
    def video_out(self, video_out):
        self._video_out = video_out
    
    @property
    def drawing(self):
        return self._drawing
    
    @drawing.setter
    def drawing(self, drawing):
        self._drawing = drawing
    
    @property
    def save_path(self):
        return self._save_path
    
    @save_path.setter
    def save_path(self, save_path):
        self._save_path = save_path

    @property
    def pixmap(self):
        return self._pixmap

    @pixmap.setter
    def pixmap(self, pixmap):
        self._pixmap = pixmap
        self.frame_changed.emit(self._pixmap)
    
    @property
    def data(self):
        return self._data
    
    
    @data.setter
    def data(self, data):
        self._data = data
    
    def playing(self):
        if self._save_path is None:
            self._playing = not self._playing
                
            if self._playing:
                self.timer.start(1000 // self._fps)
            else:
                self.timer.stop()
            
            self.play_state_changed.emit(self._playing)         

    def __init__(self) -> None:
        super().__init__()

        self._cap = None
        self._fps = 1
        self._total_frames = 1
        self._origin_width = 1
        self._origin_height = 1

        self._now_frame = 0
        self.video_out = None

        self._drawing = "bbox"
        self._save_path = None

        self._playing = False
        self.timer = QTimer()

        self._data = defaultdict(list)

        self._pixmap = None

        self.cv2_options = {'RED': (255, 0, 0),
                            'GREEN': (0, 255, 0),
                            'BLUE': (0, 0, 255),
                            'font': cv2.FONT_HERSHEY_SIMPLEX}