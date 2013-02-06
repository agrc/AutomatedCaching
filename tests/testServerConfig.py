from unittest import TestCase
from agrc.caching.config import Server
from nose.tools import nottest

@nottest
class testServerConfigGetTokenUrl(TestCase):
    def testUseHttpsReturnsUrlStartingWithHttps(self):
        server = Server(use_https = True)
        
        url = server.get_token_url()
        
        self.assertTrue(url.startswith("https"), "https not added correctly")
        
    def testPropertiesBuildUrlCorrectly(self):
        server = Server(server_name = "agrc")
        
        url = server.get_token_url()
        
        self.assertEqual(url, "http://agrc/arcgis/tokens/generateToken", "instance not added correctly")
        
    def testUsePortAddsPortToUrlCorrectly(self):
        server = Server(use_port = True, server_name = "agrc")
        
        url = server.get_token_url()
                
        print url
        self.assertEqual(url, "http://agrc:6080/arcgis/tokens/generateToken", "port not added correctly")

@nottest
class testServerConfigGetStatsurl(TestCase):
    def testUseHttpsReturnsUrlStartingWithHttps(self):
        server = Server(use_https = True)
        
        url = server.get_statistics_url("CachingTools.GPServer")
        
        print url
        
        self.assertTrue(url.startswith("https"), "https not added correctly")
        
    def testPropertiesBuildUrlCorrectly(self):
        server = Server(server_name = "agrc")
        
        url = server.get_statistics_url("CachingTools.GPServer")
        
        self.assertEqual(url, "http://agrc/arcgis/admin/services/System/CachingTools.GPServer/statistics")
        
    def testUsePortAddsPortToUrlCorrectly(self):
        server = Server(use_port = True, server_name = "agrc")
        
        url = server.get_statistics_url("CachingTools.GPServer")
        
        self.assertEqual(url, "http://agrc:6080/arcgis/admin/services/System/CachingTools.GPServer/statistics", "port not added correctly")