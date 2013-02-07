from unittest import TestCase, main
from agrc.caching.commands import cache
from agrc.caching.config import Server

class TestCache(TestCase):
    def testCacheCommandReturnsFalse(self):
        server = Server(use_port = True)
        
        command = cache.CacheStatusCommand(server)
        caching = command.execute()
        
        self.assertFalse(caching, "server is not currently caching")
        
if __name__=='__main__':
    main()