from agrc.caching import config
from arcpy import arcpy
from arcpy.da import InsertCursor

class SeedAreaOfChange(object):
    def __init__(self, changes):
        settings = config.Geodatabase()
        path = "{0}{1}".format(settings.base_path, settings.changes_path)
        
        arcpy.env.workspace = path
       
        with InsertCursor(settings.change_feature_class, settings.change_schema(include_shape=True)) as inserter:
            for change in changes:
                row = (change.start_date,
                                    change.creation_date,
                                    change.completion_date,
                                    change.layer,
                                    change.editor,
                                    self.create_polygon(change.shape)
                                    )
                inserter.insertRow(row)
            
    def create_polygon(self, coordinates):
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