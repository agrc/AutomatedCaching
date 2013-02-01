from agrc.caching.commands import cache
from agrc.caching.commands import scales
from agrc.caching.queries import sde

class Runner(object):
    def start(self):
        print 'start'
        
        caching = self._get_caching_status()
        
        if caching:
            return
        
        changes = self._get_changes()
        
        if len(changes) == 0:
            return
        
        jobs = self._process_areas_of_change(changes)
        
        for job in jobs:
            self._process_job(job)
        
    def _process_job(self, job):
        
        pass
        
    def _process_areas_of_change(self, changes):
        print "_process_areas_of_change"
        
        command = scales.GetCacheJobFromAreaOfChangeCommand(changes)
        return command.execute()

    def _get_caching_status(self):
        print "_get_caching_status"
        
        command = cache.CacheStatusCommand()
        return command.execute()
    
    def _get_changes(self):
        print "_get_changes"
        
        query = sde.AreasOfChangeQuery()
        return query.execute()
        
#http://docs.python.org/2/tutoriCal/modules.html#executing-modules-as-scripts     
if __name__ == "__main__":
    this = Runner()
    this.start()
