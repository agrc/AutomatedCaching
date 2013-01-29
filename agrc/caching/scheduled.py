from agrc.caching.commands import cache
from agrc.caching.queries import sde

class Runner(object):
    def start(self):
        print 'start'
        
        isCurrentlyCaching = self._getCachingStatus()
        
        if isCurrentlyCaching:
            return
        
        changes = self._getChanges()

    def _getCachingStatus(self):
        print "_getCachingStatus"
        
        command = cache.CacheStatusCommand()
        return command.execute()
    
    def _getChanges(self):
        print "_getChanges"
        
        query = sde.AreasOfChangeQuery()
        return query.execute()
        
        pass
        
#http://docs.python.org/2/tutoriCal/modules.html#executing-modules-as-scripts     
if __name__ == "__main__":
    this = Runner()
    this.start()
