from protocol.constants import SEP


class Response:
    def __init__(self, data):
        self.data = data

    def unpack(self, data):
        self.tokens = data.split(SEP)
        self.type = self.tokens[0]
        self.token = self.tokens[1]
