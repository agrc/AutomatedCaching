from mock import Mock, patch
from agrc.caching.commands import connect
from agrc.caching.config import Server
from unittest import TestCase
from nose.tools import nottest

@nottest
class ConnectTests(TestCase):
    def testCacheStatusCanGetAToken(self):
        server = Server(use_port = True)
            
        command = connect.GetTokenCommand(server)
        token = command.execute()
        
        self.assertIsNotNone(token)
        self.assertGreater(len(token), 10, "token length is too small") 
            
    def testCacheStatusCanGetStatusJson(self):
        server = Server(use_port = True)
            
        command = connect.GetTokenCommand(server)
        token = command.execute()
        
        command = connect.GetServiceStatisticsCommand("CachingTools.GPServer", token, server)
        stats = command.execute()
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['summary']['busy'], 0, "busy stats should be 0")