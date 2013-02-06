from agrc.caching.scheduled import Runner
from agrc.caching.models import AreaOfChange
from mock import patch

@patch('agrc.caching.scheduled.sde.AreasOfChangeQuery')
@patch('agrc.caching.scheduled.cache.CacheStatusCommand')
def testAreasOfChangeNotQueriedIfCurrentlyCaching(cache_mock, query_mock):
    cache_instance = cache_mock.return_value
    cache_instance.execute.return_value = True
    
    s = Runner()
    s.start()
        
    print cache_mock.call_count
    print query_mock.call_count
 
    print dir(cache_instance)
    
    assert cache_mock.called
    assert not query_mock.called

@patch('agrc.caching.scheduled.sde.AreasOfChangeQuery')
@patch('agrc.caching.scheduled.cache.CacheStatusCommand')  
def testAreasOfChangeQueriedIfNotCaching(cache_mock, query_mock):
    cache_instance = cache_mock.return_value
    cache_instance.execute.return_value = False
    
    query_instance = query_mock.return_value
    query_instance.execute.return_value = [AreaOfChange() for _ in xrange(2)]
    
    s = Runner()
    s.start()
        
    assert cache_mock.called
    assert query_mock.called