from agrc.caching.abstraction.base import Command
from agrc.caching.commands import connect
from agrc.caching.commands import scales
from agrc.caching import config
from agrc.caching import enums
import arcpy
# http://resources.arcgis.com/en/help/main/10.1/index.html#//005400000004000000
from arcpy import CreateMapServerCache_server as create_schema
# http://resources.arcgis.com/en/help/main/10.1/index.html#/Manage_Map_Server_Cache_Tiles/00540000000p000000/
from arcpy import ManageMapServerCacheTiles_server as create_tiles
import time

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
    tile_origin = "-5120900 9998100"
    
    #: image type to save tiles as
    tile_format = "JPEG"
    
    #: defines tiling scheme type
    tiling_scheme = "NEW"
    
    #: the tiling scheme type
    scheme_type = "CUSTOM"
    
    #: number of scales
    number_of_scales = None
    
    #: image resolution
    dpi = "96"
    
    #: pixel size of tiles
    tile_size = "256 x 256"
    
    #: individual files or many files in cluster
    storage_format = "COMPACT" #"EXPLODED"
    
    #: smush it
    compression = None
    
    #: the string of scales
    scales = None
    
    #: the full path to the service through the connection file
    service_path = None
    
    def __init__(self, cache_job, tile_origin = None, tile_format = None,
                 dpi = None, tile_size = None, number_of_scales = None,
                 compression = None):
        
        self.basemap = cache_job.service_name
        self.tile_origin = tile_origin or self.tile_origin
        self.tile_format = tile_format or self.tile_format
        self.dpi = dpi or self.dpi
        self.tile_size = tile_size or self.tile_size
        scales = config.Scales()
        self.number_of_scales = len(cache_job.levels) or number_of_scales or scales.scale_count
        basemap = config.BaseMap()
        self.compression = compression or basemap.get_compression_level(self.basemap)
        
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
        print "{0} completed with messages {1}".format(result.toolname, str(resultValue))
        
class CreateTilesCommand(object):  
    #: path to feature class with geometreis of polygon to recache 
    area_of_interest = None
    
    #: the name of the map service to cache
    #: will concatentation with service_path
    basemap = None
    
    #: location to admin connection file for caching server
    connection_file_path = None
    
    #: the number of processes to throw at a cache
    number_of_processes = 4
    
    #: the string of scales
    scales = None
    
    #: concatenation of connection file and baseap
    #  "\\connection\file\{0}".format(self.serviceName)
    service_path = None
    
    #: whether to recreate all tiles or only empty ones
    update_mode = enums.CacheUpdateModes.modes.ALL
    
    #: the extent to update, trumped by area_of_interest
    update_extent = "#"
    
    def __init__(self, cache_job, 
                 connection_file_path = None, 
                 service_path = None, 
                 scales = None, 
                 update_mode = None, 
                 number_of_processes = None, 
                 area_of_interest = None):
        
        self.basemap = cache_job.service_name
        self.scales = cache_job.scales or scales or self.scales
        self.update_mode = cache_job.update_mode or update_mode or self.update_mode
        self.service_path = service_path or self.service_path
        self.connection_file_path = connection_file_path or self.connection_file_path
        self.area_of_interest = area_of_interest or self.area_of_interest
        self.number_of_processes = number_of_processes or self.number_of_processes
    
    def execute(self):
        result = create_tiles(
                              self.service_path,
                              self.scales,
                              self.update_mode,
                              self.number_of_processes,
                              self.area_of_interest,
                              self.update_extent,
                              "WAIT")
        
        while result.status < Arcpy.Succeeded:
            print "sleeping"
            time.sleep(1)
            
        resultValue = result.getMessages()
        print "{0} completed with messages {1}".format(result.toolname, str(resultValue))
        
