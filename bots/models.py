# TODO Create logic of commands

class Command:

    def __init__(self):
        self.command_type = "StdCommand"
        self.understanded = False

    def check(self):
        if not self.understanded:
            raise Exception("Command not understanded")

    def execute(self):
        pass


class CSendMessage(Command):

    def execute(self):
        pass