from agrc.caching.abstraction.base import Command
from agrc.caching import config
from arcpy import env

class AreasOfChangeQuery(Command):
    def execute(self):
        # query sde get new changes
        return _querySdeForAreasOfChange()
    
    def _querySdeForAreasOfChange(self):
        
        env.workspace = config.Geodatabase().path
        pass
