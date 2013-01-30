class Command(object):
    def execute(self):
        raise NotImplementedError( "Should have implemented this" )
    
class CachingProcess(object):
    socProcesses = "#"
    servicePath = "" #
    serviceName = "" #
    scales = [] #
    scaleService = ""
    areaOfInterest = "" # trumps updateExtent
#    updateMode = "RECREATE_ALL_TILES"
    updateMode = "RECREATE_EMPTY_TILES"
    gdbPath = "C:\\Cache\\MapData\\UtahBaseMap-Data.gdb\\"
    gp = ""