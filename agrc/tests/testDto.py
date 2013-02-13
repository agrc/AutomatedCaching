from unittest import TestCase, main
from mock import patch, Mock
from agrc.caching.models import AreaOfChange
from agrc.caching.commands import dto
from agrc.caching.commands import layer

class TestDto(TestCase):
    @patch.object(layer.GetMapNamesContainingLayerCommand, '_layer_scale_name_map')
    def test_four_cache_jobs_created_four_different_scales_of_same_layer(self, map_mock):
        """
            each scale gets it's own cache job
        """
        
        map_mock.__get__ = Mock(return_value=
                                {
                                 'ROADS': 
                                     {
                                      "a": [0,1,2,3]
                                     }
                                 })
        
        changes = []
        changes.append(AreaOfChange("ROADS"))
        
        command = dto.GetCacheJobItemsFromAreaOfChangeCommand(changes)
        jobs = command.execute()
        
        self.assertIsNotNone(jobs, "jobs are empty")
        self.assertEqual(4, len(jobs), "incorrect amount of jobs from changes {0}".format(len(jobs)))        
        
    @patch.object(layer.GetMapNamesContainingLayerCommand, '_layer_scale_name_map')
    def test_creates_a_job_for_each_scale(self, map_mock):
        """
            each scale gets it's own cache job
        """
        
        map_mock.__get__ = Mock(return_value=
                                {
                                 'ROADS': 
                                     {
                                      "a": [0,1,2,3]
                                     },
                                 'COUNTIES': 
                                     {
                                      "b": [4,5,6]
                                     }
                                 })
        
        changes = []
        changes.append(AreaOfChange("ROADS"))
        changes.append(AreaOfChange("COUNties"))
        
        command = dto.GetCacheJobItemsFromAreaOfChangeCommand(changes)
        jobs = command.execute()
        
        self.assertIsNotNone(jobs, "jobs are empty")
        self.assertEqual(7, len(jobs), "incorrect amount of jobs from changes {0}".format(len(jobs)))        
        
if __name__=='__main__':
    main()