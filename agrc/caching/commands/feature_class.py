from agrc.caching.abstraction.base import Command
from agrc.caching import config
from arcpy import env
from arcpy.da import UpdateCursor, InsertCursor, Editor
from datetime import datetime

class InsertCacheJobItemCommand(Command):
    """
        Responsible for creating records in cache job items feature class
    """
    
    #: cache job
    job = None
    
    def __init__(self, job):
        self.job = job
    
    def execute(self):
        settings = config.Geodatabase()
        path = "{0}{1}".format(settings.base_path, settings.changes_path)
        
        env.workspace = path
        edit = Editor(path)
        
        edit.startEditing(False, False)
        
        with UpdateCursor(settings.change_feature_class, self._change_fields,
                             where_clause = self._where_clause(self.job.reference_id)) as updater:
            for row in updater:
                row[2] = datetime.now()
                updater.updateRow(row)
                with InsertCursor(settings.job_feature_class, self._job_fields) as inserter:
                    inserter.insertRow((datetime.now(),
                                        self.job.scales,
                                        self.job.service_name,
                                        self.job.update_mode,
                                        row[7]
                                        ))
                    
        edit.stopEditing(True)
    
    @property
    def _change_fields(self):
        return ['OID@', 'CreationDate', 'StartDate',  'CompletionDate', 'Layer', 'Levels', 'Editor', 'SHAPE@']
    
    @property
    def _job_fields(self):
        return ['StartDate','Levels','MapService', 'UpdateMode','SHAPE@']
         
    def _where_clause(self, oid):      
        return "OBJECTID = {0}".format(oid)