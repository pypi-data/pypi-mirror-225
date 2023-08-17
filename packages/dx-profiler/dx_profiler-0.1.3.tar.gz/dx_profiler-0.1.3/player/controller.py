import cv2
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from .view import VideoPlayer
from .model import VideoPlayerModel

VIDEO_EXTENSIONS = [".avi", ".mp4", ".mov"]


class VideoPlayerController(QObject):
    def __init__(self,
                model: VideoPlayerModel,
                view: VideoPlayer,
                video_path: str,
                record: str,
                st_time_stamp: int,
                drawing: str = 'bbox',
                save_path: str = None,
                ):
        super().__init__()

        self._model = model
        self._view = view
        self._background = True if view is None else False
        
        self._model.cap = None
        self._model.video_out = None
        self._model.drawing = drawing
        self._model.save_path = save_path

        file_ext = video_path[video_path.rfind("."):]

        if file_ext not in VIDEO_EXTENSIONS:
            raise ValueError("Not supported video format")
        
        self._model.cap = cv2.VideoCapture(video_path)

        if not self._model.cap.isOpened():
            raise ValueError("Can't open video file")
        
        if not self._background:
            self._view.progress_bar.setMaximum(self._model._total_frames)
        self.data_preprocessing(record, st_time_stamp)
        self.connect_signals()
        self.toggle_play()
    
    def data_preprocessing(self, record: str, st_time_stamp: int):
        for line in record:
            line_data = eval(line)
            time_in_seconds = (line_data["metadata"]["timestamp"] / 1e9) - st_time_stamp
            frame_num = int(time_in_seconds * self._model._fps)
            self._model.data[frame_num].append(line_data["objects"])

        if self._background:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self._model.video_out = cv2.VideoWriter(self._model.save_path,
                                                    fourcc,
                                                    self._model._fps,
                                                    (self._model._origin_width,
                                                    self._model._origin_height),
                                                    )
 
    def toggle_play(self):
        self._model.playing()
    
    @pyqtSlot(int)
    def move_frame(self, frame_num: int):
        self._model.now_frame += frame_num
        self._model.cap.set(cv2.CAP_PROP_POS_FRAMES, self._model.now_frame)
        self.update_frame()
    
    @pyqtSlot(int)
    def set_frame(self, frame_num: int):
        self._model.now_frame = frame_num - 1
        self._model.cap.set(cv2.CAP_PROP_POS_FRAMES, self._model.now_frame)
        self.update_frame()
    
    @pyqtSlot()
    def update_frame(self):
        ret, frame = self._model.cap.read()
        self._model.now_frame += 1

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            H, W, CH = frame.shape

            if self._background:
                window_width = self._model._origin_width
                window_height = self._model._origin_height
            
            else:
                window_width = self._view.video_label.width()
                window_height = self._view.video_label.height()
                
            frame = cv2.resize(frame, (window_width, window_height))

            if self._model.now_frame in self._model.data:
                data = self._model.data[self._model.now_frame]
                
                RED = self._model.cv2_options["RED"]
                GREEN = self._model.cv2_options["GREEN"]
                font = self._model.cv2_options["font"]


                for datum_ in data:
                    for datum in datum_:
                        bbox = datum[self._model.drawing]
                        x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]
                        x, y, w, h = x * window_width, \
                                     y * window_height, \
                                     w * window_width, \
                                     h * window_height

                        if datum["id"] >= 10000:
                            datum["id"] = -1

                        x, y, w, h = map(int, [x, y, w, h])
                        cv2.rectangle(frame, (x, y), (x + w, y + h), RED, 3)

                        if datum["id"] != -1:
                            cv2.putText(frame, f"[{datum['id']}] {datum['label']}", (x, y-10), font, 1, GREEN, 2)
                        else:
                            cv2.putText(frame, f"[None] {datum['label']}", (x, y - 10), font, 1, GREEN, 2)

                        drawing_texts = []

                        if "classifiers" in datum:
                            for idx, val in enumerate(datum["classifiers"]):
                                drawing_texts.append(f"[{val['label']}] {val['type']}")

                        if "score_d" in datum:
                            drawing_texts.append(f"Score: {datum['score_d']:.2f}")

                        for idx, val in enumerate(drawing_texts):
                            cv2.putText(frame, val, (x, y + (idx+1)*25), font, 1, GREEN, 2)

            if self._background:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self._model.video_out.write(frame)
            
            else:
                bytes_per_line = CH * window_width
                q_image = QImage(frame.data, window_width, window_height, bytes_per_line, QImage.Format_RGB888)
                self._model.pixmap = QPixmap.fromImage(q_image)

        else:
            self._model._playing = False
            self._model.cap.release()
            
            if self._background:
                self.out.release()
            else:
                self._view.close()
    
    def connect_signals(self):
        self._model.timer.timeout.connect(self.update_frame)
        
        if not self._background:
            self._model.frame_changed.connect(self._view.on_frame_changed)
            self._model.progress_changed.connect(self._view.on_progress_changed)
            self._model.play_state_changed.connect(self._view.on_play_state_changed)


            self._view.cap_changed.connect(self.move_frame)
            self._view.progress_bar.clicked.connect(self.set_frame)
            self._view.toggle_changed.connect(self.toggle_play)
            self._view.play_button.clicked.connect(self.toggle_play)