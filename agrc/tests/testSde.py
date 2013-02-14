from unittest import TestCase, main
from mock import patch, Mock
from agrc.caching.queries import sde
from agrc.caching.commands import feature_class,dto
from agrc.caching.config import Geodatabase
from agrc.caching import models
from arcpy import env, Delete_management as delete_fc, CreateFeatureclass_management as create_fc,ExecuteError
from os import path

from agrc.tests import seedGdb
from datetime import datetime

class estSde(TestCase):
    
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
    def setUp(self):
        place = path.join(path.abspath(path.dirname(__file__)), "..\..", "data")
        
        out = path.join(place, "Test_AreaOfChange.gdb")
        template_path = path.join(place, "AreasOfChange.gdb\CacheJobItems")
        
        try:
            create_fc(out_path = out, out_name = "Test_CacheJobItems", template = template_path) 
        except ExecuteError:
            "cache jobs not created"
        
        template_path = path.join(place, "AreasOfChange.gdb\AreasOfChange")
        
        try:
            create_fc(out_path = out, out_name = "Test_AreasOfChange", template = template_path) 
        except ExecuteError:
            "changes not created"
        
    def tearDown(self):
        env.workspace = path.join(path.abspath(path.dirname(__file__)), "..\..", "data\Test_AreaOfChange.gdb")
        try:
            delete_fc("Test_CacheJobItems")
        except ExecuteError:
            "job not deleted"
        
        try:
            delete_fc("Test_AreasOfChange")
        except ExecuteError:
            "changes not deleted"
    
    @patch.object(Geodatabase,'job_feature_class')
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_seeding(self, path_mock, fc_change_mock, fc_job_mock):
        path_mock.__get__ = Mock(return_value="\Test_AreasOfChange.gdb")
        fc_job_mock.__get__ = Mock(return_value="Test_CacheJobItems")
        fc_change_mock.__get__ = Mock(return_value="Test_AreasOfChange")
        
        seedGdb.SeedAreaOfChange([models.AreaOfChange(row=[1,
                                                          datetime.now(),
                                                          None,
                                                          None,
                                                          "Roads",
                                                          "Steve",
                                                          [
                                                           [324260.346,4577721.286],
                                                           [365270.845,4600210.914],
                                                           [416536.520,4556181.180],
                                                           [363286.466,4515544.078]
                                                          ]])])
        pass
    
    @patch.object(Geodatabase,'job_feature_class')
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def can_insert_into_gdb(self, path_mock, fc_change_mock, fc_job_mock):       
        path_mock.__get__ = Mock(return_value="\Test_AreasOfChange.gdb")
        fc_job_mock.__get__ = Mock(return_value="CacheJobItems_testing")
        fc_change_mock.__get__ = Mock(return_value="AreaOfChange_testing")
        
        command = sde.AreasOfChangeQuery()
        initial_result = command.execute()
        
        self.assertEqual(1, len(initial_result), "should only be one area of change")
        
        command = dto.GetCacheJobItemsFromAreaOfChangeCommand(initial_result)
        jobs = command.execute()
        
        for job in jobs:
            command = feature_class.InsertCacheJobItemCommand(job)
            command.execute()
        
        command = sde.AreasOfChangeQuery()
        end_result = command.execute()
        
        self.assertLess(len(end_result), len(initial_result), "all the areas of change should be marked as started")
        
if __name__=='__main__':
    main()