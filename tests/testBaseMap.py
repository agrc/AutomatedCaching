from unittest import TestCase
from agrc.caching.config import BaseMap
from nose.tools import nottest

class testBaseMap(TestCase):
    def testGetCompressionLevel(self):
        basemap = BaseMap()
        
        self.assertEqual(basemap.get_compression_level("terrain"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("TeRRaiN"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("TeRRaiN_new"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("TeRRaiN234"), basemap.get_high_quality(), "not returning correct compression for terrain")
        self.assertEqual(basemap.get_compression_level("1-2-2991.terrain"), basemap.get_high_quality(), "not returning correct compression for terrain")


        