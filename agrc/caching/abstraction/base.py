class Command(object):
    def execute(self):
        raise NotImplementedError( "Should have implemented this" )
    
class CachingProcess(object):
    socProcesses = "#"
    servicePath = None #
    serviceName = None #
    scales = [] #
    scaleService = None
    areaOfInterest = None# trumps updateExtent
#    updateMode = "RECREATE_ALL_TILES"
    updateMode = "RECREATE_EMPTY_TILES"
    gdbPath = "C:\\Cache\\MapData\\UtahBaseMap-Data.gdb\\"
    gp = None