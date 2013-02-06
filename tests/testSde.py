from agrc.caching.queries import sde
from unittest import TestCase
from nose.tools import nottest
from mock import patch, Mock
from agrc.caching.config import Geodatabase

#@nottest 
class TestConnect(TestCase):
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'path')
    def test_command_can_connect_to_file_gdb(self, path_mock, fc_mock):
        print "test_command_can_connect_to_file_gdb"
        
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_Sorting")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertIsNotNone(result, "query is broken")
        self.assertEqual(len(result), 3, "no areas of change")