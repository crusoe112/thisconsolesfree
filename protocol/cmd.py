from protocol.constants import EOM, SEP


class Command:
    def __init__(self, sequence, service, command, data):
        self.sequence = sequence
        self.service = service
        self.command = command
        self.data = data

    def prepare(self, formatted_data):
        if len(formatted_data) == 0:
            return f"C{SEP}{self.sequence}{SEP}{self.service}{SEP}{self.command}{EOM}"

        return f"C{SEP}{self.sequence}{SEP}{self.service}{SEP}{self.command}{SEP}{formatted_data}{EOM}"
