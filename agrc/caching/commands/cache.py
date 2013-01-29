from agrc.caching.abstraction.base import Command
from agrc.caching.commands import connect

class CacheStatusCommand(Command):
    def execute(self):
        command = connect.GetTokenCommand()
        token = command.execute()