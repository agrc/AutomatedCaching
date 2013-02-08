from agrc.caching.abstraction.base import Command
from agrc.caching import config
from agrc.caching import models
from arcpy import env
from arcpy.da import SearchCursor, UpdateCursor, InsertCursor
from datetime import datetime

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
        env.workspace = "{0}{1}".format(settings.base_path, settings.changes_path)
        
        changes = []
        with SearchCursor(settings.change_feature_class, self._fields,
                             where_clause = self._where_clause) as cursor:
            for row in cursor:
                change = models.AreaOfChange(row = row)
                changes.append(change)
             
        changes = sorted(changes, key=lambda change: change.creation_date)   
        
        return changes
    
    @property
    def _fields(self):
        return ['OBJECTID', 'CreationDate', 'StartDate', 'CompletionDate', 'Layer', 'Levels', 'Editor']
    
    @property
    def _where_clause(self):      
        return "StartDate Is NULL"
        
class InsertCacheJob(Command):
    """
        Responsible for creating records in cache job feature class
    """
    
    #: cache job
    job = None
    
    def __init__(self, job, service):
        self.job = job
        pass
    
    def execute(self):
        settings = config.Geodatabase()
        env.workspace = "{0}{1}".format(settings.base_path, settings.changes_path)
        
        with UpdateCursor(settings.change_feature_class, self._change_fields,
                             where_clause = self._where_clause(self.job.reference_id)) as updater:
            for row in updater:
                row[3] = datetime.now().isoformat()
#                updater.updateRow(row)
                with InsertCursor(settings.job_feature_class) as inserter:
                    pass
    
    @property
    def _change_fields(self):
        return ['OBJECTID', 'CreationDate', 'StartDate', 'Layer', 'Levels', 'Editor', 'SHAPE@']
         
    
    def _where_clause(self, oid):      
        return "OID@ == {0}".format(oid)