from unittest import TestCase, main
from mock import patch, Mock
from agrc.caching.queries import sde
from agrc.caching.config import Geodatabase
from arcpy import env
from arcpy import Copy_management as copy_fc
from arcpy import Delete_management as delete_fc
from arcpy import CreateFeatureclass_management as create_fc
from arcpy import ExecuteError
from os import path
from nose.tools import nottest

@nottest
class TestSde(TestCase):
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_command_can_connect_to_file_gdb(self, path_mock, fc_mock):       
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_Sorting")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertIsNotNone(result, "query is broken")
        self.assertEqual(len(result), 3, "no areas of change")
        
        for i in result:
            if i.id == 1:
                self.assertTrue(i.creation_date.isoformat().startswith("2013-01-01"), "date is off")
                self.assertEqual(i.start_date, None, "start date off")
                self.assertEqual(i.completion_date, None, "completion off")
                self.assertEqual(i.layer, "Roads", "layer is offf")
                self.assertEqual(i.levels, [0,1,2], "levels off")
                self.assertEqual(i.editor, "User1", "user is off")
                
                return
        
        self.assertTrue(False, "shouldn't get here")

    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_can_sort(self, path_mock, fc_mock):       
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_Sorting")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertLess(result[0].creation_date, result[1].creation_date, "order is wrong")
        self.assertLess(result[1].creation_date, result[2].creation_date, "order is wrong")
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_gets_changes_properly(self, path_mock, fc_mock):
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_HasChanges")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertEqual(len(result), 1, "There is only one area of change needing attention")
        self.assertEqual(result[0].layer, "Roads", "Wrong change")
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_gets_changes_properly_where_none_are_there(self, path_mock, fc_mock):
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="AreaOfChange_NoChanges")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertEqual(len(result), 0, "There is only one area of change needing attention")
    
class TestInsertCacheJob(TestCase):
    @classmethod
    def setUpClass(cls):
        env.workspace = path.join(path.abspath(path.dirname(__file__)), "..\..", "data\Test_AreaOfChange.gdb")
        try:
            create_fc(env.workspace, "CacheJob_Inserts_testing", template="CacheJob_Inserts")
        except ExecuteError:
            "cache jobs not created"
        
        try:
            copy_fc("AreaOfChange_HasChanges", "AreaOfChange_testing")
        except ExecuteError:
            "changes not created"
        
    @classmethod
    def tearDownClass(cls):
        env.workspace = path.join(path.abspath(path.dirname(__file__)), "..\..", "data\Test_AreaOfChange.gdb")
        try:
            delete_fc("CacheJob_Inserts_testing")
        except ExecuteError:
            "job not deleted"
        
        try:
            delete_fc("AreaOfChange_testing")
        except ExecuteError:
            "changes not deleted"
     
    @patch.object(Geodatabase,'job_feature_class')
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_can_insert_into_gdb(self, path_mock, fc_change_mock, fc_job_mock):       
        path_mock.__get__ = Mock(return_value="\Test_AreaOfChange.gdb")
        fc_job_mock.__get__ = Mock(return_value="CacheJob_Inserts_testing")
        fc_change_mock.__get__ = Mock(return_value="AreaOfChange_Sorting")
        
if __name__=='__main__':
    main()