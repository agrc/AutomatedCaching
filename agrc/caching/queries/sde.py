from agrc.caching.abstraction.base import Command
from agrc.caching import config
from arcpy import env
from arcpy import da
from time import time


class AreasOfChangeQuery(Command):
    def execute(self):
        # query sde get new changes
        return self._query_sde_for_new_changes()
    
    def _query_sde_for_new_changes(self):      
        settings = config.Geodatabase()
        env.workspace = "{0}\{1}".format(settings.base_path, settings.path)
        
        changes = []
        with da.SearchCursor(settings.changeFeatureClass, "*",
                             where_clause = self._where_clause()) as cursor:
            for row in cursor:
                changes.append(row)
                
        return changes
    
    def _where_clause(self):
        #:"StartDate" > date '2013-01-20' AND "StartDate" Is Not NULL
        return "StartDate Is NULL"
        
