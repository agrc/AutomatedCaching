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

class TestSde(TestCase):
    test_gdb = "Test_AreasOfChange.gdb"
    test_job_items_fc = "Test_CacheJobItems"
    test_changes_fc = "Test_AreasOfChange"
    base_path = path.join(path.abspath(path.dirname(__file__)), "..\..", "data")
    seeder = seedGdb.SeedAreaOfChange(base_path, test_gdb, test_changes_fc)
    def setUp(self):
        out = path.join(self.base_path, self.test_gdb)
        template_path = path.join(self.base_path, "AreasOfChange.gdb\CacheJobItems")
        
        try:
            create_fc(out_path = out, 
                      out_name = self.test_job_items_fc, 
                      template = template_path,
                      spatial_reference = template_path) 
        except ExecuteError:
            "cache jobs not created"
        
        template_path = path.join(self.base_path, "AreasOfChange.gdb\AreasOfChange")
        
        try:
            create_fc(out_path = out, 
                      out_name = self.test_changes_fc, 
                      template = template_path,
                      spatial_reference = template_path) 
        except ExecuteError:
            "changes not created"
            
        
        self.seeder.seed([models.AreaOfChange(row=[1,
                                              datetime(2011,1,1),
                                              None,
                                              None,
                                              "Roads",
                                              "Steve"
                                              ])])
        self.seeder.seed([models.AreaOfChange(row=[2,
                                              datetime(2013,1,1),
                                              datetime.now(),
                                              None,
                                              "Counties",
                                              "Steve"
                                              ])])
        self.seeder.seed([models.AreaOfChange(row=[3,
                                              datetime(2012,1,1),
                                              datetime.now(),
                                              None,
                                              "Municipalities",
                                              "Steve"
                                              ])])
        
    def tearDown(self):
        env.workspace = path.join(path.abspath(path.dirname(__file__)), "..\..", "data\Test_AreaOfChange.gdb")
        try:
            delete_fc(self.test_job_items_fc)
        except ExecuteError:
            "job not deleted"
        
        try:
            delete_fc(self.test_changes_fc)
        except ExecuteError:
            "changes not deleted"
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_command_can_connect_to_file_gdb(self, path_mock, fc_mock):
        path_mock.__get__ = Mock(return_value="Test_AreasOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="Test_AreasOfChange")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertIsNotNone(result, "query is broken")
        self.assertEqual(len(result), 1, "no areas of change")


    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_can_sort(self, path_mock, fc_mock):       
        path_mock.__get__ = Mock(return_value="Test_AreasOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="Test_AreasOfChange")
        
        self.seeder.seed([models.AreaOfChange(row=[4,
                                              datetime(2013,1,1),
                                              None,
                                              None,
                                              "Counties",
                                              "Steve"
                                              ])])
        self.seeder.seed([models.AreaOfChange(row=[5,
                                              datetime(2012,1,1),
                                              None,
                                              None,
                                              "Municipalities",
                                              "Steve"
                                              ])])

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertLess(result[0].creation_date, result[1].creation_date, "order is wrong")
        self.assertLess(result[1].creation_date, result[2].creation_date, "order is wrong")
    
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def test_gets_changes_properly(self, path_mock, fc_mock):
        path_mock.__get__ = Mock(return_value="Test_AreasOfChange.gdb")
        fc_mock.__get__ = Mock(return_value="Test_AreasOfChange")

        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertEqual(len(result), 1, "There is only one area of change needing attention")
        self.assertEqual(result[0].layer, "Roads", "Wrong change")
    
class TestInsertCacheJob(TestCase):
    test_gdb = "Test_AreasOfChange.gdb"
    test_job_items_fc = "Test_CacheJobItems"
    test_changes_fc = "Test_AreasOfChange"
    base_path = path.join(path.abspath(path.dirname(__file__)), "..\..", "data")
    
    def setUp(self):
        out = path.join(self.base_path, self.test_gdb)
        template_path = path.join(self.base_path, "AreasOfChange.gdb\CacheJobItems")
        
        try:
            create_fc(out_path = out, 
                      out_name = self.test_job_items_fc, 
                      template = template_path,
                      spatial_reference = template_path) 
        except ExecuteError:
            "cache jobs not created"
        
        template_path = path.join(self.base_path, "AreasOfChange.gdb\AreasOfChange")
        
        try:
            create_fc(out_path = out, 
                      out_name = self.test_changes_fc, 
                      template = template_path,
                      spatial_reference = template_path) 
        except ExecuteError:
            "changes not created"
            
        seeder = seedGdb.SeedAreaOfChange(self.base_path, self.test_gdb, self.test_changes_fc)
        seeder.seed([models.AreaOfChange(row=[1,
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
        
    def tearDown(self):
        env.workspace = path.join(path.abspath(path.dirname(__file__)), "..\..", "data\Test_AreaOfChange.gdb")
        try:
            delete_fc(self.test_job_items_fc)
        except ExecuteError:
            "job not deleted"
        
        try:
            delete_fc(self.test_changes_fc)
        except ExecuteError:
            "changes not deleted"
    
    @patch.object(Geodatabase,'job_feature_class')
    @patch.object(Geodatabase,'change_feature_class')
    @patch.object(Geodatabase,'changes_path')
    def can_insert_into_gdb(self, path_mock, fc_change_mock, fc_job_mock):       
        path_mock.__get__ = Mock(return_value = self.test_gdb)
        fc_job_mock.__get__ = Mock(return_value = self.test_job_items_fc)
        fc_change_mock.__get__ = Mock(return_value = self.test_changes_fc)
        
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