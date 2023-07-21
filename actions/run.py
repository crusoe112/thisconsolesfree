import argparse
import json
import sys

from protocol.client import Client
from protocol.services.processes import Processes
from protocol.services.run_control import ResumeModes, RunControl
from protocol.services.streams import Streams


def main(parsed):
    client = Client(parsed.rhost, parsed.rport)

    sequence = 100
    cmd = Streams.SubscribeCmd("Processes", sequence=sequence)
    data = client.send(cmd)

    rsp = Streams.SubscribeRsp(data)
    rsp.unpack()

    sequence += 1
    cmd = Processes.GetEnvironmentCmd(sequence=sequence)
    data = client.send(cmd)

    rsp = Processes.GetEnvironmentRsp(data)
    rsp.unpack()

    sequence += 1
    executable = parsed.cmd.split(" ")[0]
    args = json.dumps(parsed.cmd.split(" "))
    cmd = Processes.StartCmd(
        executable,
        args=args,
        pwd=parsed.pwd,
        env=json.dumps(rsp.env),
        sequence=sequence,
    )
    data = client.send(cmd)

    rsp = Processes.StartRsp(data)
    rsp.unpack()
    stdout = rsp.context["StdOutID"]
    contextID = rsp.context["ID"]

    sequence += 1
    cmd = RunControl.ResumeCmd(
        contextID, mode=ResumeModes.NORMAL.value, sequence=sequence
    )
    data = client.send(cmd)

    rsp = RunControl.ResumeRsp(data)
    rsp.unpack()

    sequence += 1
    cmd = Streams.ReadCmd(stdout, size=1024, sequence=sequence)
    data = client.send(cmd)

    rsp = Streams.ReadRsp(data)
    rsp.unpack()

    output = rsp.data
    while rsp.eos == "false":
        sequence += 1
        cmd = Streams.ReadCmd(stdout, size=1024, sequence=sequence)
        data = client.send(cmd)

        rsp = Streams.ReadRsp(data)
        rsp.unpack()
        output += rsp.data

    sys.stdout.buffer.write(output)

    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility to run shell commands via a tcf-agent with the "
        + "processes, streams, and run control  modules enabled"
    )
    parser.add_argument("rhost", help="IP address of target")
    parser.add_argument("cmd", help="The filepath to download from target")
    parser.add_argument(
        "--pwd",
        default="/",
        help="The remote directory to run the command within",
    )
    parser.add_argument(
        "--rport", default=1534, type=int, help="Port of tcf-agent service"
    )
    parsed = parser.parse_args()
    main(parsed)
