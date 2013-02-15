from agrc.caching import config
from arcpy import arcpy
from arcpy.da import InsertCursor
from agrc.tests.geometry import Geometry
from os import path

class SeedAreaOfChange(object):
    def __init__(self,base_path,gdb_name,fc_name):
        self.base_path = base_path
        self.gdb_name = gdb_name
        self.fc_name = fc_name
    
    def seed(self, changes):
        settings = config.Geodatabase()
        place = path.join(self.base_path, self.gdb_name)
        
        arcpy.env.workspace = place
        geometry = Geometry()
        
        with InsertCursor(self.fc_name, settings.change_schema(include_shape=True, include_oid = False)) as inserter:
            for change in changes:
                row = (change.creation_date,
                        change.start_date,
                        change.completion_date,
                        change.layer,
                        change.editor,
                        geometry.create_polygon(change.shape))
                
                inserter.insertRow(row)

class SeedCacheJobItems(object):
    def __init__(self,base_path,gdb_name,fc_name):
        self.base_path = base_path
        self.gdb_name = gdb_name
        self.fc_name = fc_name
    
    def seed(self, job_items):
        settings = config.Geodatabase()
        place = path.join(self.base_path, self.gdb_name)
        
        arcpy.env.workspace = place
        geometry = Geometry()
        
        with InsertCursor(self.fc_name, settings.items_schema(include_shape=True, include_oid = False)) as inserter:
            for item in job_items:
                row = (item.level,
                        item.service_name,
                        item.reference_id,
                        geometry.create_polygon(item.shape))
                
                inserter.insertRow(row)
            
    