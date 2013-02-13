from agrc.caching.commands import scales
from agrc.caching.commands import layer

class AreaOfChange(object):
    """
        A representation of a change in a feature class which then represents 
        an area of change in a layer that is used in a cache and needs to be updated
    """
    
    def __init__(self, layer = None, row = None):
        if row is not None:
            self.id = row[0]
            self.creation_date = row[1]
            self.start_date = row[2]
            self.completion_date = row[3]
            self.layer = row[4]
            self.editor = row[6]
            if len(row) == 8:
                self.shape = row[7]

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
    
    #: the date the area was updated. ie: when the new cache tiles were created
    completion_date = None
    
class CacheJobItem(object):
    """
        A representation of a cache service that is going to be updated
    """
    
    def __init__(self, level = None, service_name = None, change = None, object_id = None):
        if change is not None:
            self.creation_date = change.creation_date
            self.start_date = "current date"
            self.layer = change.layer
            self.editor = change.editor
            self.reference_id = change.id
            self.level = level
                  
        self.level = level or self.level
        self.service_name = service_name
        self.reference_id = object_id or self.reference_id
    
    #: refrence id to its area of change polygon
    reference_id = None
    
    #: the name of the map service to cache    
    service_name = None
    
    #: the geometry to update
    shape = None
    
    #: the level to recache
    level = None
    
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
        command = scales.GetUtmScaleFromLevelCommand([self.level])
        return command.execute()

    scales = property(get_scales_from_levels, None)