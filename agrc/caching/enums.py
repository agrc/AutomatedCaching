#http://stackoverflow.com/a/1695250/352432
def enum(**enums):
    return type('Enum', (), enums)

def enum(**enums):
    return type('Enum', (), enums)

class CacheUpdateModes(object):
    modes = enum(ALL = "RECREATE_ALL_TILES", EMPTY = "RECREATE_EMPTY_TILES")