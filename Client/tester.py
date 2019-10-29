#!/usr/bin/python3

from values import *
from hexapod_connection import*

class Hexapod:
    def __init__(self, mode):
        self.connection = HexapodConnection(mode=mode)
        self.start_prompt()

    def start_prompt(self):
        while True:
            try:
                command = input("$ ")
            except:
                self.connection.close()
                exit(0)
            self.send_command(command)

    def send_command(self, command):
        self.connection.send_command(command, 0)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "--wire":
        Hexapod("wire")
    else:
        Hexapod("wifi")