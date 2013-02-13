from agrc.caching.abstraction.base import Command
from agrc.caching.models import CacheJobItem
from agrc.caching.commands import layer

class GetCacheJobItemsFromAreaOfChangeCommand(Command):
    """
        Explodes the area of changes by the visible scales
    """
    
    #: the area of changes
    changes = None
    
    def __init__(self, changes):
        self.changes = changes
        
    def execute(self):
        result = []
        for change in self.changes:
            result.extend(self._create_jobs(change))
        
        return result

    def _create_jobs(self, change):
        result = []
        
        command = layer.GetMapNamesContainingLayerCommand(change = change)
        service_scale_map = command.execute()
        
        for service_name in service_scale_map.keys():
            for level in service_scale_map[service_name]:
                job = CacheJobItem(level = level, service_name = service_name, change = change)
                result.append(job)
        
        return result