from agrc.caching.scheduled import Runner
from agrc.caching.models import AreaOfChange
from mock import Mock, patch

def testAreasOfChangeNotQueriedIfCurrentlyCaching():    
    with patch('agrc.caching.scheduled.cache.CacheStatusCommand') as cache_mock:
        with patch('agrc.caching.scheduled.sde.AreasOfChangeQuery') as query_mock:
            cache_instance = cache_mock.return_value
            cache_instance.execute.return_value = True
            
            query_instance = query_mock.return_value
            query_instance.execute.return_value = []
            
            s = Runner()
            s.start()
        
    cache_mock.assert_called_once_with()
    assert not query_mock.execute.called
    
def testAreasOfChangeQueriedIfNotCaching():  
    with patch('agrc.caching.scheduled.cache.CacheStatusCommand') as cache_mock:
        with patch('agrc.caching.scheduled.sde.AreasOfChangeQuery') as query_mock:
            cache_instance = cache_mock.return_value
            cache_instance.execute.return_value = False
            
            query_instance = query_mock.return_value
            query_instance.execute.return_value = [AreaOfChange() for _ in xrange(2)]
            
            s = Runner()
            s.start()
        
    cache_mock.assert_called_once_with()
    query_mock.assert_called_once_with()