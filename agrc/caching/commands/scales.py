from agrc.caching.abstraction.base import Command
from agrc.caching import config

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