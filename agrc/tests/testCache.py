from unittest import TestCase, main
from agrc.caching.commands import cache
from agrc.caching.config import Server
from agrc.caching import models
from agrc.tests.geometry import Geometry

class TestCache(TestCase):
    def testCacheCommandReturnsFalse(self):
        server = Server(use_port = True)
        
        command = cache.CacheStatusCommand(server)
        caching = command.execute()
        
        self.assertFalse(caching, "server is not currently caching")
        
class TestProcessCacheJobItemsCommand(TestCase):
    def test_union(self):      
        geomer = Geometry()
        triangle = geomer.create_polygon([[0,0],[1,1],[1,0]])
        square = geomer.create_polygon([[0,0],[0,1],[1,1],[0,1]])
        
        job_items = [models.CacheJobItem(row=[0,"a",1, triangle]),
                 models.CacheJobItem(row=[0,"a",2, square]),
                 models.CacheJobItem(row=[0,"b",3, triangle]),
                 models.CacheJobItem(row=[0,"b",4, square])]
        
        command = cache.ProcessCacheJobItemsCommand(job_items)
        
        mapping = command._group_uniques_by_name_and_level(job_items)
        
        self.assertEqual(2, len(mapping.keys()), "should be two records one for a 0 and b 0")
        self.assertListEqual([1,2], mapping["a0"].reference_id, "reference id's are not appending correctly")
        self.assertListEqual([3,4], mapping["b0"].reference_id, "reference id's are not appending correctly")
        
if __name__=='__main__':
    main()