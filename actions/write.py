import argparse

from protocol.client import Client
from protocol.services.filesystem import FileOpenModes, FileSystem


def main(parsed):
    client = Client(parsed.rhost, parsed.rport)

    sequence = 100
    open_mode = (
        FileOpenModes.TCF_O_WRITE.value | FileOpenModes.TCF_O_CREAT.value & 0xFF
    )
    cmd = FileSystem.OpenCmd(parsed.rfile, sequence, open_mode=open_mode)
    data = client.send(cmd)

    rsp = FileSystem.OpenRsp(data)
    rsp.unpack()

    sequence += 1
    filehandle = rsp.filehandle

    with open(parsed.lfile, "rb") as lfile:
        data = lfile.read()

    sequence += 1
    cmd = FileSystem.WriteCmd(filehandle, data, sequence=sequence, offset=0)
    data = client.send(cmd)

    rsp = FileSystem.WriteRsp(data)
    rsp.unpack()
    errors = rsp.errors
    if len(errors) > 0:
        print(errors)

    sequence += 1
    cmd = FileSystem.CloseCmd(filehandle)
    data = client.send(cmd)

    client.close()

    print(f"Data written to {parsed.rfile} on {parsed.rhost}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility to upload files from a tcf-agent with the"
        + "filesystem module enabled"
    )
    parser.add_argument("rhost", help="IP address of target")
    parser.add_argument("lfile", help="The local file path to read from")
    parser.add_argument("rfile", help="The filepath to upload to the target")
    parser.add_argument(
        "--rport", default=1534, type=int, help="Port of tcf-agent service"
    )
    parsed = parser.parse_args()

    main(parsed)
