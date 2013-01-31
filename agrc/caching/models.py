class AreaOfChange(object):
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
    def __init__(self,levels=[], serviceName = ""):
        self.levels = levels
        self.serviceName = serviceName
        
    serviceName = None
    geometry = None
    levels = None
    start_date = None
    completion_date = None
    
     
