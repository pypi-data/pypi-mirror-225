from proto_py.dx_pb2_grpc import DetectorStub
from proto_py.dx_pb2 import Empty, AppReq, InferenceReq, Dx

import grpc
from asyncio import sleep

BUF_SIZE = 4096


def file_iterator(app_id: str, file: str):
    with open(file, 'rb') as f:
        while True:
            buf = f.read(BUF_SIZE)
            if len(buf) == 0:
                return
            yield AppReq(app_id=app_id, chunk=buf)


class InferenceDX:
    def __init__(self) -> None:
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = DetectorStub(self.channel)
        self.inf_req = None

    def ping(self) -> None:
        response: Dx = self.stub.GetDx(Empty())
        print(f'Connected to {response.name}')

    def install_app(self, app_id: str, file: str) -> None:
        read_file_iterator = file_iterator(app_id, file)

        response = self.stub.InstallApp(read_file_iterator)

    async def start_inference(self, app_id: str, stream_id: str, uri: str, timestamp: int) -> None:
        # Add inference
        self.inf_req = InferenceReq(
            app_id=app_id, stream_id=stream_id, uri=uri, offset=timestamp)
        result = self.stub.AddInference(self.inf_req)
        print(f'Add inference: {result}')

        while True:
            result = self.stub.GetInferenceStatus(self.inf_req)
            if result.eos or result.err:
                break
            print('Waiting for EOS...')
            await sleep(3)

        result = self.stub.RemoveInference(self.inf_req)
        print(f'Remove Inference: {result}')
        self.inf_req = None

    def clean_up_inference(self) -> None:
        if self.inf_req:
            self.stub.RemoveInference(self.inf_req)
            self.inf_req = None

    def __del__(self) -> None:
        self.channel.close()
