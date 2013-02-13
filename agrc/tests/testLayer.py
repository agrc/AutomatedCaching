from unittest import TestCase, main
from mock import patch, Mock
from agrc.caching.commands import layer

class TestLayer(TestCase):
    
    @patch.object(layer.GetMapNamesContainingLayerCommand, '_layer_scale_name_map')
    def test_gets_right_map_names_for_job(self, map_mock):
        map_mock.__get__ = Mock(return_value=
                                {
                                 'ROADS': 
                                     {
                                      "a": [0,3],
                                      "b": [0,1],
                                      "c": [1,2]
                                     }
                                 })
        
        command = layer.GetMapNamesContainingLayerCommand(layer = "roads")
        result = command.execute()
        
        for i in result:
            print i
        
        self.assertEqual(len(result), len(["a","b","c"]), "lists are different")
        self.assertItemsEqual([0,3], result["a"], "arrays are different")
        self.assertItemsEqual({"a": [0,3],"b": [0,1],"c": [1,2]}, result, "list don't contain same elements")

if __name__=='__main__':
    main()