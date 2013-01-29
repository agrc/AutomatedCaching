from agrc.caching.scheduled import Runner
from mock import Mock
from mock import patch

def testAreasOfChangeNotQueriedIfCurrentlyCaching():    
    with patch('agrc.caching.scheduled.cache.CacheStatusCommand') as cacheMock:
        with patch('agrc.caching.scheduled.sde.AreasOfChangeQuery') as queryMock:
            cacheInstance = cacheMock.return_value
            cacheInstance.execute.return_value = True
            
            queryInstance = queryMock.return_value
            queryInstance.execute.return_value = []
            
            s = Runner()
            s.start()
        
    cacheMock.assert_called_once_with()
    assert not queryMock.execute.called
    
def testAreasOfChangeQueriedIfNotCaching():    
    with patch('agrc.caching.scheduled.cache.CacheStatusCommand') as cacheMock:
        with patch('agrc.caching.scheduled.sde.AreasOfChangeQuery') as queryMock:
            cacheInstance = cacheMock.return_value
            cacheInstance.execute.return_value = False
            
            queryInstance = queryMock.return_value
            queryInstance.execute.return_value = []
            
            s = Runner()
            s.start()
        
    cacheMock.assert_called_once_with()
    queryMock.assert_called_once_with()