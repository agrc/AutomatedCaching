from agrc.caching.commands import scales
from agrc.caching.commands import layer

class AreaOfChange(object):
    """
        A representation of a change in a feature class which then represents 
        an area of change in a layer that is used in a cache and needs to be updated
    """
    
    def __init__(self, levels = None, layer = None, row = None):
        if row is not None:
            self.id = row[0]
            self.creation_date = row[1]
            self.start_date = row[2]
            self.completion_date = row[3]
            self.layer = row[4]
            self.levels = [int(x.strip()) for x in row[5].split(",")]
            self.editor = row[6]
            if len(row) == 8:
                self.shape = row[7]
        
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
    
    def __init__(self, levels = None, service_name = None, change = None, object_id = None):
        if change is not None:
            self.creation_date = change.creation_date
            self.start_date = "current date"
            self.layer = change.layer
            self.editor = change.editor
            self.reference_id = change.id
           
        self.levels = levels
        self.service_name = service_name or self.get_maps_from_layer(self)
        self.reference_id = object_id or self.reference_id
    
    #: refrence id to its area of change polygon
    reference_id = None
    
    #: the name of the map service to cache    
    service_name = None
    
    #: the geometry to update
    shape = None
    
    #: the levels to recache
    levels = None
    
    #: the layer of change
    layer = None
    
    #: the date the job was created
    creation_date = None
    
    #: the date the job started
    start_date = None
    
    #: the date the job finished
    completion_date = None
    
    #: the person who created the change
    editor = None
    
    #: whether to recreate all tiles or just empty ones
    update_mode = None
    
    def get_scales_from_levels(self):
        command = scales.GetUtmScaleFromLevelCommand(self.levels)
        return command.execute()
    
    def get_maps_from_layer(self, job):
        command = layer.GetMapNamesContainingLayerCommand(job = job)
        return command.execute()
    
    scales = property(get_scales_from_levels, None)