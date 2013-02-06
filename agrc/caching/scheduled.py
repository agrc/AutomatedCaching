from agrc.caching.commands import cache
from agrc.caching.commands import dto
from agrc.caching.queries import sde
from agrc.caching import config

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
        
        server = config.Server(use_port = True)
        
        caching = self._get_caching_status(server)
        
        if caching:
            print "The server is busy. Exiting"
            return
        
        changes = self._get_changes()
        total_changes = len(changes)
        
        if total_changes == 0:
            print "There is nothing to cache. Exiting."
            return
        
        print "There are {0} areas of change. Processing...".format(total_changes)
        
        jobs = self._process_areas_of_change(changes)
        
        for job in jobs:
            print "Processing job {0}.".format(job.service_name)
            self._process_job(job)
        
    def _process_job(self, job):
        # update data
        
        # create cache schema
        command = cache.CreateCacheSchemaCommand(job.service_name)
        command.execute()
        
        # cache tiles
        command = cache.CreateTilesCommand(job.service_name)
        command.execute()
        
    def _process_areas_of_change(self, changes):
        print "_process_areas_of_change"
        
        command = dto.GetCacheJobFromAreaOfChangeCommand(changes)
        return command.execute()

    def _get_caching_status(self, server = config.Server()):
        print "_get_caching_status"
        
        command = cache.CacheStatusCommand(server)
        return command.execute()
    
    def _get_changes(self):
        print "_get_changes"
        
        query = sde.AreasOfChangeQuery()
        return query.execute()
        
#http://docs.python.org/2/tutoriCal/modules.html#executing-modules-as-scripts     
if __name__ == "__main__":
    this = Runner()
    this.start()
