from unittest import TestCase
from mock import patch, Mock
from agrc.caching.commands import layer

class TestLayer(TestCase):
    
    @patch.object(layer.GetMapNamesContainingLayerCommand, '_layer_scale_name_map')
    def test_gets_right_map_names_for_job(self, map_mock):
        map_mock.__get__ = Mock(return_value=
                                {
                                 'ROADS': 
                                     {
                                      0: ["a", "b"],
                                      1: ["c", "b"],
                                      2: ["d", "c"],
                                      3: ["e", "a"],
                                      4: ["1"],
                                      5: ["f"]
                                     }
                                 })
        
        command = layer.GetMapNamesContainingLayerCommand(layer = "roads", levels=['0','1','2','3'])

        result = list(command.execute())
        
        self.assertEqual(len(result), len(["a","b","c","d","e"]), "lists are different")
        self.assertItemsEqual(result, ["a","b","c","d","e"], "list don't contain same elements")
        