from agrc.caching.abstraction.base import Command
from agrc.caching.commands import connect
from agrc.caching.config import Server

class CacheStatusCommand(Command):
    """
        Returns true if the number of busy instances on the server
        are greater than 0. This tells us the server is caching a job already.
    """
    
    #: the arcgis server configuration
    server = None
    
    def __init__(self, server = Server()):
        self.server = server
        
    def execute(self):
        command = connect.GetTokenCommand(server = self.server)
        token = command.execute()
        
        command = connect.GetServiceStatisticsCommand("CachingTools.GPServer", token, self.server)
        stats = command.execute()
        
        busy = stats['summary']['busy']
        
        if busy > 0:
            return True
        
        return False
    
class ProcessChangeGeometryCommand(Command):
    """
        Command to possibly normalize and dissolve geometries to be cached
        This class may be unused not sure yet.
    """
    
    #: area of change 
    changes = None
    
    #: arcgis python module
    arcpy = None
    
    def __init__(self, changes, arcpy):
        self.changes = changes
        self.arcpy = arcpy
    
    def execute(self):
        pass
        
    def _merge_geometries(self, changes):
        pass
    
    def _intersect_geometry_to_scale_extent(self, changes):
        pass
    
    def _dissolve_geometries(self, changes):
        pass

class ProccessJobCommand(Command):
    """
        A command for kicking off a cache
    """
    
    #: The current job to cache
    job = None
    
    #: arcgis python module
    arcpy = None
    
    def __init__(self, job, arcpy):
        self.job = job
        self.arcpy = arcpy
        
    def execute(self):
        pass
    
    