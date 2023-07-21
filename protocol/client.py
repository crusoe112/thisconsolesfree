import socket
import time

from protocol.constants import EOM, SEP


class Client:
    def __init__(self, host, port):
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))
        self.client_socket.send(
            f'E{SEP}Locator{SEP}Hello{SEP}["Locator"]{EOM}'.encode("utf-8")
        )
        services = self.client_socket.recv(5120).decode("utf-8")

    def recv(self, buf_size, timeout):
        self.client_socket.settimeout(timeout)
        data = self.client_socket.recv(buf_size)
        return data.decode()

    def send(self, cmd, timeout=1, retries=3):
        for attempt in range(retries):
            now = time.time()
            self.client_socket.send(cmd.prepare().encode())
            data = ""
            our_packet = False
            while not our_packet:
                try:
                    packet = self.recv(5120, timeout)
                except socket.timeout:
                    continue
                messages = packet.split(EOM)
                for message in messages:
                    try:
                        sequence = message.split(SEP)[1]
                    except:
                        continue
                    if sequence == str(cmd.sequence):
                        data += message
                        our_packet = True

            return data

    def close(self):
        self.client_socket.close()
