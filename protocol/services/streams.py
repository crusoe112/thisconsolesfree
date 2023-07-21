import base64
import json

from protocol.cmd import Command
from protocol.constants import SEP
from protocol.rsp import Response
from protocol.svc import Service

SVCNAME = "Streams"


class Streams(Service):
    def __init__(self):
        super().__init__(self, SVCNAME)

    class ReadCmd(Command):
        def __init__(self, streamID, size=4096, sequence=100):
            self.streamID = streamID
            self.size = size
            self.data = f'"{self.streamID}"{SEP}{self.size}'
            super().__init__(sequence, SVCNAME, "read", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class SubscribeCmd(Command):
        def __init__(self, source_type, sequence=100):
            self.source_type = source_type
            self.data = f'"{self.source_type}"'
            super().__init__(sequence, SVCNAME, "subscribe", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class SubscribeRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.errors = self.tokens[2]

    class ReadRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.encoded_data = self.tokens[2]
            if self.encoded_data == "null":
                self.data = b""
            else:
                self.data = base64.b64decode(self.encoded_data)
            self.errors = self.tokens[3]
            self.lost_size = self.tokens[4]
            self.eos = self.tokens[5]
