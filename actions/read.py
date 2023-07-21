import argparse

from protocol.client import Client
from protocol.services.filesystem import FileOpenModes, FileSystem


def main(parsed):
    client = Client(parsed.rhost, parsed.rport)

    sequence = 100
    cmd = FileSystem.OpenCmd(parsed.rfile, sequence)
    data = client.send(cmd)

    rsp = FileSystem.OpenRsp(data)
    rsp.unpack()

    sequence += 1
    filehandle = rsp.filehandle
    cmd = FileSystem.ReadCmd(filehandle, sequence=sequence, size=1024)
    data = client.send(cmd)

    rsp = FileSystem.ReadRsp(data)
    rsp.unpack()
    filecontents = rsp.filecontents
    location = 1024
    while rsp.eof == "false":
        sequence += 1
        cmd = FileSystem.ReadCmd(
            filehandle, sequence=sequence, offset=location, size=1024
        )
        data = client.send(cmd)

        rsp = FileSystem.ReadRsp(data)
        rsp.unpack()
        filecontents += rsp.filecontents
        location += 1024

    sequence += 1
    cmd = FileSystem.CloseCmd(filehandle, sequence=sequence)
    data = client.send(cmd)

    client.close()

    with open(parsed.lfile, "wb") as output:
        output.write(filecontents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility to download files from a tcf-agent with the"
        + "filesystem module enabled"
    )
    parser.add_argument("rhost", help="IP address of target")
    parser.add_argument("rfile", help="The filepath to download from target")
    parser.add_argument("lfile", help="The local file path to write to")
    parser.add_argument(
        "--rport", default=1534, type=int, help="Port of tcf-agent service"
    )
    parsed = parser.parse_args()
    main(parsed)
