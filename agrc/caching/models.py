class AreaOfChange(object):
    """
        A representation of a row in a feature class which then represents 
        an area of change in a layer that is used in a cache and needs to be updated
    """
    
    def __init__(self,levels=[], layer = ""):
        self.levels = levels
        self.layer = layer
        
    date = None
    shape = None
    editor = None
    layer = None #enum
    levels = None
    completion_date = None
    
class CacheJob(object):
    """
        A representation of a cache service that is going to be updated
    """
    
    def __init__(self,levels=[], serviceName = ""):
        self.levels = levels
        self.serviceName = serviceName
        
    serviceName = None
    geometry = None
    levels = None
    start_date = None
    completion_date = None
    
     
