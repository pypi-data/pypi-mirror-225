from nats.aio.client import Client as Nats
from nats.errors import TimeoutError
import json
import asyncio

from inference.file_writer import FileWriter
class NatsListener:
    def __init__(self, file_writer: FileWriter, nats_uri: str = 'nats://localhost:4222', 
                       subject: str = 'inference.result.profile'):
        self.nc = Nats()

        self.nats_uri = nats_uri
        self.subject = subject
        self.file_writer = file_writer
    
    async def connect(self):
        await self.nc.connect(self.nats_uri)
        self.sub = await self.nc.subscribe(self.subject)

    async def record(self) -> None:
        while not self.file_writer.is_closed():
            try:
                msg = await self.sub.next_msg(timeout=10)
            except TimeoutError as e:
                await asyncio.sleep(0)
                continue
            except Exception as e:
                print(e)
                break

            msg = json.loads(msg.data)
            self.file_writer.write(str(msg))
