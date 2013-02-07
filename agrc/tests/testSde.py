from unittest import TestCase
from mock import patch, Mock
from agrc.caching.queries import sde
from agrc.caching.config import Geodatabase

class TestConnect(TestCase):
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'path')
    def test_command_can_connect_to_file_gdb(self, path_mock, fc_mock):       
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_Sorting")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertIsNotNone(result, "query is broken")
        self.assertEqual(len(result), 3, "no areas of change")

    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'path')
    def test_can_sort(self, path_mock, fc_mock):       
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_Sorting")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertLess(result[0].creation_date, result[1].creation_date, "order is wrong")
        self.assertLess(result[1].creation_date, result[2].creation_date, "order is wrong")
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'path')
    def test_gets_changes_properly(self, path_mock, fc_mock):
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_HasChanges")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertEqual(len(result), 1, "There is only one area of change needing attention")
        self.assertEqual(result[0].layer, "Roads", "Wrong change")
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'path')
    def test_gets_changes_properly_where_none_are_there(self, path_mock, fc_mock):
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_NoChanges")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertEqual(len(result), 0, "There is only one area of change needing attention")