import argparse


def main(parser, args):
    cmd = args.cmd

    # retrieve subparsers from parser
    subparsers_actions = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]

    for subparsers_action in subparsers_actions:
        # get all subparsers and print help
        for choice, subparser in subparsers_action.choices.items():
            if choice == cmd:
                print("Command '{}'".format(choice))
                print(subparser.format_help())
                return

    print("Invalid command")
    print(parser.format_help())
