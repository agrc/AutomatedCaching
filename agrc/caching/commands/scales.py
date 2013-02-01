from agrc.caching.abstraction.base import Command
from agrc.caching.models import CacheJob
from agrc.caching import config

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
            
            job = CacheJob(intersection, change.layer)
            
            result.append(job)
        
        return result

    def _intersect(self, a, b):
        return list(set(a) & set(b))

class GetUtmScaleFromLevelCommand(Command):
    """
        Returns utm scale from scale level number in the format
        that the geoprocessing tool likes.
        
        `[14] => '1128.497176'`
        `[13, 14] => '2256.994353;1128.497176'`
        
        :keyword levels: see :attr:`levels`
    """
    
    #: the cache level as an array
    levels = None
    
    def __init__(self, levels = None):
        self.levels = levels
        
    def execute(self):
        scale_map = config.Scales().scale_map
        scales = [key for level, key in scale_map.iteritems() if level in self.levels]
        
        return ';'.join(scales)