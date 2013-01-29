from mock import Mock, patch
from unittest import TestCase
from agrc.caching.config import Server

class testServerConfig(TestCase):
    def testUseHttpsReturnsUrlStartingWithHttps(self):
        server = Server()
        server.useHttps = True
        
        url = server.getTokenUrl()
        
        print url
        
        assert url.startswith("https")
        
    def testPropertiesBuildUrlCorrectly(self):
        server = Server()
        server.serverName = "agrc"
        
        url = server.getTokenUrl()
        
        self.assertEqual(url, "http://agrc/arcgis/tokens/generateToken")
        
    def testUsePortAddsPortToUrlCorrectly(self):
        server = Server()
        server.usePort = True
        server.serverName = "agrc"
        
        url = server.getTokenUrl()
        
        self.assertEqual(url, "http://agrc:6080/arcgis/tokens/generateToken", "port not added correctly")