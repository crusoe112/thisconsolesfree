import argparse

import actions.help
import actions.read as read
import actions.run as run
import actions.write as write


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(
        description="Utility to interact with TCF debugging agents"
    )

    # create sub-parser
    sub_parsers = parser.add_subparsers(help="Action to run", dest="subcommand")

    # create the parser for the "read" sub-command
    parser_read = sub_parsers.add_parser(
        "read", help="Download a file from the target"
    )
    parser_read.add_argument("lfile", help="The output file to write to")
    parser_read.add_argument("rfile", help="The remote file to download")
    parser_read.add_argument("rhost", help="The remote host to connect to")
    parser_read.add_argument(
        "--rport", default=1534, type=int, help="The remote port to connect to"
    )

    # create the parser for the "write" sub-command
    parser_write = sub_parsers.add_parser(
        "write", help="Upload a file to the target"
    )
    parser_write.add_argument("lfile", help="The local file to upload")
    parser_write.add_argument("rfile", help="The remote file path to write to")
    parser_write.add_argument("rhost", help="The remote host to connect to")
    parser_write.add_argument(
        "--rport", default=1534, type=int, help="The remote port to connect to"
    )

    # create the parser for the "run" sub-command
    parser_run = sub_parsers.add_parser(
        "run", help="Execute a command on the target"
    )
    parser_run.add_argument("cmd", help="The command to run")
    parser_run.add_argument("rhost", help="The remote host to connect to")
    parser_run.add_argument(
        "--pwd",
        default="/",
        help="The working directory to run the command within",
    )
    parser_run.add_argument(
        "--rport", default=1534, type=int, help="The remote port to connect to"
    )

    # create the parser for the "help" sub-command
    parser_help = sub_parsers.add_parser(
        "help", help="Display help menu for a command"
    )
    parser_help.add_argument("cmd", help="The command to display help for")

    options = parser.parse_args()

    if options.subcommand == "help":
        actions.help.main(parser, options)
    elif options.subcommand == "read":
        read.main(options)
    elif options.subcommand == "write":
        write.main(options)
    elif options.subcommand == "run":
        run.main(options)


if __name__ == "__main__":
    main()
