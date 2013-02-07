from agrc.caching.abstraction.base import Command
from agrc.caching.models import CacheJob

class GetCacheJobFromAreaOfChangeCommand(Command):
    """
        Takes the area of change objects and intersects them with the cache extent
        level scale groups. It creates new area of change objects if the levels span
        the groups. This provides a way for other methods to intersect the area of change
        polygon with the predefined cache extent geometries defined.
    """
    
    #: the area of changes
    changes = None
    
    #: the scale levels for which we have different polygons to cache
    groups = [[0,1,2],[3,4],[5,6,7,8,9,10,11,12],[13,14]]
    
    def __init__(self, changes):
        self.changes = changes
        
    def execute(self):
        result = []
        for change in self.changes:
            result.extend(self._create_jobs(change))
        
        return result

    def _create_jobs(self, change):
        result = []
        
        for group in self.groups:
            intersection = self._intersect(change.levels, group)
            
            if len(intersection) == 0:
                continue
            
            job = CacheJob(intersection, change)
            
            result.append(job)
        
        return result

    def _intersect(self, a, b):
        return list(set(a) & set(b))