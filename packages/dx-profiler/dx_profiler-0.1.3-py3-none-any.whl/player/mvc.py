import sys

from tqdm import tqdm
from PyQt5.QtWidgets import QApplication

from model import VideoPlayerModel
from view import VideoPlayer
from controller import VideoPlayerController


def main():
    save_path = "daki.mp4"
    save_mode = False if save_path is None else True

    with open("./last.txt", "r") as f:
        video_path = f.readline().strip()
        st_time_stamp = int(f.readline().strip())
        record = f.readlines()

    model = VideoPlayerModel()
    view = None
    
    if not save_mode:
        app = QApplication(sys.argv)
        view = VideoPlayer()

    controller = VideoPlayerController(model,
                                        view,
                                        video_path=video_path,
                                        record=record,
                                        st_time_stamp=st_time_stamp,
                                        drawing='bboxd',
                                        save_path=save_path)
    if not save_mode:
        view.show()
        sys.exit(app.exec_())
    
    else:
        for i in tqdm(range(model._total_frames), desc="Saving", unit="frame"):
            controller.update_frame()        


if __name__ == "__main__":
    main()