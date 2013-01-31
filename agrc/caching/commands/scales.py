from agrc.caching.abstraction.base import Command
from agrc.caching.models import CacheJob

class GetCacheJobFromAreaOfChangeCommand(Command):
    _changes = None
    _groups = [[0,1,2],[3,4],[5,6,7,8,9,10,11,12],[13,14]]
    
    def __init__(self, changes):
        self._changes = changes
        
    def execute(self):
        result = []
        for change in self._changes:
            result.extend(self._create_jobs(change))
        
        return result

    def _create_jobs(self, change):
        print "_create_jobs"
        
        result = []
        
        for group in self._groups:
            intersection = self._intersect(change.levels, group)
            
            if len(intersection) == 0:
                continue
            
            job = CacheJob(intersection, change.layer)
            
            result.append(job)
        
        return result

    def _intersect(self, a, b):
        return list(set(a) & set(b))