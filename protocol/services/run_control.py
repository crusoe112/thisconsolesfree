from enum import Enum

from protocol.cmd import Command
from protocol.constants import SEP
from protocol.rsp import Response
from protocol.svc import Service

SVCNAME = "RunControl"


class ResumeModes(Enum):
    NORMAL = 0
    STEP_OVER = 1
    STEP = 2
    STEP_LINE = 3
    STEP_LINE_FUN = 4
    STEP_OUT = 5
    RESUME_BACK = 6
    STEP_BACK = 7
    STEP_BACK_CONTEXT = 8
    STEP_BACK_LINE = 9
    STEP_BACK_LINE_FUN = 10
    STEP_BACK_OUT = 11
    STEP_RANGE_FUN = 12
    STEP_RANGE = 13
    STEP_BACK_RANGE_FUN = 14
    STEP_BACK_RANGE = 15
    STEP_ACTIVE = 16
    STEP_BACK_ACTIVE = 17


class RunControl(Service):
    def __init__(self):
        super().__init__(self, SVCNAME)

    class ResumeCmd(Command):
        def __init__(self, contextID, mode, count=1, sequence=100):
            self.contextID = contextID
            self.mode = mode
            self.count = count
            self.data = f'"{self.contextID}"{SEP}{self.mode}{SEP}{self.count}'
            super().__init__(sequence, SVCNAME, "resume", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class ResumeRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.errors = self.tokens[2]
