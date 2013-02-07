from agrc.caching.commands import scales

class AreaOfChange(object):
    """
        A representation of a row in a feature class which then represents 
        an area of change in a layer that is used in a cache and needs to be updated
    """
    
    def __init__(self, levels = None, layer = None, row = None):
        if row is not None:
            self.id = row[0]
            self.creation_date = row[2]
            self.start_date = row[3]
            self.completion_date = row[4]
            self.layer = row[5]
            self.levels = [x.strip() for x in row[6].split(",")]
            self.editor = row[7]
        
        self.levels = levels or self.levels
        self.layer = layer or self.layer
        
    #: the object id in sde
    id = None
        
    #: the date the change was made
    creation_date = None
    
    #: day it was picked up to a cache job
    start_date = None
    
    #: the geometry of the area where there are positive and negative changes
    shape = None
    
    #: the creator of the changes
    editor = None
    
    #: the layer the change happened on
    layer = None #enum
    
    #: the levels the layer is present in
    levels = None
    
    #: the date the area was updated. ie: when the new cache tiles were created
    completion_date = None
    
class CacheJob(object):
    """
        A representation of a cache service that is going to be updated
    """
    
    def __init__(self, levels=[], service_name = ""):
        self.levels = levels
        self.service_name = service_name
    
    #: the name of the map service to cache    
    service_name = None
    
    #: the geometry to update
    geometry = None
    
    #: the levels to recache
    levels = None
    
    #: the date the job started
    start_date = None
    
    #: the date the job finished
    completion_date = None
    
    #: whether to recreate all tiles or just empty ones
    update_mode = None
    
    def get_scales_from_levels(self):
        command = scales.GetUtmScaleFromLevelCommand(self.levels)
        return command.execute()
    
    scales = property(get_scales_from_levels, None)