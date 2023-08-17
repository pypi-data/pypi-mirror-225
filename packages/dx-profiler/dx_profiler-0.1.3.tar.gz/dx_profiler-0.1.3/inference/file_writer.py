from pathlib import Path

class FileWriter:
    def __init__(self, file: Path, video_path: Path, start_timestamp: int) -> None:
        self.f = open(file, 'w')
        self.f.write(str(video_path) + '\n')
        self.f.write(str(start_timestamp) + '\n')
    
    def write(self, text: str, end: str = '\n') -> None:
        self.f.write(text + end)
    
    def close(self) -> None:
        if not self.f.closed:
            self.f.close()
    
    def is_closed(self) -> bool:
        return self.f.closed

    def __del__(self):
        self.f.close()
