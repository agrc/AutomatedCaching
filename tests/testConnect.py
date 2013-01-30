from mock import Mock, patch
from agrc.caching.commands import connect
from agrc.caching.config import Server
from unittest import TestCase

class ConnectTests(TestCase):
    def testCacheStatusCanGetAToken(self):
        with patch('agrc.caching.config.Server') as server_mock:
            server_instance = server_mock.return_value
            server_instance.url.return_value = "localhost"
            
            command = connect.GetTokenCommand()
            token = command.execute()
            
            self.assertIsNotNone(token)    