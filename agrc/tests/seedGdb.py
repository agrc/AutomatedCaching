from agrc.caching import config
from arcpy import arcpy
from arcpy.da import InsertCursor
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
       
        with InsertCursor(self.fc_name, settings.change_schema(include_shape=True, include_oid = False)) as inserter:
            for change in changes:
                row = (change.creation_date,
                        change.start_date,
                        change.completion_date,
                        change.layer,
                        change.editor,
                        self.create_polygon(change.shape)
                        )
                inserter.insertRow(row)
            
    def create_polygon(self, coordinates):
        if coordinates is None:
            return None
        
        # Create empty Point and Array objects
        point = arcpy.Point()
        array = arcpy.Array()
        
        # A list that will hold each of the Polygon objects         
        for coordPair in coordinates:
            point.X = coordPair[0]
            point.Y = coordPair[1]
            array.add(point)
    
        # Add the first point of the array in to close off the polygon
        array.add(array.getObject(0))
    
        # Create a Polygon object based on the array of points
        return arcpy.Polygon(array)