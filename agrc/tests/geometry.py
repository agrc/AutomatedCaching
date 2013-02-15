import arcpy

class Geometry(object):
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