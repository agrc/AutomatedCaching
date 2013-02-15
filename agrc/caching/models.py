from agrc.caching.commands import scales
from datetime import datetime

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
            self.editor = row[5]
            if len(row) == 7:
                self.shape = row[6]

        self.layer = layer or self.layer
        
    #: the object id in sde
    id = None
        
    #: the date the change was made
    creation_date = None
    
    #: day it was picked up to a cache job
    start_date = None
    
    #: the date the area was updated. ie: when the new cache tiles were created
    completion_date = None
    
    #: the layer the change happened on
    layer = None #enum
        
    #: the creator of the changes
    editor = None    
    
    #: the geometry of the area where there are positive and negative changes
    shape = None
    
class CacheJob(object):
    """
        A representation of a cache service that is going to be updated
    """
    
    def __init__(self, level = None, service_name = None, job_item = None, object_id = None):
        if job_item is not None:
            self.creation_date = datetime.now()
            self.reference_id = job_item.id
            self.scale = self.get_scales_from_levels(level)
                  
        self.level = level or self.level
        self.service_name = service_name
        self.reference_id = object_id or self.reference_id
    
    #: refrence id to its area of change polygon
    reference_id = None
    
    #: the name of the map service to cache    
    service_name = None
    
    #: the geometry to update
    shape = None
    
    #: the scale to recache
    scale = None
    
    #: the date the job was created
    creation_date = None
    
    #: the date the job started
    start_date = None
    
    #: the date the job finished
    completion_date = None
    
    #: whether to recreate all tiles or just empty ones
    update_mode = None
    
    def get_scales_from_levels(self, level):
        command = scales.GetUtmScaleFromLevelCommand([level])
        return command.execute()

class CacheJobItem(object):
    """
        The intermediate step before an area of change becomes a caching item.
        this allows us to dissolve, clip, whatever
    """   
    
    def __init__(self, level = None, service_name = None, change = None, row = None):
        if row is not None:
            self.level = row[0]
            self.service_name = row[1]
            self.reference_id = row[2] 
            self.shape = row[3]    
            
        self.service_name = self.service_name or service_name
        self.reference_id = self.reference_id or change.id
        self.shape = self.shape or change.shape
        self.level = self.level or level
         
    #: the cache level to recache
    level = None
    
    #: the name of the map service to cache    
    service_name = None
    
    #: the id of the area of change that created this item
    reference_id = None
    
    #: the geometry of the area of change
    shape = None
    
    
