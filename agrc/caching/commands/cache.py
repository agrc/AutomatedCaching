from agrc.caching.abstraction.base import Command
from agrc.caching.commands import connect
from agrc.caching.config import Server

class CacheStatusCommand(Command):
    _server = ""
    
    def __init__(self, server = Server()):
        self._server = server
        
    def execute(self):
        command = connect.GetTokenCommand(server = self._server)
        token = command.execute()
        
        command = connect.GetServiceStatisticsCommand("CachingTools.GPServer", token, self._server)
        stats = command.execute()
        
        busy = stats['summary']['busy']
        
        if busy > 0:
            return True
        
        return False