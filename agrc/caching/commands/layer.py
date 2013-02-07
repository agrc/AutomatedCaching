from agrc.caching.abstraction.base import Command
from agrc.caching import enums

class GetMapNamesContainingLayerCommand(Command):
    """
        This will contain a map for every layer in the base map 
        and what scales it is visible.
        
        returns ['terrain', 'vector'] map names containing the layer
                                      visible in those scales
    """
    
    _layer_scale_name_map = {
                             'Roads': 
                                 {
                                  0: ["terrain", "vector", "hybrid"],
                                  1: ["terrain", "vector", "hybrid"]
                                 }, 
                             'Counties': 
                                {
                                 0: ["terrain", "vector", "hybrid"]
                                },
                             'Municipalities': 
                                {
                                 0: ["terrain"]
                                }
                             }
    
    layer = None
    
    levels = None
    
    def __init__(self, layer, levels):
        self.layer = layer
        self.levels = levels
        
    def execute(self):
        return [enums.BaseMaps().name.IMAGERY]