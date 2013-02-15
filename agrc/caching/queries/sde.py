from agrc.caching.abstraction.base import Command
from agrc.caching import config
from agrc.caching import models
from arcpy import env
from arcpy.da import SearchCursor
from os import path

class AreasOfChangeQuery(Command):
    """
        Queries geodata where startdate is null meaning the area of change
        hasn't been picked up yet and started.
    """
    
    def execute(self):
        # query sde get new changes
        return self._query_sde_for_new_changes()
    
    def _query_sde_for_new_changes(self):      
        settings = config.Geodatabase()
        env.workspace = path.join(settings.base_path, settings.changes_gdb_path)
        
        changes = []
        with SearchCursor(settings.change_feature_class, settings.change_schema(include_shape=False, include_oid = True),
                             where_clause = self._where_clause) as cursor:
            for row in cursor:
                change = models.AreaOfChange(row = row)
                changes.append(change)
             
        changes = sorted(changes, key=lambda change: change.creation_date)   
        
        return changes
    
    @property
    def _where_clause(self):      
        return "StartDate Is NULL"
    
class CacheJobItemsQuery(Command):
    """
        Queries geodata where startdate is null meaning the area of change
        hasn't been picked up yet and started.
    """
    
    def execute(self):
        # query sde get new changes
        return self._query_sde_for_new_changes()
    
    def _query_sde_for_new_changes(self):      
        settings = config.Geodatabase()
        env.workspace = path.join(settings.base_path, settings.changes_gdb_path)
        
        changes = []
        with SearchCursor(settings.item_feature_class, settings.items_schema()) as cursor:
            for row in cursor:
                change = models.AreaOfChange(row = row)
                changes.append(change)
             
        changes = sorted(changes, key=lambda change: change.creation_date)   
        
        return changes