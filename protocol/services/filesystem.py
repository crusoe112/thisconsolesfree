import base64
from enum import Enum

from protocol.cmd import Command
from protocol.constants import SEP
from protocol.rsp import Response
from protocol.svc import Service

SVCNAME = "FileSystem"


class FileOpenModes(Enum):
    # Open the file for reading.
    TCF_O_READ = 1

    # Open the file for writing.
    # If both this and TCF_O_READ are specified,
    # the file is opened for both reading and
    # writing.
    TCF_O_WRITE = 2

    # Force all writes to append data at the end of
    # the file.
    TCF_O_APPEND = 4

    # If this flag is specified, then a new file
    # will be created if one does not already exist
    # (if TCF_O_TRUNC is specified, the new file
    # will be truncated to zero length if it
    # previously exists).
    TCF_O_CREAT = 8

    # Forces an existing file with the same name to
    # be truncated to zero length when creating a
    # file by specifying TCF_O_CREAT. TCF_O_CREAT
    # MUST also be specified if this flag is used.
    TCF_O_TRUNC = 0x10

    # Causes the request to fail if the named file
    # already exists. TCF_O_CREAT MUST also be
    # specified if this flag is used.
    TCF_O_EXCL = 0x20


class FileSystem(Service):
    def __init__(self):
        super().__init__(self, SVCNAME)

    class OpenCmd(Command):
        def __init__(
            self,
            filename,
            sequence=100,
            open_mode=FileOpenModes.TCF_O_READ.value,
        ):
            self.filename = filename
            self.data = f'"{self.filename}"{SEP}{open_mode}{SEP}null'
            super().__init__(sequence, SVCNAME, "open", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class ReadCmd(Command):
        def __init__(self, filehandle, offset=0, size=5120, sequence=100):
            self.filehandle = filehandle
            self.offset = offset
            self.size = size
            self.data = f'"{self.filehandle}"{SEP}{self.offset}{SEP}{self.size}'
            super().__init__(sequence, SVCNAME, "read", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class WriteCmd(Command):
        def __init__(self, filehandle, filecontent, offset=0, sequence=100):
            self.filehandle = filehandle
            self.filecontent = filecontent
            self.encodedcontent = base64.b64encode(filecontent).decode()
            self.offset = offset
            self.data = (
                f'"{filehandle}"{SEP}{offset}{SEP}"{self.encodedcontent}"'
            )
            super().__init__(sequence, SVCNAME, "write", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class CloseCmd(Command):
        def __init__(self, filehandle, sequence=100):
            self.filehandle = filehandle
            self.data = f'"{filehandle}"'
            super().__init__(sequence, SVCNAME, "close", self.data)

        def prepare(self):
            return f"{super().prepare(self.data)}"

    class OpenRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.errors = self.tokens[2]
            self.filehandle = self.tokens[3].replace('"', "")

    class ReadRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.encodedfile = self.tokens[2].replace('"', "")
            self.errors = self.tokens[3]
            self.eof = self.tokens[4]
            self.filecontents = base64.b64decode(self.encodedfile)

    class WriteRsp(Response):
        def __init__(self, data):
            super().__init__(data)

        def unpack(self):
            super().unpack(self.data)
            self.errors = self.tokens[2]
