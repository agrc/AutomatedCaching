from agrc.caching.abstraction.base import Command

class GetMapNamesContainingLayerCommand(Command):
    """
        This will contain a map for every layer in the base map 
        and what scales it is visible.
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
    
    def __init__(self, layer = None, change = None):
        if change is not None:
            self.layer = change.layer
        
        self.layer = layer or self._layer
        
    def get_layer(self):
        if self._layer is None:
            return None
        
        return self._layer.upper()
    
    def set_layer(self, layer):
        self._layer = layer
               
    def execute(self):
        return self._layer_scale_name_map[self.layer]
    
    layer = property(get_layer, set_layer)