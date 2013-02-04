#http://stackoverflow.com/a/1695250/352432
def enum(**enums):
    return type('Enum', (), enums)

def enum(**enums):
    return type('Enum', (), enums)

class CacheUpdateModes(object):
    modes = enum(ALL = "RECREATE_ALL_TILES", 
                 EMPTY = "RECREATE_EMPTY_TILES")
    
class BaseMaps(object):
    name = enum(TERRAIN = "terrain", 
                VECTOR = "vector",
                LITE = "lite",
                IMAGERY = "imagery",
                TOPO = "topo",
                HILLSHADE = "hillshade",
                HYBRID = "hybrid")

class Arcpy(object):
    status = enum(New = 0,
                  Submitted = 1,
                    Waiting = 2,
                    Executing = 3,
                    Succeeded = 4,
                    Failed = 5,
                    Timed_out = 6,
                    Cancelling = 7,
                    Cancelled = 8,
                    Deleting = 9,
                    Deleted = 10)