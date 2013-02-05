from agrc.caching.abstraction.base import Command
from agrc.caching import config
from arcpy import env
from arcpy import da


class AreasOfChangeQuery(Command):
    def execute(self):
        # query sde get new changes
        return self._querySdeForAreasOfChange()
    
    def _querySdeForAreasOfChange(self):      
        settings = config.Geodatabase()
        env.workspace = "{0}\{1}".format(settings.base_path, settings.path)
        
        changes = []
        with da.SearchCursor(settings.changeFeatureClass, "*") as cursor:
            for row in cursor:
                changes.append(row)
                
        return changes
        
