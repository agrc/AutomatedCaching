from unittest import TestCase, main
from agrc.caching.config import BaseMap

class TestBaseMap(TestCase):
    def testGetCompressionLevel(self):
        basemap = BaseMap()
        
        self.assertEqual(basemap.get_compression_level("terrain"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("TeRRaiN"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("TeRRaiN_new"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("TeRRaiN234"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("1-2-2991.terrain"), basemap.get_high_quality(), "not returning correct compression for terrain")
        
if __name__=='__main__':
    main()