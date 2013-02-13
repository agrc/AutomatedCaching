from agrc.caching.abstraction.base import Command
from agrc.caching import enums

class GetMapNamesContainingLayerCommand(Command):
    """
        This will contain a map for every layer in the base map 
        and what scales it is visible.
        
        returns ['terrain', 'vector'] map names containing the layer
                                      visible in those scales
    """
    
    @property
    def _layer_scale_name_map(self): 
        return {
                 'ROADS': 
                     {
                      "terrain": [0,1],
                      "vector": [0,1],
                      "hybrid": [0,1]
                     }, 
                 'COUNTIES': 
                    {
                     "terrain": [0],
                     "vector": [0],
                     "hybrid": [0]
                    },
                 'MUNICIPALITIES': 
                    {
                     "terrain": [0]
                    }
                 }
    
    _layer = None
    
    levels = None
    
    def __init__(self, layer = None, levels = None, job = None):
        if job is not None:
            self.layer = job.layer
            self.levels = job.levels
        
        self.layer = layer or self._layer
        self.levels = levels or self.levels
        
    def get_layer(self):
        if self._layer is None:
            return None
        
        return self._layer.upper()
    
    def set_layer(self, layer):
        self._layer = layer
               
    def execute(self):
        maps = set()
        for layer_key in self._layer_scale_name_map.keys():
            if layer_key == self.layer:
                for scale in self.levels:  
                    if scale in self._layer_scale_name_map[layer_key].keys():
                        # union into master set
                        maps |= set(self._layer_scale_name_map[layer_key][scale])   
                                  
        return list(maps)
    
    layer = property(get_layer, set_layer)