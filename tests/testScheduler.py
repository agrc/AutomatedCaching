from agrc.caching.scheduled import Runner
from agrc.caching.models import AreaOfChange
from mock import patch
from nose.tools import nottest
from unittest import TestCase

@nottest
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
    
    @patch('agrc.caching.scheduled.sde.AreasOfChangeQuery')
    @patch('agrc.caching.scheduled.cache.CacheStatusCommand')  
    def test_areas_of_change_queried_if_not_caching(self, cache_mock, query_mock):
        cache_instance = cache_mock.return_value
        cache_instance.execute.return_value = False
        
        query_instance = query_mock.return_value
        query_instance.execute.return_value = [AreaOfChange() for _ in xrange(2)]
        
        s = Runner()
        s.start()
            
        assert cache_mock.called
        assert query_mock.called