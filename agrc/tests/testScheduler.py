from unittest import TestCase, main
from mock import patch
from agrc.caching.scheduled import Runner
from agrc.caching.models import AreaOfChange

class TestScheduleRunner(TestCase):
    
    @patch('agrc.caching.scheduled.sde.AreasOfChangeQuery')
    @patch('agrc.caching.scheduled.cache.CacheStatusCommand')
    def test_areas_of_change_not_queried_if_caching(self, cache_mock, query_mock):
        cache_instance = cache_mock.return_value
        cache_instance.execute.return_value = True
        
        s = Runner()
        s.start()
        
        assert cache_mock.called
        assert not query_mock.called
    
    @patch('agrc.caching.scheduled.dto.GetCacheJobFromAreaOfChangeCommand')
    @patch('agrc.caching.scheduled.sde.AreasOfChangeQuery')
    @patch('agrc.caching.scheduled.cache.CacheStatusCommand')  
    def test_areas_of_change_queried_if_not_caching(self, cache_mock, query_mock, job_mock):
        cache_instance = cache_mock.return_value
        cache_instance.execute.return_value = False
        
        query_instance = query_mock.return_value
        query_instance.execute.return_value = [AreaOfChange([0,1,2], "roads")]
        
        job_instance = job_mock.return_value
        job_instance.execute.return_value = []
        
        s = Runner()        
        s.start()
            
        assert cache_mock.called
        assert query_mock.called

if __name__=='__main__':
    main()