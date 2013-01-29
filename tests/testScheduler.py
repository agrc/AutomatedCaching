from agrc.caching.scheduler import Scheduler
from mock import Mock
from mock import patch

def TestGetChangesIsNotCalledIfCurrentlyCaching():    
    with patch('agrc.caching.scheduler.cache.CacheStatusCommand') as mock:
        instance = mock.return_value
        instance.execute.return_value = True
        s = Scheduler()
        s.start()
        
    assert mock.assert_called_once_with()