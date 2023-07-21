import json

from protocol.cmd import Command
from protocol.constants import SEP
from protocol.rsp import Response
from protocol.svc import Service

SVCNAME = "Processes"


class Processes(Service):
    def __init__(self):
        super().__init__(self, SVCNAME)

    class GetEnvironmentCmd(Command):
        def __init__(self, sequence=100):
            super().__init__(sequence, SVCNAME, "getEnvironment", "")

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class StartCmd(Command):
        def __init__(
            self,
            executable,
            pwd="",
            args=[],
            env="[]",
            attach="true",
            sequence=100,
        ):
            self.executable = executable
            self.pwd = pwd
            self.args = args
            self.env = env
            self.attach = attach
            self.data = f'"{self.pwd}"{SEP}"{self.executable}"{SEP}{self.args}{SEP}{self.env}{SEP}{self.attach}'
            super().__init__(sequence, SVCNAME, "start", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class StartRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.errors = self.tokens[2]
            self.context = json.loads(self.tokens[3])

    class GetEnvironmentRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.errors = self.tokens[2]
            self.env = json.loads(self.tokens[3])
