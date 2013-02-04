from agrc.caching.abstraction.base import Command
from agrc.caching.commands import connect
from agrc.caching.commands import scales
from agrc.caching import config
from arcpy.caching.enums import Arcpy
#http://resources.arcgis.com/en/help/main/10.1/index.html#//005400000004000000
from arcpy import CreateMapServerCache_server as create_schema

class CacheStatusCommand(Command):
    """
        Returns true if the number of busy instances on the server
        are greater than 0. This tells us the server is caching a job already.
        
        :keyword server: see :attr:`server`
    """
    
    #: the arcgis server configuration
    server = None
    
    def __init__(self, server = config.Server()):
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
        
        :keyword changes: see :attr:`changes`.
        :keyword arcpy: see :attr:`arcpy`.
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
        
        :keyword job: see :attr:`job`.
        :keyword arcpy: see :attr:`arcpy`.
    """
    
    #: The current job to cache
    job = None
    
    #: arcgis python module
    arcpy = None
    
    def __init__(self, job, arcpy = None):
        self.job = job
        self.arcpy = arcpy
        
    def execute(self):
        levels = self._get_scales_from_levels(self.job.levels)
    
    def _get_scales_from_levels(self, levels):
        command = scales.GetUtmScaleFromLevelCommand(levels)
        return command.execute()
    
class CreateCacheSchemaCommand(Command):
    
    #: the agrc.caching.enums.BaseMaps.names
    basemap = None
    
    #: location to store tiles
    caching_path = None
    
    #: location to admin connection file for caching server
    connection_file_path = None
    
    #: the tile orgin centroid
    tile_origin = None
    
    #: image type to save tiles as
    tile_format = None
    
    #: defines tiling scheme type
    tiling_scheme = "NEW"
    
    #: the tiling scheme type
    scheme_type = "CUSTOM"
    
    #: number of scales
    number_of_scales = None
    
    #: image resolution
    dpi = None
    
    #: pixel size of tiles
    tile_size = None
    
    #: individual files or many files in cluster
    storage_format = "COMPACT" #"EXPLODED"
    
    #: smush it
    compression = None
    
    #: the string of scales
    scales = None
    
    #: the full path to the service through the connection file
    service_path = None
    
    def __init__(self, basemap_name, tile_orgin = "-5120900 9998100", tile_format = "JPEG",
                 dpi =  "96", tile_size = "256 x 256", number_of_scales = config.Scales().scale_count,
                 compression = "96"):
        self.basemap = basemap_name
        self.tile_origin = tile_orgin
        self.tile_format = tile_format
        self.dpi = dpi
        self.tile_size = tile_size
        self.number_of_scales = number_of_scales
        self.compression = compression
        
    def execute(self):
        result = create_schema(
                               self.basemap,
                               self.caching_path,
                               self.tiling_scheme,
                               self.scheme_type,
                               self.number_of_scales,
                               self.dpi,
                               self.tile_size,
                               "#",
                               self.tile_origin,
                               self.scales,
                               self.tile_format,
                               self.compression,
                               self.storage_format)
        
        while result.status < Arcpy.Succeeded:
            print "sleeping"
            time.sleep(1)
            
        resultValue = result.getMessages()
        report.write ("{0} completed with messages {1}".format(result.toolname, 
                                                               str(resultValue))