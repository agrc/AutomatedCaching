from agrc.caching.commands import cache
from agrc.caching.commands import scales
from agrc.caching.queries import sde

class Runner(object):
    """
        A class that is called to orchestrate caching.
        A scheduled task will call this nightly to check 
        for area of change features in SDE and create cache jobs
        to instruct the system to update the affected caches.
    """
    
    def start(self):
        """
            main entry method to start the cache updating process
        """
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
        # update data
        
        # create cache schema
        command = cache.CreateCacheSchemaCommand(job.service_name)
        command.execute()
        
        # cache tiles
        
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
