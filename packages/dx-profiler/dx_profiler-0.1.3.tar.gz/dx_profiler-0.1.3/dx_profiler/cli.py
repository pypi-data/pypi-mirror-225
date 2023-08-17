import sys
import os
import typer
from typing_extensions import Annotated
from pathlib import Path
from grpc import RpcError
import asyncio
from functools import wraps
from time import time
from shutil import copyfile
from tqdm import tqdm

from inference.inference import InferenceDX
from inference.file_writer import FileWriter
from inference.nats_listener import NatsListener

from PyQt5.QtWidgets import QApplication

from player.model import VideoPlayerModel
from player.view import VideoPlayer
from player.controller import VideoPlayerController

app = typer.Typer()

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    
    return wrapper

@app.command('inference')
@coro
async def cli_inference(file_path: Annotated[Path, typer.Option('-F', '--file', help='Input file path.')],
                  app_path: Annotated[Path, typer.Option('-A', '--app', help='Input app path.')],
                  output_path: Annotated[Path, typer.Option('-O', '--output', help='Store inference result.')]):
    """
    Inference video, save log.
    """
    # 파일 확인
    if not os.geteuid() == 0:
        print('Run with root privileged.')
        raise typer.Exit(-1)

    if not file_path.exists():
        print(f'{file_path} is not exist.')
        raise typer.Exit(-1)
    
    if not app_path.exists():
        print(f'{app_path} is not exist.')
        raise typer.Exit(-1)
    
    if output_path.exists():
        print(f'{output_path} is already exist.')
        raise typer.Exit(-1)

    print(f'input file: {file_path}, app: {app_path}, output file: {output_path}')

    # Inference 시작
    dx_inf = InferenceDX()
    timestamp = int(time())
    
    try:
        dx_inf.ping()
    except RpcError as e:
        print('Start Dx first.')
        raise typer.Exit(-1)
    
    # app id 추출
    app_name = app_path.name
    
    if len(app_name) < 36:
        print('App file must start with uuid.')
        raise typer.Exit(-1)
    
    app_id = app_name[:36]
    
    # install app
    try:
        dx_inf.install_app(app_id, app_path)
    except RpcError as e:
        # 실제로 문제가 있는지, 아니면 app이 이미 인스톨 되어있어 에러가 가는지
        # 확인이 어려워 일단 에러 메시지만 출력하고 넘어감
        print(e)
    
    # video copy
    dx_file_path = Path('/opt/autocare/dx/video').joinpath(file_path.name)
    dx_file_volume_path = Path('/opt/autocare/dx/volume/video').joinpath(file_path.name)
    print(dx_file_path)

    copyfile(file_path, dx_file_path)

    # log writer and nats listener
    log_writer = FileWriter(output_path, file_path, timestamp)
    nats_listener = NatsListener(log_writer)
    await nats_listener.connect()

    write_task = asyncio.create_task(nats_listener.record())
    await asyncio.sleep(0)

    uri = 'file://' + str(dx_file_volume_path)
    print(f'uri: {uri}')
    timestamp = timestamp * 10**6
    print(f'timestamp: {timestamp}')

    # start inference
    try:
        await dx_inf.start_inference(app_id, 'profile', uri, timestamp)
    except RpcError as e:
        print(e)
        dx_inf.clean_up_inference()
        raise typer.Exit(-1)
    except Exception as e:
        print(e)
        dx_inf.clean_up_inference()
        raise typer.Exit(-1)
    
    log_writer.close()
    await asyncio.sleep(0)
    await write_task

    print('Done.')
    

@app.command('profile')
def cli_profile(input_path: Annotated[Path, typer.Option('-F', '--file', help='Input file path.')],
                draw_obj: Annotated[str, typer.Option('-O', '--obj', help='Input object_name "bbox" or "bboxd"')],
                save_path: Annotated[str, typer.Option('-S', '--save', help='Input save video_path')] = None):
    """
    Play video with inference log info.
    """
    # 파일 확인
    if not input_path.exists():
        print(f'{input_path} is not exist.')
        raise typer.Exit(-1)
    
    print(f'input file: {input_path}')

    save_mode = False if save_path is None else True

    with open(input_path, "r") as f:
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
                                        drawing=draw_obj,
                                        save_path=save_path)
    if not save_mode:
        view.show()
        sys.exit(app.exec_())
    
    else:
        for i in tqdm(range(model._total_frames), desc="Saving", unit="frame"):
            controller.update_frame()


if __name__ == '__main__':
    app()
